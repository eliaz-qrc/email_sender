from django.shortcuts import render, redirect
from django.http import HttpResponse
import pythoncom
import win32com.client
import os
import re
import pandas as pd
import unicodedata

def enlever_accents(texte):
    texte_normalise = unicodedata.normalize('NFD', texte)
    texte_sans_accents = ''.join(
        char for char in texte_normalise
        if unicodedata.category(char) != 'Mn'
    )
    return texte_sans_accents

def formater_texte(texte):
    texte = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texte)
    texte = re.sub(r'\*(.*?)\*', r'<i>\1</i>', texte)
    return texte

def format_french_phone_number(phone_number: int):
    phone_str = str(phone_number)
    if len(phone_str) != 9:
        raise ValueError("Le numéro doit contenir exactement 9 chiffres (sans le 0 initial).")
    formatted_number = f"+33 {phone_str[0]} {phone_str[1:3]} {phone_str[3:5]} {phone_str[5:7]} {phone_str[7:]}"
    return formatted_number

def trouver_template_html():
    chemin_script = os.path.dirname(os.path.abspath(__file__))
    chemin_template = os.path.join(chemin_script, "templates", "Template-Mail-CACS.html")
    return chemin_template if os.path.exists(chemin_template) else None

def charger_donnees_excel():
    chemin_script = os.path.dirname(os.path.abspath(__file__))
    chemin_excel = os.path.join(chemin_script, "Membres_CACS.xlsx")
    return pd.read_excel(chemin_excel) if os.path.exists(chemin_excel) else None

def recuperer_infos_membre(df, nom, prenom):
    membre = df[(df["Nom"].str.lower() == nom.lower()) & (df["Prénom"].str.lower() == prenom.lower())]
    return (membre.iloc[0]["Poste"], membre.iloc[0]["Numéro"]) if not membre.empty else (None, None)

def index(request):
    return render(request, 'form.html')

def envoyer_email(request):
    if request.method == 'POST':
        pythoncom.CoInitialize()  # Initialiser COM
        try:
            destinataires = request.POST['destinataires']
            cc = request.POST['cc']
            bcc = request.POST['bcc']
            titre = request.POST['titre']
            contenu = request.POST['contenu']
            nom = request.POST['nom']
            prenom = request.POST['prenom']
            pieces_jointes = request.FILES.getlist('pieceJointe[]')  # Récupération de plusieurs fichiers

            outlook = win32com.client.Dispatch("Outlook.Application")
            df_membres = charger_donnees_excel()

            if df_membres is None:
                return render(request, 'notification_echec.html', {'raison_echec': 'Fichier Excel introuvable.'})

            email_auteur = f"{enlever_accents(prenom).lower()}.{enlever_accents(nom).lower()}@student-cs.fr"
            nom_prenom_auteur = f"{prenom.capitalize()} {nom.capitalize()}"
            poste, numero = recuperer_infos_membre(df_membres, nom, prenom)

            if poste is None or numero is None:
                return render(request, 'notification_echec.html', {'raison_echec': 'Auteur non trouvé dans le fichier Excel.'})

            numero = format_french_phone_number(numero)

            chemin_template = trouver_template_html()
            if not chemin_template:
                return render(request, 'notification_echec.html', {'raison_echec': 'Fichier HTML introuvable.'})

            with open(chemin_template, "r", encoding="utf-8") as f:
                html_content = f.read()
                html_content = html_content.replace("{{titre_mail}}", titre)
                html_content = html_content.replace("{{contenu_mail}}", "<br>".join([formater_texte(ligne) for ligne in contenu.split('\n')]))
                html_content = html_content.replace("{{nom_prenom}}", nom_prenom_auteur)
                html_content = html_content.replace("{{email_auteur}}", email_auteur)
                html_content = html_content.replace("{{poste}}", poste)
                html_content = html_content.replace("{{numero}}", numero)

            mail = outlook.CreateItem(0)
            mail.To = destinataires
            mail.CC = cc
            mail.BCC = bcc
            mail.Subject = f"[CACS CentraleSupélec] {titre}"
            mail.HTMLBody = html_content

            # Gestion des pièces jointes multiples
            fichiers_temporaires = []  # Pour stocker les chemins des fichiers temporaires
            for fichier in pieces_jointes:
                chemin_piece_jointe = os.path.join(os.getcwd(), fichier.name)
                with open(chemin_piece_jointe, 'wb+') as destination:
                    for chunk in fichier.chunks():
                        destination.write(chunk)
                mail.Attachments.Add(chemin_piece_jointe)
                fichiers_temporaires.append(chemin_piece_jointe)  # Stockage du fichier temporaire

            mail.Send()

            # Envoi d'une copie de vérification à l'auteur
            mail_verification = outlook.CreateItem(0)
            mail_verification.To = email_auteur
            mail_verification.Subject = f"Vérification mail: {titre}"
            mail_verification.HTMLBody = html_content
            mail_verification.Send()

            # Suppression des fichiers temporaires après l'envoi
            for fichier in fichiers_temporaires:
                if os.path.exists(fichier):
                    os.remove(fichier)

            return render(request, 'confirmation_envoi.html')

        except Exception as e:
            return render(request, 'notification_echec.html', {'raison_echec': str(e)})

        finally:
            pythoncom.CoUninitialize()  # Libérer COM

    return redirect('index')
