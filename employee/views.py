from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Complaint, Category, Response
from django.contrib.auth.models import User


def user_login(request):
    if request.user.is_authenticated:
        # Si l'utilisateur est déjà connecté, on le redirige selon son rôle
        if request.user.is_superuser:
            return redirect('dashboard')  # Redirige vers le dashboard Admin de ta copine
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

            # Tri automatique lors de la soumission du formulaire
            if user.is_superuser:
                return redirect('dashboard')  # Redirige vers le dashboard Admin de ta copine
            elif user.groups.filter(name='Agent').exists():
                return redirect('/agent/')  # Redirection vers ton espace Agent
            else:
                return redirect('employee_dashboard')  # Redirection vers l'espace de l'employé
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

        # Check passwords
        if password != confirm_password:
            return render(request, 'employee/signup.html', {
                'error': 'Passwords do not match.'
            })

        # Check username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'employee/signup.html', {
                'error': 'Username already exists.'
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Login automatically after signup
        login(request, user)

        return redirect('employee_dashboard')

    return render(request, 'employee/signup.html')

def user_logout(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def dashboard(request):
    """Employee dashboard - shows their complaints with stats"""
    complaints = Complaint.objects.filter(employee=request.user).order_by('-created_at')

    # Calculate statistics
    total = complaints.count()
    new_count = complaints.filter(status='new').count()
    in_progress_count = complaints.filter(status='in_progress').count()
    resolved_count = complaints.filter(status='resolved').count()

    context = {
        'complaints': complaints,
        'total_count': total,
        'new_count': new_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
    }
    return render(request, 'employee/dashboard.html', context)


# --- GARDE TA FONCTION TRAITER_RECLAMATION TELLE QUELLE ---
@login_required(login_url='/login/')
def traiter_reclamation(request, complaint_id):
    if not request.user.groups.filter(name='Agent').exists():
        messages.error(request, "Accès refusé.")
        return redirect('employee_dashboard')

    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        nouveau_statut = request.POST.get('status')
        if nouveau_statut in ['new', 'in_progress', 'resolved']:
            complaint.status = nouveau_statut
            complaint.save()
            messages.success(request, f"La réclamation {complaint.id} a été mise à jour.")
            return redirect('/agent/')
        else:
            messages.error(request, "Statut invalide.")

    return render(request, 'agent/traiter_reclamation.html', {'complaint': complaint})


# --- AJOUTE JUSTE CELLE-CI EN DESSOUS ---
@login_required(login_url='/login/')
def agent_dashboard(request):
    if not request.user.groups.filter(name='Agent').exists():
        return redirect('employee_dashboard')

    # On récupère toutes les réclamations pour ton affichage d'Agent
    complaints = Complaint.objects.all().order_by('-created_at')

    return render(request, 'agent/dashboard.html', {'complaints': complaints})

@login_required(login_url='/login/')
def submit_complaint(request):
    """Easy form to submit a complaint"""
    if request.method == 'POST':
        complaint = Complaint.objects.create(
            employee=request.user,
            category_id=request.POST.get('category') if request.POST.get('category') else None,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            attachment=request.FILES.get('attachment')
        )
        messages.success(request, 'Votre réclamation a été soumise avec succès!')
        return redirect('employee_dashboard')

    categories = Category.objects.all()
    return render(request, 'employee/submit.html', {'categories': categories})

@login_required(login_url='/login/')
def track_complaint(request, complaint_id):
    """Track a specific complaint"""
    complaint = get_object_or_404(Complaint, id=complaint_id, employee=request.user)
    return render(request, 'employee/track.html', {'complaint': complaint})