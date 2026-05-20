import os
import django

# On configure Django pour qu'il comprenne qu'on parle à ton projet
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employeeproject.settings')
django.setup()

from django.contrib.auth.models import User, Group

def insert_data():
    print("⏳ Insertion des utilisateurs dans le système...")

    # 1. On crée les rôles/groupes (indispensable pour ton système d'aiguillage)
    group_agent, _ = Group.objects.get_or_create(name='Agent')
    group_employee, _ = Group.objects.get_or_create(name='Employee')

    # 2. INSERT de TON compte Agent (pour te connecter sur ton dashboard)
    if not User.objects.filter(username='MonAgent').exists():
        agent = User.objects.create_user(username='MonAgent', password='password123', email='agent@test.com')
        agent.groups.add(group_agent)
        print("✅ INSERT : Agent 'MonAgent' est créé (MDP: password123).")

    # 3. INSERT de quelques utilisateurs "Employee" (pour simuler des clients/employés)
    utilisateurs_a_inserer = [
        {'username': 'sami_dev', 'email': 'sami@test.com'},
        {'username': 'leila_rh', 'email': 'leila@test.com'},
        {'username': 'omar_tech', 'email': 'omar@test.com'}
    ]

    for user_data in utilisateurs_a_inserer:
        if not User.objects.filter(username=user_data['username']).exists():
            new_user = User.objects.create_user(
                username=user_data['username'],
                password='password123',
                email=user_data['email']
            )
            new_user.groups.add(group_employee)
            print(f"✅ INSERT : Employé '{user_data['username']}' est injecté.")

    print("🎉 Tous les utilisateurs de test sont maintenant officiellement dans ta base !")

if __name__ == '__main__':
    insert_data()