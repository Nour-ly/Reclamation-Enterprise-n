from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from employee import views as employee_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', employee_views.user_login, name='login'),
    path('signup/', employee_views.user_signup, name='signup'),
    path('logout/', employee_views.user_logout, name='logout'),

    # Tes applications existantes
    path('employee/', include('employee.urls')),
    path('agent/', include('agent.urls')),

    # --- INCLUSION DE LA PARTIE DE TA COPINE (ADMIN_APP) ---
    # On laisse les chemins vides '' pour que ses URLs s'écrivent directement
    # comme elle l'a codé (ex: /dashboard/, /users/, /categories/)
    path('', include('admin_app.urls')),

    # La racine redirige automatiquement vers la page de login unique
    path('', lambda request: redirect('login')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)