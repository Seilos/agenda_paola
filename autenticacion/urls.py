from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Esta linea redirige a la vista index de la aplicacion agenda
    path('', auth_views.LoginView.as_view(template_name='autenticacion/login.html', redirect_authenticated_user=True), name='login'),
    path('registro/', views.registro_estudiante, name='registro'),
]