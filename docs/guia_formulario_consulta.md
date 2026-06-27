# Guía para la Creación de un Formulario de Consulta Médica

Esta guía explica cómo construir y diseñar un formulario para la creación de consultas médicas utilizando el modelo `Consultas`, un formulario Django (`forms.ModelForm`) y las clases CSS del sistema de diseño ya definidas en `components.css`.

---

## 1. Definir el Formulario en Django (`forms.py`)

Creamos el formulario heredando de `forms.ModelForm`. Agregamos clases y placeholders directamente en los *widgets* del formulario si es necesario:

```python
# agenda/forms.py
from django import forms
from .models import Consultas

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consultas
        # Campos que el estudiante o profesor completará al crear la consulta
        fields = [
            'nombre_id', 
            'fecha_hora', 
            'profesor_id', 
            'diagnostico_estudiante', 
            'comentarios_previos'
        ]
        
        labels = {
            'nombre_id': 'Paciente',
            'fecha_hora': 'Fecha y Hora de la Consulta',
            'profesor_id': 'Profesor Asignado',
            'diagnostico_estudiante': 'Diagnóstico Inicial (Estudiante)',
            'comentarios_previos': 'Comentarios Previos',
        }

        widgets = {
            # Se usa el type datetime-local para que el navegador muestre un selector de fecha/hora nativo y moderno
            'fecha_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'diagnostico_estudiante': forms.Textarea(
                attrs={'placeholder': 'Escribe tu diagnóstico inicial aquí...', 'rows': 4}
            ),
            'comentarios_previos': forms.Textarea(
                attrs={'placeholder': 'Observaciones previas del paciente...', 'rows': 3}
            ),
        }
```

---

## 2. La Vista en Django (`views.py`)

Una vista básica que maneja la lógica de renderizado e inserción del formulario:

```python
# agenda/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConsultaForm

def crear_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            # Guardar la consulta. Si es estudiante, le autoasignamos su estudiante_id
            consulta = form.save(commit=False)
            if request.user.rol == 'ESTUDIANTE':
                consulta.estudiante_id = request.user
            consulta.save()
            
            messages.success(request, '¡Consulta médica programada con éxito!')
            return redirect('agenda:index')
    else:
        form = ConsultaForm()
        
    return render(request, 'agenda/crear_consulta.html', {'form': form})
```

---

## 3. El Template HTML (`crear_consulta.html`)

Reutiliza los componentes estructurales (`.page-card`, `.form-row`, `.form-group`, `.btn-*`, etc.) que ya definimos. 

Renderizamos los campos de forma manual campo a campo para tener un control exacto del diseño responsivo:

```html
{% extends 'agenda/base.html' %}

{% block title %}Programar Consulta - Agenda{% endblock %}

{% block section_name %}Nueva Consulta{% endblock %}

{% block content %}
<div class="page-card">
    <h2 class="page-card-title">Programar Nueva Consulta Médica</h2>

    <form method="POST" action="">
        {% csrf_token %}

        <!-- Mensaje de error general de formulario -->
        {% if form.non_field_errors %}
        <div class="alert-form-error">
            {% for error in form.non_field_errors %}
                <p>{{ error }}</p>
            {% endfor %}
        </div>
        {% endif %}

        <!-- FILA 1: Paciente y Fecha/Hora (Dos columnas responsivas) -->
        <div class="form-row">
            <div class="form-group">
                <label for="{{ form.nombre_id.id_for_label }}">{{ form.nombre_id.label }}</label>
                {{ form.nombre_id }}
                {% if form.nombre_id.errors %}
                    <span class="field-error">{{ form.nombre_id.errors.0 }}</span>
                {% endif %}
            </div>

            <div class="form-group">
                <label for="{{ form.fecha_hora.id_for_label }}">{{ form.fecha_hora.label }}</label>
                {{ form.fecha_hora }}
                {% if form.fecha_hora.errors %}
                    <span class="field-error">{{ form.fecha_hora.errors.0 }}</span>
                {% endif %}
            </div>
        </div>

        <!-- FILA 2: Profesor Asignado (Ancho completo) -->
        <div class="form-group">
            <label for="{{ form.profesor_id.id_for_label }}">{{ form.profesor_id.label }}</label>
            {{ form.profesor_id }}
            {% if form.profesor_id.errors %}
                <span class="field-error">{{ form.profesor_id.errors.0 }}</span>
            {% endif %}
        </div>

        <!-- FILA 3: Diagnóstico del Estudiante (Área de Texto) -->
        <div class="form-group">
            <label for="{{ form.diagnostico_estudiante.id_for_label }}">{{ form.diagnostico_estudiante.label }}</label>
            {{ form.diagnostico_estudiante }}
            {% if form.diagnostico_estudiante.errors %}
                <span class="field-error">{{ form.diagnostico_estudiante.errors.0 }}</span>
            {% endif %}
        </div>

        <!-- FILA 4: Comentarios Previos (Área de Texto) -->
        <div class="form-group">
            <label for="{{ form.comentarios_previos.id_for_label }}">{{ form.comentarios_previos.label }}</label>
            {{ form.comentarios_previos }}
            {% if form.comentarios_previos.errors %}
                <span class="field-error">{{ form.comentarios_previos.errors.0 }}</span>
            {% endif %}
        </div>

        <!-- Botones de Acción (Guardar o Cancelar) -->
        <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 25px;">
            <a href="{% url 'agenda:index' %}" class="btn-ghost">Cancelar</a>
            <button type="submit" class="btn-primary">Programar Consulta</button>
        </div>
    </form>
</div>
{% endblock %}
```
