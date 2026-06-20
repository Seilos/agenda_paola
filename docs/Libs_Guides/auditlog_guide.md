# Guía de django-auditlog: Registro de Actividad y Auditoría

Esta guía explica el funcionamiento de la librería `django-auditlog` implementada en el proyecto **Agenda Paola**, detallando cómo registra la actividad del sistema y cómo expandir su cobertura a medida que se agreguen nuevas funcionalidades y modelos.

---

## 1. ¿Cómo funciona `django-auditlog`?

`django-auditlog` es una aplicación de Django que realiza un seguimiento automático de las mutaciones de la base de datos (creaciones, modificaciones y eliminaciones).

### Flujo de Captura de Actividad
1. **Señales de Django (`django.db.models.signals`)**: La librería se conecta a las señales `post_save` y `post_delete` de los modelos registrados.
2. **Captura del Usuario Activo (Middleware)**: Registramos `auditlog.middleware.AuditlogMiddleware` en `settings.py`. Este intercepta cada solicitud HTTP y asocia el usuario autenticado (`request.user`) con cualquier cambio de base de datos que ocurra durante dicha solicitud.
3. **Escritura del Log**: Cada cambio escribe un registro en la tabla `auditlog_logentry` que almacena:
   - **Actor**: Quién realizó el cambio.
   - **Acción**: Si fue creación (`CREATE`), modificación (`UPDATE`) o eliminación (`DELETE`).
   - **Objeto**: El elemento modificado y su ID.
   - **Fecha/Hora**: Timestamp del evento.
   - **Cambios**: Formato JSON que contiene el estado anterior y el nuevo valor del campo modificado.

---

## 2. Modelos Registrados Actualmente

En el archivo [admin.py](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda/admin.py) se han registrado los modelos centrales:

```python
from auditlog.registry import auditlog
from .models import Usuario, Paciente, Consultas

auditlog.register(Usuario)
auditlog.register(Paciente)
auditlog.register(Consultas)
```

Cualquier cambio realizado a estos modelos mediante formularios del frontend o desde el panel Django Admin quedará registrado.

---

## 3. ¿Cómo registrar un Nuevo Modelo en el Log?

Si en el futuro agregas un modelo nuevo (por ejemplo: `Tratamiento`), sigue estos pasos para auditarlo:

1. Abre el archivo [admin.py](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda/admin.py).
2. Importa el nuevo modelo.
3. Agrégalo al registro de `auditlog`:

```python
# c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda/admin.py
from .models import Usuario, Paciente, Consultas, Tratamiento  # 1. Importar

auditlog.register(Tratamiento)  # 2. Registrar
```

A partir de ese instante, cualquier creación, edición o eliminación de un `Tratamiento` quedará registrada automáticamente.

---

## 4. Personalizar el Registro por Modelo

Si deseas limitar qué campos se auditan o excluir campos sensibles (como contraseñas o tokens), puedes pasar parámetros al método `register`:

### Excluir campos específicos
```python
# No registrará cambios sobre el campo 'contrasenia' ni 'token_sesion'
auditlog.register(Usuario, exclude=['contrasenia', 'token_sesion'])
```

### Incluir únicamente campos específicos
```python
# Solo registrará cambios si se modifican estos tres campos
auditlog.register(Consultas, fields=['diagnostico_final', 'calificacion', 'is_active'])
```

---

## 5. Registro de Eventos Manuales (No vinculados a Base de Datos)

Si necesitas registrar una acción que no sea guardar o borrar un registro (por ejemplo: *"Un profesor exportó un historial a Excel"* o *"Intento de inicio de sesión fallido"*), puedes instanciar manualmente una entrada de auditoría dentro de tus vistas (`views.py`):

```python
from auditlog.models import LogEntry
from django.contrib.contenttypes.models import ContentType

def exportar_datos_view(request):
    # ... Lógica de exportación de archivos ...

    # Registro manual en la bitácora
    LogEntry.objects.create(
        actor=request.user,
        action=LogEntry.Action.UPDATE,
        content_type=ContentType.objects.get_for_model(request.user),
        object_id=request.user.id,
        object_repr="Exportó historial médico a Excel",
        changes='{"accion": ["Generar Excel", "Completado"]}'
    )
    
    return response
```

---

## 6. Visualización de Logs en el Frontend

La vista [actividad](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda/views.py#L34-L49) consulta el modelo `LogEntry` e inyecta la información en la plantilla HTML:

```python
# Consulta en views.py
logs = LogEntry.objects.all().select_related('actor').order_by('-timestamp')[:100]
```

En la plantilla HTML ([actividad.html](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda/templates/agenda/actividad.html)), puedes acceder a:
- `{{ log.timestamp }}`: Fecha y hora.
- `{{ log.actor }}`: Usuario que lo hizo.
- `{{ log.get_action_display }}`: Representación textual de la acción (Creado, Modificado, etc.).
- `{{ log.object_repr }}`: Objeto sobre el que se actuó.
- `{{ log.changes }}`: (Opcional) Cadena JSON con los cambios detallados.
