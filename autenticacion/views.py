from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .form import RegistroUsuarioForm

# Crear la vista de registro

def registro_estudiante(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Notifica al profesor para activación.")
            return redirect('login')
    else:
        # Aquí definimos la variable form para las peticiones GET
        form = RegistroUsuarioForm()
        
    # Esta línea queda fuera del if/else.
    # Si es GET, renderiza el form vacío.
    # Si es POST y falló la validación, renderiza el form con los errores y datos ingresados.
    return render(request, "autenticacion/registro.html", {'form': form})
