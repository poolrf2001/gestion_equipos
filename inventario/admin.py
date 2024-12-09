from django.contrib import admin
from .models import Area, Inventario, Periferico, Mantenimiento,HistorialMantenimiento, Usuario

from django.contrib import admin

# Cambia el título del encabezado
admin.site.site_header = "Administración de Mantenimientos"
# Cambia el texto que aparece en el título del navegador
admin.site.site_title = "Administración de Mantenimientos"
# Cambia el texto en la página principal del admin
admin.site.index_title = "Bienvenido al Sistema de Gestión de Mantenimientos"


# Registro de Áreas
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('codigo_inventario', 'detalle_bien', 'marca', 'modelo', 'estado_inventario', 'area_actual', 'fecha_actualizacion_estado')
    list_filter = ('detalle_bien', 'estado_inventario', 'area_actual')
    search_fields = ('codigo_inventario', 'marca', 'modelo', 'detalle_bien')
    readonly_fields = ('fecha_actualizacion_estado',)

    class Media:
        js = ('admin/js/inventario.js',)

from .models import Periferico
from .forms import PerifericoForm
@admin.register(Periferico)
class PerifericoAdmin(admin.ModelAdmin):
    form = PerifericoForm
    list_display = ('codigo_inventario', 'tipo', 'marca', 'estado_inventario', 'area_actual', 'fecha_actualizacion_estado', 'equipo_principal')
    list_filter = ('tipo', 'estado_inventario', 'area_actual')
    search_fields = ('codigo_inventario', 'marca', 'modelo', 'tipo')

# Registro de Mantenimiento
from django.contrib import admin
from .forms import MantenimientoForm
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from .models import Mantenimiento
from .views import generar_ficha_pdf_y_guardar
@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    form = MantenimientoForm
    change_list_template = "admin/inventario/mantenimiento_change_list.html"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:mantenimiento_id>/regenerar_pdf/', self.admin_site.admin_view(self.regenerar_pdf), name='regenerar_pdf'),
        ]
        return custom_urls + urls

    def regenerar_pdf(self, request, mantenimiento_id):
        # Lógica para regenerar el PDF
        generar_ficha_pdf_y_guardar(request, mantenimiento_id)
        self.message_user(request, f"PDF del mantenimiento {mantenimiento_id} regenerado correctamente.")
        return redirect("admin:inventario_mantenimiento_changelist")
    
    def ver_pdf(self, obj):
        if obj.pdf_url:
            return format_html('<a href="{}" target="_blank">Ver PDF</a>', obj.pdf_url)
        return "No disponible"
    ver_pdf.short_description = "PDF Generado"

    class Media:
        js = ('admin/js/inventario.js', 'admin/js/responsable_area.js',)

    fieldsets = (
        (None, {
            'fields': ('area', 'responsable_area', 'inventario', 'fecha_mantenimiento', 'tipo_mantenimiento', 'estado_inicial', 'tareas_realizadas', 'tareas_otros')
        }),
        ('Observaciones', {
            'fields': ('estado_general', 'problemas_detectados', 'acciones_recomendadas', 'observaciones_adicionales')
        }),
        ('Registro Fotográfico', {
            'fields': ('foto_antes_1', 'foto_antes_2', 'foto_despues_1', 'foto_despues_2', 'pdf_url')
        }),
    )

    def preview_foto_antes_1(self, obj):
        if obj.foto_antes_1:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.foto_antes_1.url)
        return "No disponible"

    def preview_foto_despues_1(self, obj):
        if obj.foto_despues_1:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.foto_despues_1.url)
        return "No disponible"

    list_display = (
        'inventario', 'area', 'fecha_mantenimiento', 'tipo_mantenimiento',
        'estado_inicial', 'estado_general', 'responsable_area', 'ver_pdf', 
        'preview_foto_antes_1', 'preview_foto_despues_1'
    )

    list_filter = (
        'area', 'tipo_mantenimiento', 'estado_inicial'
    )

    search_fields = (
        'inventario__codigo_inventario', 'responsable_area', 'problemas_detectados', 'area__nombre'
    )


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

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'responsable')  # Mostrar campos clave
    search_fields = ('nombre', 'responsable')  # Búsqueda por nombre y responsable

from django.contrib import admin
from .models import HistorialArea

@admin.register(HistorialArea)
class HistorialAreaAdmin(admin.ModelAdmin):
    list_display = ('inventario', 'periferico', 'area_anterior', 'area_nueva', 'fecha_cambio')
    list_filter = ('area_anterior', 'area_nueva', 'fecha_cambio')
    search_fields = ('inventario__codigo_inventario', 'periferico__codigo_inventario')
    date_hierarchy = 'fecha_cambio'
