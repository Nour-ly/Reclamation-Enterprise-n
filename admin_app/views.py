from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from .models import Category
from .models import Complaint


# Create your views here.

def add_user(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        # FIX : On vérifie si l'utilisateur existe déjà pour éviter le Duplicate entry sur le username
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # Optionnel : on met à jour son mot de passe si tu veux
            user.set_password(password)
            user.save()
        else:
            # S'il n'existe pas, on le crée normalement
            user = User.objects.create_user(
                username=username,
                password=password
            )

        # On évite l'IntegrityError sur le profil
        Profile.objects.update_or_create(
            user=user,
            defaults={'role': role}
        )

        # modifier le rôle !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        user.profile.role = role
        user.profile.save()

    return render(request, 'admin_app/add_user.html')


def users_list(request):
    users = User.objects.all()
    return render(request, 'admin_app/users_list.html', {'users': users})


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('users_list')


def agents_list(request):
    agents = Profile.objects.filter(role='agent')
    return render(request, 'admin_app/agents_list.html', {'agents': agents})


def employees_list(request):
    employees = Profile.objects.filter(role='employee')
    return render(request, 'admin_app/employees_list.html', {'employees': employees})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin_app/category_list.html', {'categories': categories})


def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        return redirect('category_list')

    return render(request, 'admin_app/add_category.html')


def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('category_list')


def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == "POST":
        category.name = request.POST['name']
        category.save()
        return redirect('category_list')

    return render(request, 'admin_app/edit_category.html', {'category': category})


def reclamation_list(request):
    reclamations = Complaint.objects.all()
    return render(request, 'admin_app/reclamation_list.html', {
        'reclamations': reclamations
    })


def add_reclamation(request):
    users = User.objects.all()
    categories = Category.objects.all()

    if request.method == "POST":
        Complaint.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            employee_id=request.POST['user'],
            category_id=request.POST['category']
        )
        return redirect('reclamation_list')

    return render(request, 'admin_app/add_reclamation.html', {
        'users': users,
        'categories': categories
    })


def edit_reclamation(request, rec_id):
    rec = Complaint.objects.get(id=rec_id)
    users = User.objects.all()
    categories = Category.objects.all()

    if request.method == "POST":
        rec.title = request.POST['title']
        rec.description = request.POST['description']
        rec.status = request.POST['status']
        rec.priority = request.POST['priority']
        rec.employee_id = request.POST['user']
        rec.category_id = request.POST['category']
        rec.save()
        return redirect('reclamation_list')

    return render(request, 'admin_app/edit_reclamation.html', {
        'rec': rec,
        'users': users,
        'categories': categories
    })


def delete_reclamation(request, rec_id):
    rec = Complaint.objects.get(id=rec_id)
    rec.delete()
    return redirect('reclamation_list')


from django.shortcuts import render
# 1. IMPORTANT : On importe le bon modèle "Reclamation" depuis l'application agent
from agent.models import Reclamation


def dashboard(request):
    # TOTAL (Interroge la table Reclamation)
    total = Reclamation.objects.count()

    # STATUS (On utilise 'statut' et les choix exacts du modèle : 'En attente', 'En cours', 'Resolue', 'Rejetee')
    nouvelle = Reclamation.objects.filter(statut='En attente').count()
    en_cours = Reclamation.objects.filter(statut='En cours').count()
    resolue = Reclamation.objects.filter(statut='Resolue').count()
    rejetee = Reclamation.objects.filter(statut='Rejetee').count()

    # PRIORITY (On utilise 'priorite' et les choix exacts du modèle : 'Basse', 'Moyenne', 'Haute')
    faible = Reclamation.objects.filter(priorite='Basse').count()
    moyenne = Reclamation.objects.filter(priorite='Moyenne').count()
    urgente = Reclamation.objects.filter(priorite='Haute').count()

    context = {
        'total': total,

        'nouvelle': nouvelle,
        'en_cours': en_cours,
        'resolue': resolue,
        'rejetee': rejetee,

        'faible': faible,
        'moyenne': moyenne,
        'urgente': urgente,
    }

    return render(request, 'admin_app/dashboard.html', context)