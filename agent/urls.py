from django.urls import path
from . import views

urlpatterns = [
    # Route pour afficher le dashboard principal de l'agent
    path('', views.agent_dashboard, name='agent_dashboard'),

    # Route pour attribuer la réclamation (le bouton vert Prendre en charge)
    path('complaint/prendre/<int:id>/', views.s_attribuer_reclamation, name='s_attribuer_reclamation'),

    # Route pour la page de traitement et la soumission du formulaire (bouton bleu)
    path('complaint/traiter/<int:id>/', views.traiter_reclamation, name='traiter_reclamation'),
]