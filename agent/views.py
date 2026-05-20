from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employee.models import Complaint  # Utilisation du bon modèle global
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employee.models import Complaint  # Utilisation du bon modèle global


# FONCTION D'ANALYSE DE SENTIMENT / FRUSTRATION AUTOMATIQUE
def analyser_frustration(description):
    texte = description.lower() if description else ""
    mots_critiques = ['bloqué', 'impossible', 'panne', 'urgent', 'erreur', 'crise', 'bloque', 'coincé', 'marche pas']
    mots_moderés = ['problème', 'souci', 'lent', 'retard', 'question', 'aide']

    score = 15  # Score de base

    for mot in mots_critiques:
        if mot in texte:
            score += 25
    for mot in mots_moderés:
        if mot in texte:
            score += 10

    score = min(score, 100)

    if score >= 65:
        statut_ia = "Critique 🚨"
        conseil = "Employé très frustré ou bloqué. Réponse immédiate et ton hautement professionnel requis."
        couleur = "#ef4444"
    elif score >= 35:
        statut_ia = "Modéré ⚠️"
        conseil = "Inconfort détecté. Apporter une réponse claire sous 24h."
        couleur = "#f59e0b"
    else:
        statut_ia = "Calme 🟢"
        conseil = "Demande standard. Ton neutre et informatif."
        couleur = "#10b981"

    return {'score': score, 'statut': statut_ia, 'conseil': conseil, 'couleur': couleur}


@login_required(login_url='/login/')
def agent_dashboard(request):
    if not request.user.groups.filter(name='Agent').exists():
        messages.error(request, "Accès refusé.")
        return redirect('employee_dashboard')

    nom_agent = request.user.username

    reclamations_dispo = Complaint.objects.filter(status='new').order_by('-created_at')
    mes_reclamations = Complaint.objects.filter(status='in_progress').order_by('-updated_at')
    en_attente_info = Complaint.objects.filter(status='pending').order_by('-updated_at')
    historique = Complaint.objects.filter(status='resolved').order_by('-updated_at')[:15]

    kpi_en_cours = mes_reclamations.count()
    kpi_attente = reclamations_dispo.count()
    kpi_resolues = Complaint.objects.filter(status='resolved').count()
    kpi_pending = en_attente_info.count()

    return render(request, 'agent/dashboard.html', {
        'mes_reclamations': mes_reclamations,
        'reclamations_dispo': reclamations_dispo,
        'en_attente_info': en_attente_info,
        'historique': historique,
        'nom_agent': nom_agent,
        'kpi_en_cours': kpi_en_cours,
        'kpi_attente': kpi_attente,
        'kpi_resolues': kpi_resolues,
        'kpi_pending': kpi_pending,
    })


@login_required(login_url='/login/')
def traiter_reclamation(request, id):
    if not request.user.groups.filter(name='Agent').exists():
        messages.error(request, "Accès refusé.")
        return redirect('employee_dashboard')

    complaint = get_object_or_404(Complaint, id=id)

    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')

        if nouveau_statut in ['new', 'in_progress', 'resolved', 'pending']:
            complaint.status = nouveau_statut
            complaint.save()

            if nouveau_statut == 'pending':
                messages.success(request, f"Le ticket #{id} a été mis en attente d'informations complémentaires.")
            else:
                messages.success(request, f"La réclamation #{id} a bien été mise à jour.")
            return redirect('agent_dashboard')
        else:
            messages.error(request, "Statut invalide.")

    analyse_ia = analyser_frustration(complaint.description)

    return render(request, 'agent/traiter_reclamation.html', {
        'complaint': complaint,
        'analyse_ia': analyse_ia
    })


@login_required(login_url='/login/')
def s_attribuer_reclamation(request, id):
    if not request.user.groups.filter(name='Agent').exists():
        messages.error(request, "Accès refusé.")
        return redirect('employee_dashboard')

    reclamation = get_object_or_404(Complaint, id=id)
    reclamation.status = 'in_progress'
    reclamation.save()

    messages.success(request, f"La réclamation #{id} a été passée en cours de traitement.")
    return redirect('agent_dashboard')