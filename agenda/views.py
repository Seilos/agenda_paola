from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from auditlog.models import LogEntry
from .models import Usuario


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
    
@login_required
def cerrar_sesion(request):
    """Funcion que cierra la sesion del usuario
    Args:
        request: Objeto HttpRequest
    Returns:
        HttpResponse: Redirige al usuario a la vista de inicio de sesion
    """
    # Ejecutamos la funcion logout para cerrar la sesion del usuario
    logout(request)

    # Redirigimos al usuario a la vista de inicio de sesion
    return redirect('login')


from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta

@login_required
def actividad(request):
    """Vista que muestra el log de actividad del sistema.
    Solo accesible para profesores y administradores.
    Soporta filtros por fecha (rango máx. 6 meses) y paginación de 50 elementos.
    """
    # Solo profesores y superusuarios pueden ver la actividad
    if not (request.user.rol == 'PROFESOR' or request.user.is_superuser):
        return redirect('agenda:index')

    ahora = timezone.localtime(timezone.now())
    
    # Obtener fechas desde la petición GET o usar valores por defecto (último mes)
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    
    error_mensaje = None

    # Valores por defecto (últimos 30 días)
    fecha_fin = ahora
    fecha_inicio = ahora - timedelta(days=30)

    try:
        if fecha_inicio_str:
            # Parsear la fecha del input (YYYY-MM-DD) y asignarle la hora de inicio del día (00:00:00)
            fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        if fecha_fin_str:
            # Parsear la fecha del input y asignarle la hora de fin del día (23:59:59)
            fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str + " 23:59:59", '%Y-%m-%d %H:%M:%S'))
            
        # Validación de rango máximo: 6 meses (aprox 183 días)
        if (fecha_fin - fecha_inicio).days > 183:
            error_mensaje = "El rango máximo de consulta no puede superar los 6 meses."
            # Volver a los últimos 30 días si hay error
            fecha_fin = ahora
            fecha_inicio = ahora - timedelta(days=30)
    except ValueError:
        error_mensaje = "Formato de fechas incorrecto."

    # Consultar logs en base al rango de fechas filtrado
    logs_queryset = LogEntry.objects.filter(
        timestamp__range=(fecha_inicio, fecha_fin)
    ).select_related('actor', 'content_type').order_by('-timestamp')

    # Configurar Paginación (50 registros por página)
    paginator = Paginator(logs_queryset, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Formatear fechas para los valores por defecto del input HTML
    fecha_inicio_input = fecha_inicio.strftime('%Y-%m-%d')
    fecha_fin_input = fecha_fin.strftime('%Y-%m-%d')

    context = {
        'logs': page_obj,  # El objeto paginado que contiene los registros de la página actual
        'fecha_inicio': fecha_inicio_input,
        'fecha_fin': fecha_fin_input,
        'error_mensaje': error_mensaje
    }

    return render(request, 'agenda/actividad.html', context)


@login_required
def gestion_usuarios(request):
    """Vista para administrar usuarios, accesible solo para Profesores y Administradores.
    Muestra los usuarios ordenados en dos grupos (activos/todos y pendientes de activación).
    Soporta búsquedas a través del parámetro 'q'.
    """
    if not (request.user.rol == 'PROFESOR' or request.user.is_superuser):
        return redirect('agenda:index')

    tab = request.GET.get('tab', 'pendientes') # Por defecto muestra la pestaña de pendientes
    q = request.GET.get('q', '').strip()
    
    # Obtener usuarios según la pestaña seleccionada
    if tab == 'todos':
        # Todos los usuarios registrados
        usuarios_list = Usuario.objects.all().order_by('-date_joined')
    else:
        # Usuarios pendientes de activación (is_active=False y recien_registrado=True)
        usuarios_list = Usuario.objects.filter(is_active=False, recien_registrado=True).order_by('-date_joined')

    # Filtrado por búsqueda si se especificó el parámetro 'q'
    if q:
        from django.db.models import Q
        usuarios_list = usuarios_list.filter(
            Q(username__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )

    # Paginación de 50 en 50
    paginator = Paginator(usuarios_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'usuarios': page_obj,
        'tab': tab,
        'q': q,
    }
    return render(request, 'agenda/usuarios.html', context)


@login_required
def cambiar_estado_usuario(request, usuario_id):
    """Permite a los profesores/administradores activar o desactivar un usuario.
    """
    if not (request.user.rol == 'PROFESOR' or request.user.is_superuser):
        return redirect('agenda:index')
        
    if request.method == "POST":
        # Evitar desactivarse a uno mismo
        if request.user.id == usuario_id:
            return redirect('agenda:gestion_usuarios')
            
        usuario = Usuario.objects.get(id=usuario_id)
        # Invertir el estado de activación
        usuario.is_active = not usuario.is_active
        if usuario.is_active:
            # Una vez activado, deja de ser recién registrado para siempre
            usuario.recien_registrado = False
        usuario.save()
        
        # Redirigir a la pestaña correspondiente, conservando la búsqueda si aplica
        tab_origen = request.POST.get('tab_origen', 'pendientes')
        q = request.POST.get('q', '')
        url = f"/agenda/usuarios/?tab={tab_origen}"
        if q:
            from django.utils.http import urlencode
            url += "&" + urlencode({'q': q})
        return redirect(url)
        
    return redirect('agenda:gestion_usuarios')


from django.http import JsonResponse

@login_required
def buscar_usuarios_ajax(request):
    """Endpoint AJAX para el autocompletado en tiempo real de búsqueda de usuarios.
    """
    if not (request.user.rol == 'PROFESOR' or request.user.is_superuser):
        return JsonResponse({'error': 'No autorizado'}, status=403)
        
    tab = request.GET.get('tab', 'pendientes')
    q = request.GET.get('q', '').strip()
    
    if not q:
        return JsonResponse({'usuarios': []})
        
    # Aplicamos el mismo filtro base de la pestaña activa
    if tab == 'todos':
        usuarios_qs = Usuario.objects.all()
    else:
        usuarios_qs = Usuario.objects.filter(is_active=False, recien_registrado=True)
        
    from django.db.models import Q
    usuarios_qs = usuarios_qs.filter(
        Q(username__icontains=q) |
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q)
    ).order_by('-date_joined')[:10]  # Limitar a 10 resultados para el dropdown
    
    resultados = []
    for u in usuarios_qs:
        resultados.append({
            'id': u.id,
            'username': u.username,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'rol_display': u.obtener_rol_display,
            'is_active': u.is_active,
        })
        
    return JsonResponse({'usuarios': resultados})


# consultas crud
def consulta_crud(request):
    return render(request, 'agenda/consulta_crud.html')
