from django.urls import path
from . import views

urlpatterns = [
    # Vista de inicio de sesión personalizada
    path('', views.login_view, name='login'),
    # Vista de registro de nuevos estudiantes/profesores
    path('registro/', views.registro_estudiante, name='registro'),
]