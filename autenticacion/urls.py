from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Esta linea redirige a la vista index de la aplicacion agenda
    path('', auth_views.LoginView.as_view(template_name='autenticacion/login.html'), name='login'), 
]