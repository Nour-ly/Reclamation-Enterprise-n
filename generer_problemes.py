import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employeeproject.settings')
django.setup()

from django.contrib.auth.models import User, Group
# L'importation correcte ciblée sur l'application agent !
from agent.models import Reclamation


def insert_problemes():
    print("⏳ ÉTAPE 1 : Configuration des rôles et création de l'Agent...")

    group_agent, _ = Group.objects.get_or_create(name='Agent')
    group_employee, _ = Group.objects.get_or_create(name='Employee')

    # Compte Agent pour tes démos
    if not User.objects.filter(username='MonAgent').exists():
        mon_agent = User.objects.create_user(username='MonAgent', password='password123')
        mon_agent.groups.add(group_agent)
        print("   ✅ Agent 'MonAgent' opérationnel.")

    print("\n👥 ÉTAPE 2 : Génération des 15 employés de l'entreprise...")

    def obtenir_ou_creer_employe(nom):
        if User.objects.filter(username=nom).exists():
            return User.objects.get(username=nom)
        else:
            nouvel_emp = User.objects.create_user(username=nom, password='password123')
            nouvel_emp.groups.add(group_employee)
            print(f"   [+] Employé créé : {nom}")
            return nouvel_emp

    # Création des 15 comptes d'employés
    emp1 = obtenir_ou_creer_employe('sami_dev')
    emp2 = obtenir_ou_creer_employe('leila_rh')
    emp3 = obtenir_ou_creer_employe('wiam_dev')
    emp4 = obtenir_ou_creer_employe('youssef_data')
    emp5 = obtenir_ou_creer_employe('lina_rh')
    emp6 = obtenir_ou_creer_employe('samir_ops')
    emp7 = obtenir_ou_creer_employe('ghita_design')
    emp8 = obtenir_ou_creer_employe('mehdi_finance')
    emp9 = obtenir_ou_creer_employe('anass_cyber')
    emp10 = obtenir_ou_creer_employe('keltoum_mkt')
    emp11 = obtenir_ou_creer_employe('omar_infra')
    emp12 = obtenir_ou_creer_employe('chaima_qa')
    emp13 = obtenir_ou_creer_employe('marouane_support')
    emp14 = obtenir_ou_creer_employe('imane_legal')
    emp15 = obtenir_ou_creer_employe('tarik_bi')

    print("\n🛠️ ÉTAPE 3 : Injection des 15 réclamations dans la table Reclamation...")

    # Liste des données adaptées aux CHOICES du modèle : (user, titre, desc, statut_modèle, priorite_modèle)
    tickets = [
        (emp1, "Panne totale du WiFi au guichet",
         "Impossible de se connecter au réseau depuis ce morning, le travail est bloqué.", 'En attente', 'Haute'),
        (emp2, "Erreur sur la fiche de paie de Mai",
         "Il manque la prime de déplacement sur mon virement de ce mois-ci.", 'En cours', 'Moyenne'),
        (emp3, "Écran Dell XPS fissuré et tactile HS",
         "Mon écran est complètement cassé suite à un choc. L'affichage scintille et le tactile fait des clics fantômes, c'est impossible de bosser, c'est super urgent !",
         'En attente', 'Haute'),
        (emp4, "Demande d'aide configuration VPN",
         "Bonjour, j'ai une simple question concernant les identifiants d'accès au VPN pour le télétravail. Est-ce qu'on peut m'aider ou m'aiguiller ?",
         'En attente', 'Basse'),
        (emp5, "Problème d'accès à l'application d'évaluation",
         "Mon compte refuse de se connecter à la plateforme d'évaluation en ligne. J'ai un souci de mot de passe invalide visiblement, c'est embêtant.",
         'En cours', 'Moyenne'),
        (emp6, "Panne totale de la base de données Oracle",
         "Alerte crise ! Plus aucune requête PL/SQL ne passe sur le serveur de prod. Tout est bloqué, erreur 500 en boucle sur l'application !",
         'En attente', 'Haute'),
        (emp7, "Connexion réseau internet extrêmement lente",
         "Le réseau au 3ème étage est vraiment très lent aujourd'hui. Les pages mettent 3 minutes à charger, ça crée un gros retard dans mes livraisons et c'est un problème pour mon travail.",
         'En cours', 'Moyenne'),
        (emp8, "Badge d'accès aux bureaux désactivé à Rabat",
         "Mon badge ne fonctionne plus ce matin à l'entrée du bâtiment de Rabat. Je suis coincé dehors, aidez-moi rapidement s'il vous plaît !",
         'En attente', 'Haute'),
        (emp9, "Suspicion de Phishing / Email suspect",
         "J'ai reçu un email bizarre me demandant mes accès de connexion. Je préfère le signaler pour vérification, pas d'urgence mais doute sérieux.",
         'En attente', 'Basse'),
        (emp10, "Demande d'attestation de travail",
         "Bonjour l'équipe RH, j'ai besoin d'une attestation de travail assez rapidement pour un dossier administratif personnel. Merci pour votre aide.",
         'En attente', 'Basse'),
        (emp11, "Climatisation en panne salle des serveurs",
         "La température monte très vite dans la baie réseau de Rabat. Risque de surchauffe matériel critique si on n'intervient pas !",
         'En attente', 'Haute'),
        (emp12, "Licence logicielle PyCharm expirée",
         "Mon IDE m'indique que la licence d'entreprise a expiré aujourd'hui. Impossible de compiler mon code proprement.",
         'En cours', 'Moyenne'),
        (emp13, "Remplacement de souris et clavier défectueux",
         "La molette de ma souris ne répond plus du tout. Est-il possible de passer au stock informatique pour un échange standard ?",
         'Resolue', 'Basse'),
        (emp14, "Modification de la mutuelle d'entreprise",
         "Je souhaite ajouter un membre de ma famille à ma couverture médicale. Quelle est la procédure ou les papiers à fournir ?",
         'Resolue', 'Basse'),
        (emp15, "Rapport PowerBI qui ne s'actualise plus",
         "Les données de ventes restent bloquées sur les chiffres de la semaine dernière. Ça fausse nos analyses hebdomadaires, problème persistant.",
         'En attente', 'Moyenne'),
    ]

    for user, title, desc, status, priority in tickets:
        # Nettoyage des anciens tests au cas où pour repartir sur une base propre
        Reclamation.objects.filter(titre=title, client_nom=user.username).delete()

        # Insertion finale avec les vrais champs de agent/models.py
        Reclamation.objects.create(
            client_nom=user.username,
            titre=title,
            description=desc,
            statut=status,
            priorite=priority
        )
        print(f"   [+] Réclamation synchronisée : [{status.upper()}] - '{title}'")

    print("\n🎉 [SUCCESS] Base de données officiellement mise à jour avec le modèle de l'application 'agent' !")


if __name__ == '__main__':
    insert_problemes()