from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users_list, name='users_list'),
    path('add-user/', views.add_user, name='add_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('categories/', views.category_list, name='category_list'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('reclamations/', views.reclamation_list, name='reclamation_list'),
    path('add-reclamation/', views.add_reclamation, name='add_reclamation'),
    path('edit-reclamation/<int:rec_id>/', views.edit_reclamation, name='edit_reclamation'),
    path('delete-reclamation/<int:rec_id>/', views.delete_reclamation, name='delete_reclamation'),
    path('dashboard/', views.dashboard, name='dashboard'),
]