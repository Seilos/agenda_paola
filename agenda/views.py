from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    """Funcion que renderiza la vista index de la aplicacion agenda
    Args:
        request: Objeto HttpRequest
    Returns:
        HttpResponse: Objeto HttpResponse
    """
    return render(request, 'agenda/index.html')
    