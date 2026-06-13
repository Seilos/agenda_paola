from django.db import models
from agenda_project.models import *
from django.contrib.auth.models import AbstractUser

# 1. Modelo de Usuario Personalizado
class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que hereda de AbstractUser
    agregando el campo rol
    """
    Roles = (
    ('ESTUDIANTE', 'Estudiante'),
    ('PROFESOR', 'Profesor'),
    ('ADMINISTRADOR', 'Administrador')
    )
    rol = models.CharField(max_length=20, choices=Roles, default='ESTUDIANTE')
    
    def __str__(self):
        return self.username
    
# 2. Modelo para paciente anonimo

class Paciente(MultiMixin):
    """
    Modelo que representa un paciente anónimo
    hereda de MultiMixin
    """
    nombre = models.CharField(max_length=100, null=True, blank=True)
        
    def __str__(self):
        return self.nombre

# 3. Modelo de consulta medica
class Consultas(MultiMixin):
    """
    Modelo que representa una consulta médica
    hereda de MultiMixin
    """
    fecha_hora = models.DateTimeField(null=True, blank=True)
    nombre_paciente = models.CharField(max_length=100, null=True, blank=True)
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, limit_choices_to={'rol': 'ESTUDIANTE'})
    profesor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, limit_choices_to={'rol': 'PROFESOR'})
    
    # Diagnostico
    diagnostico_estudiante = models.TextField(null=True, blank=True)
    diagnostico_medico = models.TextField(null=True, blank=True)
    diagnostico_final = models.TextField(null=True, blank=True)

    # Seguimiento
    requiere_seguimiento = models.BooleanField(default=False)
    fecha_proxima_consulta = models.DateTimeField(null=True, blank=True)
    comentarios_previos = models.TextField(null=True, blank=True)

    # Evaluacion del Profesor
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)   
    precicion_diagnostica = (models.CharField(max_length=20, null=True, blank=True))   
    observaciones_evaluacion = models.TextField(null=True, blank=True)   
       
    def __str__(self):
        return f"Consulta de {self.nombre_paciente}"
        
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        constraints = [
            models.UniqueConstraint(
                fields=['estudiante', 'nombre_paciente', 'fecha_hora'],
                name='unique_consulta_por_estudiante'
            )
        ]