# Evaluación de Arquitectura y Guía de Desacoplamiento

Esta guía analiza el estado actual del proyecto, el nivel de acoplamiento de sus componentes, y proporciona estrategias detalladas paso a paso para implementar mejores prácticas de desarrollo.

---

## 1. Estilos en Línea (Inline CSS) y Reutilización
### El Diagnóstico
En archivos como `usuarios.html` y `actividad.html`, las tablas y botones contienen estilos embebidos (ej. `<table style="width:100%; border-collapse: collapse; ...">`).
*   **Problema**: Dificulta el mantenimiento y viola el principio DRY (Don't Repeat Yourself). Si deseas cambiar el diseño visual, tendrás que editar múltiples archivos HTML uno por uno.

### Guía de Implementación
1.  **Definir Clases en el Archivo CSS Central (`index.css` o `tablas.css`)**:
    Identifica los estilos repetitivos y muévelos a clases reutilizables.
    ```css
    /* static/agenda/index.css */
    .dashboard-table-container {
        overflow-x: auto;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }

    .dashboard-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
        background: #ffffff;
        min-width: 800px;
    }

    .dashboard-table th {
        background: linear-gradient(90deg, #2c3e50, #1abc9c);
        color: white;
        padding: 14px 18px;
        text-align: left;
        font-weight: 600;
        font-size: 0.95rem;
    }

    .dashboard-table td {
        padding: 14px 18px;
        border-bottom: 1px solid #f0f2f5;
    }
    ```
2.  **Limpiar los HTMLs**:
    Sustituye los bloques complejos de `style="..."` por clases CSS limpias.
    ```html
    <!-- Antes -->
    <div style="overflow-x: auto; border-radius: 8px; ...">
        <table style="width:100%; border-collapse: collapse; ...">
            ...
        </table>
    </div>

    <!-- Después -->
    <div class="dashboard-table-container">
        <table class="dashboard-table">
            ...
        </table>
    </div>
    ```

---

## 2. Automatización del Helper de Botones (JavaScript Global)
### El Diagnóstico
Actualmente importas manualmente un script `form_helper.js` en cada página que tiene formularios para evitar el doble submit.
*   **Problema**: Es propenso a olvidos. Si un desarrollador crea una nueva interfaz y olvida importar el script, el formulario sufrirá el riesgo de submits duplicados.

### Guía de Implementación
1.  **Importar el JS de forma global**:
    Coloca la importación del script helper en la plantilla padre (`base.html`), justo antes del cierre de la etiqueta `</body>` o en el `<head>`.
    ```html
    <!-- agenda/templates/agenda/base.html -->
    <script src="{% static 'js/form_helper.js' %}" defer></script>
    ```
2.  **Convertir el script en un Escuchador Global (Event Listener)**:
    En lugar de acoplar la funcionalidad a un botón específico mediante atributos manuales, haz que JavaScript detecte automáticamente cualquier submit del sitio web.
    ```javascript
    // static/js/form_helper.js
    document.addEventListener('DOMContentLoaded', function() {
        document.addEventListener('submit', function(event) {
            // Buscamos el botón de tipo submit dentro del formulario que se está enviando
            const form = event.target;
            const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
            
            if (submitButton) {
                // Prevenir múltiples clics desactivando el botón
                // Se usa setTimeout para permitir que Django procese la validación del submit antes de deshabilitar
                setTimeout(() => {
                    submitButton.disabled = true;
                    // Opcional: Cambiar el texto del botón para feedback visual
                    submitButton.dataset.originalText = submitButton.innerHTML;
                    submitButton.innerHTML = "Procesando...";
                }, 50);
            }
        });
    });
    ```

---

## 3. Evitar "Magic Strings" en Roles de Usuario
### El Diagnóstico
Comparaciones como `if user.rol == 'PROFESOR'` usan cadenas de texto planas directamente en el código de las vistas.
*   **Problema**: Si en el futuro decides cambiar el nombre interno del rol a `'DOCENTE'`, tendrás que buscar en todo el proyecto dónde usaste `'PROFESOR'` en formato string.

### Guía de Implementación
1.  **Definir Constantes en el Modelo**:
    Usa la clase `TextChoices` de Django en `agenda/models.py`.
    ```python
    # agenda/models.py
    class Usuario(AbstractUser):
        class Roles(models.TextChoices):
            ESTUDIANTE = 'ESTUDIANTE', 'Estudiante'
            PROFESOR = 'PROFESOR', 'Profesor'
            ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
            
        rol = models.CharField(
            max_length=20, 
            choices=Roles.choices, 
            default=Roles.ESTUDIANTE
        )
    ```
2.  **Utilizar las constantes en las vistas**:
    ```python
    # agenda/views.py
    from .models import Usuario

    @login_required
    def actividad(request):
        if not (request.user.rol == Usuario.Roles.PROFESOR or request.user.is_superuser):
            return redirect('agenda:index')
        ...
    ```

---

## 4. Consultas Personalizadas en el Modelo (Custom Managers)
### El Diagnóstico
La definición de un usuario "pendiente" (`is_active=False` y `recien_registrado=True`) reside en la lógica de las vistas (`views.py`).
*   **Problema**: La vista se sobrecarga de responsabilidades (saber qué campos de base de datos definen el estado de un usuario). Si otra sección del código necesita consultar usuarios pendientes, tendrá que duplicar esta consulta.

### Guía de Implementación
1.  **Crear un QuerySet/Manager personalizado**:
    Define un Manager en `agenda/models.py` para abstraer la consulta.
    ```python
    # agenda/models.py
    from django.db import models
    from django.contrib.auth.models import UserManager

    class UsuarioQuerySet(models.QuerySet):
        def pendientes_de_activacion(self):
            return self.filter(is_active=False, recien_registrado=True)
            
        def activos(self):
            return self.filter(is_active=True)

    class CustomUserManager(UserManager.from_queryset(UsuarioQuerySet)):
        pass
        
    class Usuario(AbstractUser):
        # ... campos ...
        
        # Asignar el Manager personalizado
        objects = CustomUserManager()
    ```
2.  **Simplificar la vista**:
    Ahora, tus vistas no necesitan conocer los campos internos de activación. Solo piden la lista conceptualmente.
    ```python
    # agenda/views.py
    @login_required
    def gestion_usuarios(request):
        ...
        if tab == 'todos':
            usuarios_list = Usuario.objects.all().order_by('-date_joined')
        else:
            # Consulta limpia y descriptiva
            usuarios_list = Usuario.objects.pendientes_de_activacion().order_by('-date_joined')
        ...
    ```
