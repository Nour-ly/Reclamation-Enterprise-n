from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employee.models import Complaint  # Utilisation du bon modèle global


# =====================================================================
# 1. DASHBOARD DE L'AGENT
# =====================================================================
@login_required(login_url='/login/')
def agent_dashboard(request):
    # Sécurité : vérifier si l'utilisateur connecté appartient au groupe 'Agent'
    if not request.user.groups.filter(name='Agent').exists():
        messages.error(request, "Accès refusé.")
        return redirect('employee_dashboard')

    # Récupère le username de l'agent connecté
    nom_agent = request.user.username

    # Réclamations globales en attente (statut 'new')
    reclamations_dispo = Complaint.objects.filter(status='new').order_by('-created_at')

    # Réclamations en cours de traitement (statut 'in_progress')
    mes_reclamations = Complaint.objects.filter(status='in_progress').order_by('-updated_at')

    # Historique des réclamations résolues (statut 'resolved') - Limité aux 15 dernières
    historique = Complaint.objects.filter(status='resolved').order_by('-updated_at')[:15]

    return render(request, 'agent/dashboard.html', {
        'mes_reclamations': mes_reclamations,
        'reclamations_dispo': reclamations_dispo,
        'historique': historique,
        'nom_agent': nom_agent
    })


# =====================================================================
# 2. PRENDRE EN CHARGE UNE RÉCLAMATION (Passer de 'new' à 'in_progress')
# =====================================================================
@login_required(login_url='/login/')
def s_attribuer_reclamation(request, id):
    if not request.user.groups.filter(name='Agent').exists():
        messages.error(request, "Accès refusé.")
        return redirect('employee_dashboard')

    reclamation = get_object_or_404(Complaint, id=id)
    reclamation.status = 'in_progress'
    reclamation.save()

    messages.success(request, f"La réclamation #{id} vous a été attribuée avec succès.")
    return redirect('agent_dashboard')  # Correction : Redirection via le nom de la route


# =====================================================================
# 3. TRAITER, RÉPONDRE ET PASSER LE STATUT EN 'RESOLVED'
# =====================================================================
@login_required(login_url='/login/')
def traiter_reclamation(request, id):
    if not request.user.groups.filter(name='Agent').exists():
        messages.error(request, "Accès refusé.")
        return redirect('employee_dashboard')

    complaint = get_object_or_404(Complaint, id=id)

    if request.method == 'POST':
        # Récupère la valeur du champ 'statut' envoyé par le formulaire HTML
        nouveau_statut = request.POST.get('statut')

        if nouveau_statut in ['new', 'in_progress', 'resolved']:
            complaint.status = nouveau_statut
            complaint.save()
            messages.success(request, f"La réclamation #{id} a bien été mise à jour.")
            return redirect('agent_dashboard')  # Correction : Redirection via le nom de la route
        else:
            messages.error(request, "Statut invalide.")

    return render(request, 'agent/traiter_reclamation.html', {'complaint': complaint})