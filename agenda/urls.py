from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    # Esta linea redirige a la vista index de la aplicacion agenda
    path('', views.index, name='index'), 
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('actividad/', views.actividad, name='actividad'),
    path('usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('usuarios/cambiar_estado/<int:usuario_id>/', views.cambiar_estado_usuario, name='cambiar_estado_usuario'),
]