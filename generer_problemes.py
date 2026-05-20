import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employeeproject.settings')
django.setup()

from django.contrib.auth.models import User, Group
from employee.models import Complaint, Category

def insert_problemes():
    print("⏳ Insertion des catégories et des utilisateurs...")

    group_agent, _ = Group.objects.get_or_create(name='Agent')
    group_employee, _ = Group.objects.get_or_create(name='Employee')

    # Création de ton compte Agent pour la connexion future
    if not User.objects.filter(username='MonAgent').exists():
        mon_agent = User.objects.create_user(username='MonAgent', password='password123')
        mon_agent.groups.add(group_agent)
        print("✅ Agent 'MonAgent' créé.")

    # Création des employés de test
    def obtenir_ou_creer_employe(nom):
        if User.objects.filter(username=nom).exists():
            return User.objects.get(username=nom)
        else:
            nouvel_emp = User.objects.create_user(username=nom, password='password123')
            nouvel_emp.groups.add(group_employee)
            print(f"✅ Employé '{nom}' créé.")
            return nouvel_emp

    sami = obtenir_ou_creer_employe('sami_dev')
    leila = obtenir_ou_creer_employe('leila_rh')

    # Création des catégories
    cat_tech, _ = Category.objects.get_or_create(name="Technique")
    cat_rh, _ = Category.objects.get_or_create(name="Ressources Humaines")

    print("🛠️ Injection des réclamations propres...")

    # Réclamation 1 - Nouveau problème pour le flux
    Complaint.objects.get_or_create(
        title="Panne totale du WiFi au guichet",
        description="Impossible de se connecter au réseau depuis ce matin, le travail est bloqué.",
        category=cat_tech,
        employee=sami,
        status='new'
    )

    # Réclamation 2 - Autre cas de test
    Complaint.objects.get_or_create(
        title="Erreur sur la fiche de paie de Mai",
        description="Il manque la prime de déplacement sur mon virement de ce mois-ci.",
        category=cat_rh,
        employee=leila,
        status='in_progress'
    )

    print("🎉 Base de données peuplée avec succès !")

if __name__ == '__main__':
    insert_problemes()