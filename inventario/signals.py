from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Inventario, Mantenimiento

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    # Crear grupos
    admin_group, _ = Group.objects.get_or_create(name='Administrador')
    tecnico_group, _ = Group.objects.get_or_create(name='Técnico')
    consultor_group, _ = Group.objects.get_or_create(name='Consultor')

    # Obtener permisos de los modelos
    inventario_perms = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Inventario))
    mantenimiento_perms = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Mantenimiento))

    # Asignar permisos
    admin_group.permissions.set(inventario_perms | mantenimiento_perms)  # Todos los permisos
    tecnico_group.permissions.set(mantenimiento_perms.exclude(codename__startswith='delete'))  # Sin eliminar
    consultor_group.permissions.set(
        inventario_perms.filter(codename__startswith='view') |
        mantenimiento_perms.filter(codename__startswith='view')
    )  # Solo lectura
