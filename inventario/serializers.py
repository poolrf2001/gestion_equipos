from rest_framework import serializers
from .models import Inventario, Mantenimiento, HistorialMantenimiento

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

class MantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantenimiento
        fields = '__all__'

class HistorialMantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialMantenimiento
        fields = '__all__'
