from django.urls import path
from . import views

urlpatterns = [
    # Esta linea redirige a la vista index de la aplicacion agenda
    path('', views.index, name='index'), 
]