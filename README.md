# Application d'Envoi d'E-mails avec Django

Cette application Django permet d'envoyer des e-mails via une interface web conviviale. Elle utilise Outlook pour envoyer les e-mails et permet de joindre des pièces jointes.

# Pré-utilisation de l'application
## Fonctionnalités

- Envoi d'e-mails à plusieurs destinataires (To, Cc, Bcc).
- Personnalisation du contenu de l'e-mail avec un éditeur de texte.
- Envoi de pièces jointes.
- Envoi d'une copie de vérification à l'expéditeur.

# Prérequis pour la machine

Pour exécuter cette application, assurez-vous d'avoir les éléments suivants installés sur votre système :

- **Python 3.x** : L'application est compatible avec Python 3. Vous pouvez télécharger Python depuis [python.org](https://www.python.org/).

- **Django** : Le framework web utilisé pour cette application. Vous pouvez l'installer via pip :
  ```bash
  pip install django
  ```

- **win32com** : Utilisé pour l'intégration avec Microsoft Outlook. Installez-le via pip :
```bash
pip install pywin32
```

- **pandas** : Utilisé pour la gestion des fichiers Excel. Installez-le via pip :
```bash
pip install pandas
```

### Si les Prérequis ne Sont Pas Satisfaits

Si vous rencontrez des problèmes d'installation ou si les prérequis ne sont pas satisfaits, voici quelques étapes à suivre :

1. **Vérifiez Votre Version de Python** :
   - Assurez-vous que Python 3.x est installé sur votre système. Vous pouvez vérifier votre version de Python en exécutant :
     ```bash
     python --version
     ```

2. **Installez les Dépendances Manquantes** :
   - Si une dépendance est manquante, utilisez pip pour l'installer. Par exemple, pour installer Django :
     ```bash
     pip install django
     ```

3. **Vérifiez Votre Installation de Microsoft Outlook** :
   - Assurez-vous que Microsoft Outlook est correctement installé et configuré sur votre machine. `win32com` nécessite Outlook pour fonctionner correctement.

4. **Utilisez un Environnement Virtuel** :
   - Pour éviter les conflits de dépendances, il est recommandé d'utiliser un environnement virtuel. Vous pouvez en créer un avec :
     ```bash
     python -m venv env
     source env/bin/activate  # Sur Windows, utilisez `env\Scripts\activate`
     ```

5. **Consultez la Documentation** :
   - Si vous rencontrez des problèmes spécifiques, consultez la documentation officielle de chaque dépendance ou recherchez des solutions en ligne.

En suivant ces étapes, vous devriez être en mesure de satisfaire les prérequis et de faire fonctionner l'application correctement. Si vous avez des questions ou des problèmes persistants, n'hésitez pas à contacter le support ou à consulter les forums de la communauté.


# Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/eliaz-qrc/email_sender.git
   cd email_sender
   ```

# Utilisation

### Vérifications préalables

1. **Excel des membres CACS** : Si vous n'avez pas rempli l'excel qui était envoyé dans le groupe WhatsApp spam CACS par Eliaz alors rendez-vous sur: https://centralesupelec-my.sharepoint.com/:x:/g/personal/eliaz_queric_student-cs_fr/EafdHiGeLAZAjBdGCLUWVOUBI2Svljb4WeswEBM1XBqp_Q?e=U4ezg8 et renseignez vos informations puis en informer Eliaz. Sinon le modifiez l'excel Membres_CACS.xlsx en local dans email_sender/email_app.

### Envoie de mail

1. **Ouvrez VScode et ouvrez un terminal** (ou tout autre terminal de votre choix)
2. **Rendez-vous dans le dossier email_sender avec son chemin d'accès dans le terminal**
3. **Tapez** ```python manage.py runserver```
4. **Cliquez sur le lien qui apparaît dans votre terminal** : http://127.0.0.1:8000/
5. **Renseignez les champs demandés**:

### Quelques informations importantes pour le bon envoie du mail:
- Vous devez bien-sûr être connecté à internet
- Pour mettre plusieurs destinataires les séparer d'un **;**
- Le titre du mail est aussi l'objet 
> **Exemple**: Titre saisi: *Demande de devis*
> Objet du mail: *[CACS CentraleSupélec] Demande de devis*
- A la fin du mail sera mis automatiquement une signature automatique, donc il n'est pas nécessaire de signer son mail. 
>  ![Exemple de bas de page](https://i.imgur.com/sFKshZ1.png)
- Une copie du mail vous sera envoyée pour que vous puissiez vérifier que toutes les informations que vous souhaitiez saisir apparaîssent bien.