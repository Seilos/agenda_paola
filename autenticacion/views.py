from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from .form import RegistroUsuarioForm
from agenda.models import Ambulatorio, Profesor

User = get_user_model()


# ─── Vista de Login Personalizada ────────────────────────────────────────────
def login_view(request):
    """
    Vista de inicio de sesión personalizada.
    - Si el usuario ya está autenticado, lo redirige según su rol.
    - Si las credenciales son correctas pero el usuario está inactivo,
      muestra un mensaje indicando que está pendiente de activación.
    - Después de autenticar, redirige al superusuario al panel admin
      y al resto al panel personalizado (agenda:index).
    """
    # Si ya inició sesión, redirigir según el rol
    if request.user.is_authenticated:
        return _redirigir_segun_rol(request.user)

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        # Primero verificamos si el usuario existe y está inactivo
        try:
            user_obj = User.objects.get(username=username)
            if not user_obj.is_active:
                messages.error(
                    request,
                    "Tu cuenta está pendiente de activación. "
                    "Comunícate con tu profesor."
                )
                return render(request, "autenticacion/login.html")
        except User.DoesNotExist:
            pass

        # Intentar autenticar
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return _redirigir_segun_rol(user)
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "autenticacion/login.html")


def _redirigir_segun_rol(user):
    """Redirige al usuario según su rol tras iniciar sesión."""
    if user.is_superuser:
        return redirect('/admin/')
    return redirect('agenda:index')


# ─── Vista de Registro ────────────────────────────────────────────────────────
def registro_estudiante(request):
    """Vista de registro de nuevos estudiantes."""
    
    if request.user.is_authenticated:
        return _redirigir_segun_rol(request.user)

    # Consultamos los ambulatorios una sola vez arriba
    ambulatorios = Ambulatorio.objects.all().order_by('nombre')
    profesores = Profesor.objects.all().order_by('nombre_completo')

    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Aquí capturaremos el ID del select usando request.POST.get('ambulatorio')
            # para crear el registro correspondiente en el modelo Estudiante.
            
            messages.success(request, "Registro exitoso. Notifica al profesor para activación.")
            return redirect('login')
    else:
        form = RegistroUsuarioForm()

    #  Unificamos todo en un único diccionario de contexto antes de renderizar
    context = {
        'form': form,
        'ambulatorios': ambulatorios,
        'profesores': profesores
    }
        
    # De esta manera, tanto si es GET como si es un POST que falló la validación,
    # la plantilla siempre recibirá la lista de los 75 ambulatorios para el select.
    return render(request, "autenticacion/registro.html", context)