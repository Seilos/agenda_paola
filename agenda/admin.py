from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import format_html
from auditlog.registry import auditlog
from .models import Usuario, Paciente, Consultas

# Registrar modelos con auditlog para rastreo automático de cambios desde el frontend
auditlog.register(Usuario)
auditlog.register(Paciente)
auditlog.register(Consultas)


# ──────────────────────────────────────────────────────────────
# 1. USUARIO
# ──────────────────────────────────────────────────────────────
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Panel de administración para el modelo de Usuario personalizado.
    Hereda de UserAdmin para mantener el manejo seguro de contraseñas.
    """

    # Columnas visibles en la lista
    list_display = ('username', 'get_full_name', 'email', 'rol', 'obtener_rol_display', 'is_active', 'is_staff', 'date_joined')
    list_display_links = ('username',)

    # Filtros laterales
    list_filter = ('rol', 'is_active', 'is_staff', 'is_superuser')

    # Búsqueda por texto
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # Orden por defecto
    ordering = ('-date_joined',)

    # Campos editables directamente desde la lista (sin abrir el formulario)
    list_editable = ('is_active',)

    # Agregar el campo 'rol' al formulario heredado de UserAdmin
    fieldsets = UserAdmin.fieldsets + (
        ('Rol en la Agenda', {
            'fields': ('rol',),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol en la Agenda', {
            'fields': ('rol',),
        }),
    )


# ──────────────────────────────────────────────────────────────
# 2. PACIENTE
# ──────────────────────────────────────────────────────────────
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    """
    Panel de administración para el modelo Paciente.
    """

    list_display = ('nombre', 'is_active', 'is_deleted', 'created_at', 'created_by')
    list_display_links = ('nombre',)
    list_filter = ('is_active', 'is_deleted')
    search_fields = ('nombre',)
    ordering = ('-created_at',)
    list_editable = ('is_active',)
    readonly_fields = ('id', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')

    fieldsets = (
        ('Información del Paciente', {
            'fields': ('nombre',)
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted'),
        }),
        ('Auditoría (solo lectura)', {
            'classes': ('collapse',),
            'fields': ('id', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by'),
        }),
    )


# ──────────────────────────────────────────────────────────────
# 3. CONSULTAS
# ──────────────────────────────────────────────────────────────
@admin.register(Consultas)
class ConsultasAdmin(admin.ModelAdmin):
    """
    Panel de administración para el modelo Consultas.
    """

    list_display = ('__str__', 'estudiante_id', 'profesor_id', 'fecha_hora', 'calificacion', 'requiere_seguimiento', 'is_active', 'is_deleted')
    list_display_links = ('__str__',)
    list_filter = ('is_active', 'is_deleted', 'requiere_seguimiento', 'profesor_id')
    search_fields = ('nombre_id__nombre', 'estudiante_id__username', 'profesor_id__username')
    ordering = ('-fecha_hora',)
    date_hierarchy = 'fecha_hora'
    readonly_fields = ('id', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')

    fieldsets = (
        ('Consulta', {
            'fields': ('nombre_id', 'estudiante_id', 'profesor_id', 'fecha_hora')
        }),
        ('Diagnósticos', {
            'fields': ('diagnostico_estudiante', 'diagnostico_medico', 'diagnostico_final'),
        }),
        ('Seguimiento', {
            'fields': ('requiere_seguimiento', 'fecha_proxima_consulta', 'comentarios_previos'),
        }),
        ('Evaluación del Profesor', {
            'fields': ('calificacion', 'precicion_diagnostica', 'observaciones_evaluacion'),
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted'),
        }),
        ('Auditoría (solo lectura)', {
            'classes': ('collapse',),
            'fields': ('id', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by'),
        }),
    )


# ──────────────────────────────────────────────────────────────
# 4. LOG DE ACCIONES DEL SISTEMA (LogEntry)
# ──────────────────────────────────────────────────────────────
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    Muestra el historial completo de acciones realizadas en el panel admin.
    Solo lectura: ningún admin puede modificar ni borrar los logs del sistema.
    """

    # Íconos de acción según el tipo de operación
    ACCION_ICONO = {
        ADDITION: '✅ Creación',
        CHANGE:   '✏️ Edición',
        DELETION: '🗑️ Eliminación',
    }

    list_display = ('accion_icono', 'object_repr', 'content_type', 'user', 'action_time', 'change_message')
    list_filter = ('action_flag', 'content_type', 'user')
    search_fields = ('object_repr', 'user__username', 'change_message')
    ordering = ('-action_time',)
    date_hierarchy = 'action_time'

    # Todos los campos son de solo lectura
    readonly_fields = [field.name for field in LogEntry._meta.get_fields()]

    def accion_icono(self, obj):
        return self.ACCION_ICONO.get(obj.action_flag, '❓ Desconocido')
    accion_icono.short_description = 'Tipo de Acción'

    # Deshabilitar todos los permisos de escritura sobre los logs
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
