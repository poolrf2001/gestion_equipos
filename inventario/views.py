from django.shortcuts import render
from rest_framework import viewsets
from .models import Area, Inventario, Mantenimiento, HistorialMantenimiento
from .serializers import InventarioSerializer, MantenimientoSerializer, HistorialMantenimientoSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

def equipos_principales_por_area(request, area_id):
    equipos = Inventario.objects.filter(area_actual_id=area_id).values('id', 'codigo_inventario', 'detalle_bien')
    return JsonResponse(list(equipos), safe=False)

def responsable_area(request, area_id):
    area = Area.objects.filter(id=area_id).first()
    if area:
        return JsonResponse({'responsable': area.responsable}, safe=False)
    return JsonResponse({'error': 'Área no encontrada'}, status=404)

def inventarios_por_area(request, area_id):
    """
    Retorna una lista de inventarios filtrados por área en formato JSON.
    """
    inventarios = Inventario.objects.filter(area_actual_id=area_id).values('id', 'codigo_inventario', 'detalle_bien')
    return JsonResponse(list(inventarios), safe=False)

class InventarioViewSet(viewsets.ModelViewSet):
    """
    API para gestionar el inventario de equipos.
    """
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

class MantenimientoViewSet(viewsets.ModelViewSet):
    """
    API para gestionar fichas de mantenimiento.
    """
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

class HistorialMantenimientoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para consultar el historial de mantenimiento de equipos.
    """
    queryset = HistorialMantenimiento.objects.all()
    serializer_class = HistorialMantenimientoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrar por equipo si se pasa un parámetro "inventario_id"
        inventario_id = self.request.query_params.get('inventario_id')
        if inventario_id:
            return self.queryset.filter(inventario__id=inventario_id)
        return self.queryset
    
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Mantenimiento    
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.timezone import localtime

from django.conf import settings
from django.utils.timezone import localtime

from django.conf import settings
from django.utils.timezone import localtime

def generar_ficha_pdf_y_guardar(request, mantenimiento_id):
    mantenimiento = Mantenimiento.objects.get(pk=mantenimiento_id)

    # Si ya existe un PDF, eliminarlo
    if mantenimiento.pdf_url:
        existing_pdf_path = mantenimiento.pdf_url.replace(settings.MEDIA_URL, "")
        if default_storage.exists(existing_pdf_path):
            default_storage.delete(existing_pdf_path)
            
    # Construir las URLs absolutas para las fotos
    foto_antes_1_url = request.build_absolute_uri(mantenimiento.foto_antes_1.url) if mantenimiento.foto_antes_1 else None
    foto_antes_2_url = request.build_absolute_uri(mantenimiento.foto_antes_2.url) if mantenimiento.foto_antes_2 else None
    foto_despues_1_url = request.build_absolute_uri(mantenimiento.foto_despues_1.url) if mantenimiento.foto_despues_1 else None
    foto_despues_2_url = request.build_absolute_uri(mantenimiento.foto_despues_2.url) if mantenimiento.foto_despues_2 else None

    # Obtener periféricos asociados al equipo principal
    perifericos = mantenimiento.inventario.perifericos.all()

    # Convertir las tareas realizadas en lista de strings
    tareas_realizadas = mantenimiento.tareas_realizadas if mantenimiento.tareas_realizadas else []
    # Renderizar el HTML
    html_string = render_to_string(
        'mantenimiento/ficha_pdf.html',
        {
            'mantenimiento': mantenimiento,
            'perifericos': perifericos ,
            'tareas_realizadas': tareas_realizadas,
            'foto_antes_1_url': foto_antes_1_url,
            'foto_antes_2_url': foto_antes_2_url,
            'foto_despues_1_url': foto_despues_1_url,
            'foto_despues_2_url': foto_despues_2_url,
        }
    )

    # Nombre y ruta del archivo
    numero_inventario = mantenimiento.inventario.codigo_inventario
    fecha = localtime(mantenimiento.fecha_mantenimiento).strftime('%Y-%m-%d')
    filename = f'mantenimientos/{numero_inventario}/mantenimiento_{numero_inventario}_{fecha}.pdf'

    # Generar el PDF como archivo
    pdf_file = ContentFile(HTML(string=html_string).write_pdf())

    # Guardar el archivo en default_storage
    pdf_path = default_storage.save(filename, pdf_file)

    # Construir la URL completa utilizando MEDIA_URL
    pdf_url = f"{settings.MEDIA_URL}{pdf_path}"

    # Guardar la URL en el modelo
    mantenimiento.pdf_url = pdf_url
    mantenimiento.save()

    # Retornar la ruta del PDF generado
    return HttpResponse(f'PDF guardado en: {pdf_url}')



