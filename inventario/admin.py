from django.contrib import admin
from .models import Area, Inventario, Periferico, Mantenimiento, RegistroFotografico, HistorialMantenimiento, Usuario

# Registro de Áreas
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('codigo_inventario', 'detalle_bien', 'marca', 'modelo', 'estado_inventario', 'area_actual', 'fecha_actualizacion_estado')
    list_filter = ('detalle_bien', 'estado_inventario', 'area_actual')
    search_fields = ('codigo_inventario', 'marca', 'modelo', 'detalle_bien')

@admin.register(Periferico)
class PerifericoAdmin(admin.ModelAdmin):
    list_display = ('codigo_inventario', 'tipo', 'marca', 'modelo', 'estado_inventario', 'area_actual', 'fecha_actualizacion_estado', 'equipo_principal')
    list_filter = ('tipo', 'estado_inventario', 'area_actual')
    search_fields = ('codigo_inventario', 'marca', 'modelo', 'tipo')

# Registro de Mantenimiento
from django.contrib import admin
from .models import Mantenimiento

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = (
        'inventario', 'fecha_mantenimiento', 'tipo_mantenimiento',
        'estado_inicial', 'responsable_area'
    )
    list_filter = (
        'tipo_mantenimiento', 'estado_inicial'
    )
    search_fields = ('inventario__codigo_inventario', 'responsable_area', 'problemas_detectados')



# Registro de RegistroFotografico
@admin.register(RegistroFotografico)
class RegistroFotograficoAdmin(admin.ModelAdmin):
    list_display = ('mantenimiento', 'foto_antes', 'foto_despues')

# Registro de HistorialMantenimiento
@admin.register(HistorialMantenimiento)
class HistorialMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('inventario', 'fecha_mantenimiento', 'tipo_mantenimiento', 'estado_general', 'estado_inventario')
    list_filter = ('tipo_mantenimiento', 'estado_general', 'estado_inventario')
    search_fields = ('inventario__codigo_inventario',)

# Registro de Usuarios
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'area', 'is_active')
    list_filter = ('rol', 'is_active')
    search_fields = ('username', 'email')
