from django import forms
from .models import Consultas

class RegistroConsultaForm(forms.ModelForm):
    class Meta:
        model = Consultas
        fields = [
            'docente',
            'ambulatorio',
            'preceptor',
            'tipo_consulta',
            'genero',
            'biopsicosocial',
            'edad',
            'higiene_diagnostico',
            'nivel',
            'procedimiento',
            'criterios_diagnosticos',
            'indicaciones_medico',
            'coincide_criterio',
            'sugerido_estudiante',
            'seguimiento_indicado',
            'estado_paciente',           
        ]