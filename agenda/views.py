from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    """Funcion que renderiza la vista index de la aplicacion agenda
    Args:
        request: Objeto HttpRequest
    Returns:
        HttpResponse: Objeto HttpResponse
    """
    return render(request, 'agenda/index.html')
    