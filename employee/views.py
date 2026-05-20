from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User

# IMPORTANT : On importe le VRAI modèle "Reclamation" depuis l'application agent
from agent.models import Reclamation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint as Reclamation # Import de ton modèle Reclamation

def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        elif request.user.groups.filter(name='Agent').exists():
            return redirect('/agent/')
        else:
            return redirect('employee_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('dashboard')
            elif user.groups.filter(name='Agent').exists():
                return redirect('/agent/')
            else:
                return redirect('employee_dashboard')
        else:
            return render(request, 'employee/login.html', {'error': 'Identifiant ou mot de passe incorrect.'})

    return render(request, 'employee/login.html')


def user_signup(request):
    if request.user.is_authenticated:
        return redirect('employee_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'employee/signup.html', {'error': 'Passwords do not match.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'employee/signup.html', {'error': 'Username already exists.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('employee_dashboard')

    return render(request, 'employee/signup.html')


def user_logout(request):
    logout(request)
    return redirect('/login/')


# =====================================================================
#  L'ESPACE DASHBOARD EMPLOYÉ CORRIGÉ (FINI LES 0 !)
# =====================================================================
@login_required(login_url='/login/')
@login_required(login_url='/login/')
def dashboard(request):
    """Employee dashboard - montre ses réclamations avec les vraies stats"""

    # ON FILTRE SUR LE BON CHAMP DE BDD (employee) MAIS ON GARDE TON CODE EXACT
    complaints = Reclamation.objects.filter(employee=request.user).order_by('-created_at')

    # On calcule les statistiques en s'adaptant aux statuts réels
    total = complaints.count()
    new_count = complaints.filter(status='new').count()
    in_progress_count = complaints.filter(status='in_progress').count()
    resolved_count = complaints.filter(status='resolved').count()

    # On recrée les faux attributs à la volée pour que ton HTML d'origine ne plante pas
    for c in complaints:
        c.client_nom = request.user.username
        c.titre = c.title
        c.priorite = getattr(c, 'priority', 'Moyenne')
        c.date_creation = c.created_at
        # Traduction pour tes badges HTML existants
        if c.status == 'new':
            c.statut = 'En attente'
        elif c.status == 'in_progress':
            c.statut = 'En cours'
        elif c.status == 'resolved':
            c.statut = 'Resolue'
        else:
            c.statut = 'Rejetee'
        c.reponse_agent = getattr(c, 'agent_response', '')

    context = {
        'complaints': complaints,
        'total_count': total,
        'new_count': new_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
    }
    return render(request, 'employee/dashboard.html', context)


# =====================================================================
#  LES AUTRES FONCTIONS ADAPTÉES AU MODÈLE RECLAMATION
# =====================================================================
@login_required(login_url='/login/')
def traiter_reclamation(request, complaint_id):
    if not request.user.groups.filter(name='Agent').exists():
        messages.error(request, "Accès refusé.")
        return redirect('employee_dashboard')

    complaint = get_object_or_404(Reclamation, id=complaint_id)

    if request.method == 'POST':
        nouveau_statut = request.POST.get('status')  # Garde le name HTML du formulaire
        if nouveau_statut in ['En attente', 'En cours', 'Resolue', 'Rejetee']:
            complaint.statut = nouveau_statut
            complaint.save()
            messages.success(request, f"La réclamation #{complaint.id} a été mise à jour.")
            return redirect('/agent/')
        else:
            messages.error(request, "Statut invalide.")

    return render(request, 'agent/traiter_reclamation.html', {'complaint': complaint})


@login_required(login_url='/login/')
def agent_dashboard(request):
    if not request.user.groups.filter(name='Agent').exists():
        return redirect('employee_dashboard')

    # On récupère TOUTES les réclamations de la bonne table
    all_reclamations = Reclamation.objects.all().order_by('-date_creation')

    # Tri automatique selon le statut exact enregistré par ton script de seeding
    reclamations_dispo = all_reclamations.filter(statut='En attente')
    mes_reclamations = all_reclamations.filter(statut='En cours')
    historique = all_reclamations.filter(statut='Resolue')

    context = {
        'reclamations_dispo': reclamations_dispo,
        'mes_reclamations': mes_reclamations,
        'historique': historique,
    }

    return render(request, 'agent/dashboard.html', context)


@login_required(login_url='/login/')
def submit_complaint(request):
    """Formulaire de soumission d'une nouvelle réclamation"""

    # 1. Si l'employé valide le formulaire (méthode POST)
    if request.method == 'POST':
        category_id = request.POST.get('category')

        # CORRECTION : On a complètement retiré la ligne priority pour éviter le TypeError
        Reclamation.objects.create(
            employee=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            status='new',
            category_id=category_id if category_id and category_id.strip() else None
        )
        messages.success(request, 'Votre réclamation a été soumise avec succès !')
        return redirect('employee_dashboard')

    # 2. Si l'employé affiche juste la page (méthode GET)
    try:
        from admin_app.models import Category
        categories = Category.objects.all()
    except ImportError:
        try:
            from employee.models import Category
            categories = Category.objects.all()
        except ImportError:
            categories = []

    context = {
        'categories': categories
    }
    return render(request, 'employee/submit.html', context)


@login_required(login_url='/login/')
def track_complaint(request, complaint_id):
    """Suivi d'une réclamation spécifique"""
    complaint = get_object_or_404(Reclamation, id=complaint_id, client_nom=request.user.username)
    return render(request, 'employee/track.html', {'complaint': complaint})