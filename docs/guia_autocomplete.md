# Guía de Uso del Componente Autocomplete Genérico

Esta guía describe cómo implementar rápidamente nuevas barras de búsqueda autocompletables en el proyecto utilizando el componente reutilizable `Autocomplete` definido en [autocomplete.js](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda_project/static/js/autocomplete.js).

---

## Paso 1: Definir la Estructura HTML

En tu plantilla Django, añade la estructura para el buscador con su menú desplegable. Asegúrate de incluir los atributos `data-url` y cualquier otro dato dinámico en el formulario.

```html
<div class="search-wrapper">
    <!-- Formulario Contenedor -->
    <form method="GET" action="" id="estudiantes-search-form" class="search-box" 
          data-url="{% url 'agenda:buscar_estudiantes_ajax' %}">
        
        <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        
        <!-- Input de texto -->
        <input type="text" name="q" id="estudiantes-search-input" placeholder="Buscar estudiante..." 
               autocomplete="off" class="search-input">
    </form>

    <!-- Menú Desplegable para Autocompletado -->
    <div id="estudiantes-dropdown" class="autocomplete-dropdown">
        <ul id="estudiantes-list" class="autocomplete-list">
            <!-- Insertado dinámicamente -->
        </ul>
    </div>
</div>
```

---

## Paso 2: Crear el Endpoint/Vista Django

La vista debe aceptar una petición GET con el parámetro de búsqueda `q` y retornar un JSON con una lista dentro de la clave `results` (o `usuarios` en el caso original).

```python
# agenda/views.py
from django.http import JsonResponse
from .models import Estudiante # Tu modelo

def buscar_estudiantes_ajax(request):
    query = request.GET.get('q', '').strip()
    resultados = []
    
    if query:
        # Ejemplo de filtrado por nombre/apellido
        estudiantes = Estudiante.objects.filter(
            nombre__icontains=query
        )[:5] # Limitar a 5 resultados para mejor performance
        
        for est in estudiantes:
            resultados.append({
                'id': est.id,
                'nombre': est.nombre,
                'matricula': est.matricula,
                'carrera': est.carrera
            })
            
    return JsonResponse({'results': resultados})
```

---

## Paso 3: Inicializar el Componente en JavaScript

Instancia el objeto `Autocomplete` en tu bloque `extra_js` de la plantilla o en un archivo JS dedicado:

```html
{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('estudiantes-search-form');
        if (!form) return;

        const url = form.getAttribute('data-url');

        new Autocomplete({
            inputSelector: '#estudiantes-search-input',
            dropdownSelector: '#estudiantes-dropdown',
            listSelector: '#estudiantes-list',
            formSelector: '#estudiantes-search-form',
            url: url,
            
            // Si necesitas pasar parámetros GET adicionales (ej. filtros activos)
            getParams: () => ({
                carrera_filtro: 'todas'
            }),
            
            // Función encargada de dibujar cada fila del menú desplegable
            renderItem: (estudiante) => {
                return `
                    <div style="font-weight: 600; color: #2c3e50; font-size: 0.9rem;">
                        ${estudiante.nombre}
                    </div>
                    <div style="font-size: 0.8rem; color: #7f8c8d; margin-top: 2px;">
                        Matrícula: ${estudiante.matricula} • ${estudiante.carrera}
                    </div>
                `;
            },
            
            // Qué acción realizar cuando se hace clic en una opción
            onSelect: (estudiante) => {
                const input = document.getElementById('estudiantes-search-input');
                const dropdown = document.getElementById('estudiantes-dropdown');
                
                input.value = estudiante.nombre;
                dropdown.style.display = 'none';
                
                // Envía el formulario de inmediato
                form.submit();
            }
        });
    });
</script>
{% endblock %}
```
