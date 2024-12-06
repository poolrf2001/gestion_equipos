from django.db import models

class Area(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.TextField(null=True, blank=True)
    responsable = models.CharField(max_length=255, null=True, blank=True)  # Nuevo campo

    def __str__(self):
        return self.nombre


class Inventario(models.Model):
    codigo_inventario = models.CharField(max_length=50, unique=True)  # Identificador único
    DETALLE_BIEN_CHOICES = [
        ('CPU', 'CPU'),
        ('Laptop', 'Laptop'),
        ('Impresora', 'Impresora'),
        ('All in One', 'All in One'),
    ]
    detalle_bien = models.CharField(
        max_length=50,
        choices=DETALLE_BIEN_CHOICES
    ) # Ejemplo: CPU, Monitor, Laptop
    marca = models.CharField(max_length=100, null=True, blank=True)  # Marca
    modelo = models.CharField(max_length=100, null=True, blank=True)
    procesador = models.CharField(max_length=50, null=True, blank=True)
    generacion = models.CharField(max_length=50, null=True, blank=True)
    velocidad = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    capacidad_disco = models.CharField(max_length=50, null=True, blank=True)
    tipo_disco = models.CharField(
        max_length=50,
        choices=[('HDD', 'HDD'), ('SSD', 'SSD')],
        null=True,
        blank=True
    )
    sistema_operativo = models.CharField(max_length=50, null=True, blank=True)  # Modelo
    estado_inventario = models.CharField(
        max_length=50,
        choices=[
            ('Presente', 'Presente'),
            ('Libre', 'Libre'),
            ('Fuera de Área', 'Fuera de Área'),
            ('No Habido', 'No Habido')
        ]
    )  # Estado del inventario
    estado_conservacion = models.CharField(
        max_length=50,
        choices=[
            ('Bueno', 'Bueno'),
            ('Regular', 'Regular'),
            ('Malo', 'Malo'),
        ],
        default='Regular'
    )  # Estado físico del bien
    area_actual = models.ForeignKey(
        Area, on_delete=models.SET_NULL, null=True, related_name='inventario_area_actual'
    )  # Ubicación actual
    fecha_actualizacion_estado = models.DateTimeField(auto_now=True)  # Última actualización del estado

    def __str__(self):
        return f"{self.detalle_bien} ({self.codigo_inventario})"


class HistorialArea(models.Model):
    inventario = models.ForeignKey('Inventario', on_delete=models.CASCADE, null=True, blank=True)
    periferico = models.ForeignKey('Periferico', on_delete=models.CASCADE, null=True, blank=True)
    area_anterior = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, related_name='historial_area_anterior')
    area_nueva = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, related_name='historial_area_nueva')
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.inventario:
            return f"{self.inventario.codigo_inventario} - {self.area_anterior} -> {self.area_nueva}"
        elif self.periferico:
            return f"{self.periferico.codigo_inventario} - {self.area_anterior} -> {self.area_nueva}"
        return "Movimiento desconocido"



class Periferico(models.Model):
    codigo_inventario = models.CharField(max_length=50, unique=True)  # Identificador único
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('Monitor', 'Monitor'),
            ('Teclado', 'Teclado'),
            ('Mouse', 'Mouse'),
            ('Parlantes', 'Parlantes'),
            ('Otros', 'Otros'),
        ]
    )  # Tipo de periférico
    marca = models.CharField(max_length=100, null=True, blank=True)  # Marca 
    estado_inventario = models.CharField(
        max_length=50,
        choices=[
            ('Presente', 'Presente'),
            ('Libre', 'Libre'),
            ('Fuera de Área', 'Fuera de Área'),
            ('No Habido', 'No Habido')
        ]
    )  # Estado del inventario
    estado_conservacion = models.CharField(
        max_length=50,
        choices=[
            ('Bueno', 'Bueno'),
            ('Regular', 'Regular'),
            ('Malo', 'Malo'),
        ],
        default='Regular'
    )  # Estado físico del periférico
    equipo_principal = models.ForeignKey(
        Inventario,
        on_delete=models.CASCADE,
        related_name='perifericos',
        null=True,
        blank=True
    )
    area_actual = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perifericos',
    )
    fecha_actualizacion_estado = models.DateTimeField(auto_now=True)  # Última actualización del estado

    def __str__(self):
        return f"{self.tipo} ({self.codigo_inventario})"
    
from django.db import models
import json   
class Mantenimiento(models.Model):
    TAREAS_CHOICES = [
        ('Inspección inicial', 'Inspección inicial'),
        ('Limpieza interna y externa', 'Limpieza interna y externa'),
        ('Revisión de conexiones internas y externas', 'Revisión de conexiones internas y externas'),
        ('Actualización de software y controladores', 'Actualización de software y controladores'),
        ('Verificación de estado del disco duro', 'Verificación de estado del disco duro'),
        ('Pruebas de funcionamiento', 'Pruebas de funcionamiento'),
        ('Activación de Windows', 'Activación de Windows'),
        ('Activación de Office', 'Activación de Office'),
        ('Otros', 'Otros'),
    ]

    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    fecha_mantenimiento = models.DateTimeField()
    tipo_mantenimiento = models.CharField(
        max_length=50,
        choices=[
            ('Preventivo', 'Preventivo'),
            ('Correctivo', 'Correctivo')
        ]
    )
    estado_inicial = models.CharField(
        max_length=50,
        choices=[
            ('Óptimo', 'Óptimo'),
            ('Bueno', 'Bueno'),
            ('Regular', 'Regular'),
            ('Malo', 'Malo')
        ],
        default='Bueno'
    )
    tareas_realizadas = models.JSONField(default=list, blank=True)
    tareas_otros = models.TextField(null=True, blank=True)  # Lista detallada de tareas realizadas
    problemas_detectados = models.TextField(null=True, blank=True)
    acciones_recomendadas = models.TextField(null=True, blank=True)
    observaciones_adicionales = models.TextField(null=True, blank=True)  # Nuevo campo  # Nuevo campo
    responsable_area = models.CharField(max_length=255, null=True, blank=True)  # Responsable del área

    def save(self, *args, **kwargs):
        # Llamar al método original save para guardar la ficha
        super().save(*args, **kwargs)
        
        # Crear una nueva entrada en el historial
        from django.apps import apps
        HistorialMantenimiento = apps.get_model('inventario', 'HistorialMantenimiento')  # Usar get_model
        HistorialMantenimiento.objects.create(
            inventario=self.inventario,
            fecha_mantenimiento=self.fecha_mantenimiento,
            tipo_mantenimiento=self.tipo_mantenimiento,
            estado_general=self.estado_inicial,
            problemas_detectados=self.problemas_detectados,
            observaciones=f"Ficha de mantenimiento creada: {self.pk}",
            mantenimiento=self
        )

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
