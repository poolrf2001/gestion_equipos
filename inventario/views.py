from django.shortcuts import render
from rest_framework import viewsets
from .models import Inventario, Mantenimiento, HistorialMantenimiento
from .serializers import InventarioSerializer, MantenimientoSerializer, HistorialMantenimientoSerializer
from rest_framework.permissions import IsAuthenticated

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