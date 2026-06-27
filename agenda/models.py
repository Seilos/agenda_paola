from sys import get_coroutine_origin_tracking_depth
from django.db.models.fields.related_lookups import get_normalized_value
from django.forms import formsets
from django.db import models
from agenda_project.models import *
from django.contrib.auth.models import AbstractUser

class Ambulatorio(MultiMixin):
    """
    Modelo que representa un ambulatorio
    hereda de MultiMixin
    """
    nombre = models.CharField(max_length=150, unique=True)
        
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Ambulatorio"
        verbose_name_plural = "Ambulatorios"
        constraints = [
            models.UniqueConstraint(
                fields=['nombre'],
                name='unique_nombre_ambulatorio'
            )
        ]

class Profesor(MultiMixin):
    """
    Modelo que representa un profesor
    hereda de MultiMixin
    """
    nombre_completo = models.CharField(max_length=150)
    especialidad = models.CharField(max_length=150, null=True, blank=True)
    usuario_sistema = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'rol':'PROFESOR'},
        related_name='profesor')
    
    def __str__(self):
        return self.nombre_completo
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        constraints = [
            models.UniqueConstraint(
                fields=['nombre_completo'],
                name='unique_nombre_profesor'
            )
        ]

class Estudiante(MultiMixin):
    """
    Modelo que representa un estudiante
    hereda de MultiMixin
    """
    nombre_completo = models.CharField(max_length=150)
    usuario_sistema = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'rol':'ESTUDIANTE'},
        related_name='estudiante'
    )
    profesor_asignado = models.ForeignKey(
        Profesor,
        on_delete=models.PROTECT, related_name='Estudiantes_a_cargo'
    )
    ambulatorio = models.ForeignKey(
        Ambulatorio,
        on_delete=models.PROTECT,
        related_name='Estudiantes_inscritos'
    )

    def __str__(self):
        return self.nombre_completo
    
    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        constraints = [
            models.UniqueConstraint(
                fields=['nombre_completo'],
                name='unique_nombre_estudiante'
            )
        ]

# 1. Modelo de Usuario Personalizado
class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que hereda de AbstractUser
    agregando el campo rol
    """
    ROLES = (
    ('ESTUDIANTE', 'Estudiante'),
    ('PROFESOR', 'Profesor'),
    ('ADMINISTRADOR', 'Administrador')
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='ESTUDIANTE')
    recien_registrado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username

    @property
    def obtener_rol_display(self):
        """
        Calcula jerárquicamente el rol del usuario para el frontend.
        Garantiza que un Superusuario siempre sea reconocido como Administrador,
        y de lo contrario, devuelve el formato legible del rol asignado.
        """
        # Validación de seguridad: Si es superusuario de Django, tiene el rol máximo por defecto
        if self.is_superuser:
            return 'Administrador'
        
        # El método nativo get_rol_display() de Django convierte 'PROFESOR' en 'Profesor' automáticamente
        return self.get_rol_display()
    
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
    class Genero(models.TextChoices):
        M = "M","Masculino"
        F = "F","Femenino"
    
    class Tipo_consulta(models.TextChoices):
        P = "P","Primera vez"
        S = "S","Subsecuente"

    class caso_biopsicosocial(models.TextChoices):
        S = "S","Si"
        N = "N","No"
    
    #Header
    fecha_hora = models.DateTimeField(auto_now_add=True)
    #nombre = models.ForeignKey(Paciente, on_delete=models.PROTECT, null=True, blank=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT, related_name='consultas_como_estudiante')
    profesor = models.ForeignKey(Profesor, on_delete=models.PROTECT, related_name='consultas_como_profesor')
    preceptor = models.CharField(max_length=100)
    ambulatorio = models.ForeignKey(Ambulatorio, on_delete=models.PROTECT)
    alias_paciente = models.CharField(max_length=100, null=True, blank=True)

    #Crud primera pagina
    tipo_consulta = models.CharField(
        max_length=1,
        choices=Tipo_consulta.choices,
        default=Tipo_consulta.P,
        null=True,
        blank=True
    )
    genero = models.CharField(
        max_length=1,
        choices=Genero.choices,
        default=Genero.M,
        null=True,
        blank=True
    )
    
        
    caso_biopsicosocial = models.CharField(
        max_length=1,
        choices=caso_biopsicosocial.choices,
        default=caso_biopsicosocial.N,
        null=True,
        blank=True
    )
    edad = models.IntegerField(null=True, blank=True)
    higiene = models.CharField(max_length=100, null=True, blank=True)
    nivel = models.CharField(max_length=100, null=True, blank=True)
    
    #Diagnostico
    criterio_diagnostico = models.TextField(max_length=500, null=True, blank=True)
    indicaciones_medico = models.TextField(max_length=500, null=True, blank=True)
    coincidencia = models.BooleanField(default=False)
    sugerido_por_estudiante = models.TextField(max_length=500, null=True, blank=True)
    procedimientos = models.ManyToManyField(
        'procedimientos',
        through='ProcedimientosConsultas',
        related_name='consultas'
    )

    #seguimiento del caso
    resultado = models.TextField(max_length=500, null=True, blank=True)
    estado_actual = models.CharField(max_length=100, null=True, blank=True)
    requiere_seguimiento = models.BooleanField(default=False)

    # Evaluacion del Profesor
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)   
    precicion_diagnostica = models.CharField(max_length=20, null=True, blank=True)   
    observaciones_evaluacion = models.TextField(max_length=500, null=True, blank=True)  
    

    def __str__(self):
        return f"Consulta del paciente: {self.alias_paciente} - {self.fecha_hora}"
        
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        

class procedimientos(MultiMixin):
    """
    Modelo que representa un procedimiento médico
    hereda de MultiMixin
    """
    procedimiento_nombre=models.CharField(max_length=100, null=True, blank=True)
    descripcion_procedimiento = models.TextField(max_length=500)

    def __str__(self):
        return self.procedimiento_nombre

    class Meta:
        verbose_name = "Procedimiento"
        verbose_name_plural = "Procedimientos"
        constraints = [
            models.UniqueConstraint(
                fields=['procedimiento_nombre'],
                name='unique_procedimiento_nombre'
            )
        ]
    
class ProcedimientosConsultas(MultiMixin):
    """
    Modelo que representa un procedimiento realizado en una consulta
    hereda de MultiMixin
    """
    consulta = models.ForeignKey(Consultas, on_delete=models.PROTECT, null=True, blank=True)
    procedimiento = models.ForeignKey(procedimientos, on_delete=models.PROTECT, null=True, blank=True)
    nombre_procedimiento = models.CharField(max_length=100)
    
    
    def __str__(self):
        return f"{self.procedimiento} realizado en la consulta {self.consulta}"

    class Meta:
        verbose_name = "Procedimiento Consulta"
        verbose_name_plural = "Procedimientos Consultas"
    