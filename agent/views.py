from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employee.models import Complaint  # On utilise le bon modèle ici


# 1. Dashboard de l'agent
@login_required(login_url='/login/')
def agent_dashboard(request):
    # Sécurité : vérifier si c'est bien un agent
    if not request.user.groups.filter(name='Agent').exists():
        messages.error(request, "Accès refusé.")
        return redirect('employee_dashboard')

    # Au lieu d'une chaîne fixe, on prend le vrai nom de l'utilisateur connecté !
    nom_agent = request.user.username

    # Réclamations globales en attente (statut 'new')
    reclamations_dispo = Complaint.objects.filter(status='new').order_by('-created_at')

    # Réclamations en cours de traitement (statut 'in_progress')
    mes_reclamations = Complaint.objects.filter(status='in_progress').order_by('-updated_at')

    # Réclamations résolues (statut 'resolved') pour l'historique/traçabilité
    historique = Complaint.objects.filter(status='resolved').order_by('-updated_at')[:15]

    return render(request, 'agent/dashboard.html', {
        'mes_reclamations': mes_reclamations,
        'reclamations_dispo': reclamations_dispo,
        'historique': historique,
        'nom_agent': nom_agent
    })


# 2. Prendre en charge une réclamation (Passer de 'new' à 'in_progress')
@login_required(login_url='/login/')
def s_attribuer_reclamation(request, id):
    if not request.user.groups.filter(name='Agent').exists():
        return redirect('employee_dashboard')

    reclamation = get_object_or_404(Complaint, id=id)
    reclamation.status = 'in_progress'
    reclamation.save()

    messages.success(request, f"La réclamation #{id} vous a été attribuée.")
    return redirect('/agent/')


# 3. Traiter, Répondre et passer en 'resolved'
@login_required(login_url='/login/')
def traiter_reclamation(request, id):
    if not request.user.groups.filter(name='Agent').exists():
        return redirect('employee_dashboard')

    complaint = get_object_or_404(Complaint, id=id)

    if request.method == 'POST':
        # Correction ici : on récupère 'statut' car c'est le name dans ton HTML
        nouveau_statut = request.POST.get('statut')

        if nouveau_statut in ['new', 'in_progress', 'resolved']:
            complaint.status = nouveau_statut
            complaint.save()
            messages.success(request, f"La réclamation #{id} a bien été mise à jour.")
            return redirect('/agent/')
        else:
            messages.error(request, "Statut invalide.")

    return render(request, 'agent/traiter_reclamation.html', {'complaint': complaint})