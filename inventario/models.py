from django.db import models

# Create your models here.

class Area(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    codigo_inventario = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=50)  # Ejemplo: CPU, Laptop, Impresora
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    estado_inventario = models.CharField(
        max_length=50,
        choices=[
            ('Presente', 'Presente'),
            ('Libre', 'Libre'),
            ('Fuera de Área', 'Fuera de Área'),
            ('No Habido', 'No Habido')
        ]
    )
    fecha_actualizacion_estado = models.DateTimeField(auto_now=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(null=True, blank=True)
    # Campos para monitores asociados
    codigo_inventario_monitor = models.CharField(max_length=50, null=True, blank=True)
    marca_monitor = models.CharField(max_length=100, null=True, blank=True)
    modelo_monitor = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.categoria} ({self.codigo_inventario})"

class Periferico(models.Model):
    codigo_inventario = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=50)  # Ejemplo: Monitor, Teclado, Mouse
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    estado_inventario = models.CharField(
        max_length=50,
        choices=[
            ('Presente', 'Presente'),
            ('Libre', 'Libre'),
            ('Fuera de Área', 'Fuera de Área'),
            ('No Habido', 'No Habido')
        ]
    )
    fecha_actualizacion_estado = models.DateTimeField(auto_now=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} ({self.codigo_inventario})"

class Mantenimiento(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    fecha_mantenimiento = models.DateTimeField()
    tipo_mantenimiento = models.CharField(
        max_length=50,
        choices=[
            ('Preventivo', 'Preventivo'),
            ('Correctivo', 'Correctivo')
        ]
    )
    software_actualizado = models.BooleanField(default=False)
    estado_general = models.CharField(
        max_length=50,
        choices=[
            ('Óptimo', 'Óptimo'),
            ('Bueno', 'Bueno'),
            ('Regular', 'Regular'),
            ('Malo', 'Malo')
        ]
    )
    estado_inventario = models.CharField(max_length=50)
    partes_mantenidas = models.TextField(null=True, blank=True)
    problemas_detectados = models.TextField(null=True, blank=True)
    acciones_recomendadas = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Mantenimiento ({self.inventario.codigo_inventario}) - {self.fecha_mantenimiento}"

class RegistroFotografico(models.Model):
    mantenimiento = models.OneToOneField(Mantenimiento, on_delete=models.CASCADE)
    foto_antes = models.ImageField(upload_to='fotos_mantenimiento/', null=True, blank=True)
    foto_despues = models.ImageField(upload_to='fotos_mantenimiento/', null=True, blank=True)

    def __str__(self):
        return f"Fotos de {self.mantenimiento.inventario.codigo_inventario}"

class HistorialMantenimiento(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    fecha_mantenimiento = models.DateTimeField()
    tipo_mantenimiento = models.CharField(max_length=50)
    estado_general = models.CharField(max_length=50)
    estado_inventario = models.CharField(max_length=50)
    problemas_detectados = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Historial ({self.inventario.codigo_inventario}) - {self.fecha_mantenimiento}"

from django.contrib.auth.models import AbstractUser
from django.db import models
from .models import Area

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Técnico', 'Técnico'),
        ('Consultor', 'Consultor'),
    ]
    rol = models.CharField(max_length=50, choices=ROL_CHOICES)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.rol})"
