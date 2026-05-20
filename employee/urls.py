from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='employee_dashboard'),
    path('complaint/submit/', views.submit_complaint, name='submit_complaint'),
    path('complaint/track/<int:complaint_id>/', views.track_complaint, name='track_complaint'),

    # --- LES DEUX ROUTES POUR TON ESPACE AGENT ---
    path('agent/', views.agent_dashboard, name='agent_dashboard'),
    path('complaint/traiter/<int:complaint_id>/', views.traiter_reclamation, name='traiter_reclamation'),
]