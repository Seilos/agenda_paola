import uuid
from django.db import models
from django.conf import settings  # usuario autenticado

# Create your models here.
class CreatedMixin(models.Model):
    """
    Mixin que agrega campos de auditoría:
    - created_at: fecha y hora de creación
    - created_by: usuario que creó el registro
    """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)s_created", null=True, blank=True)

    class Meta:
        abstract = True
    
class UpdatedMixin(models.Model):
    """
    Mixin que agrega campos de auditoría:
    - updated_at: fecha y hora de última modificación
    - updated_by: usuario que modificó el registro
    """
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)s_updated",
        null=True, blank=True)

    class Meta:
        abstract = True

class DeletedMixin(models.Model):
    """
    Mixin que agrega campos de auditoría:
    - deleted_at: fecha y hora de eliminación
    - deleted_by: usuario que eliminó el registro
    - is_deleted: indica si el registro está eliminado
    """
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="%(class)s_deleted",
        null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

class ActivMixin(models.Model):
    """
    Mixin que agrega campos de auditoría:
    - is_active: indica si el registro está activo
    """
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True

class IdMixin(models.Model):
    """
    Mixin que agrega campos de auditoría:
    - id: UUID único
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        abstract = True

class MultiMixin(IdMixin,CreatedMixin, UpdatedMixin, DeletedMixin, ActivMixin):
    """
    Mixin que combina todos los mixins de auditoría
    """
    class Meta:
        abstract = True


