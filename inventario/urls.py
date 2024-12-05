from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventarioViewSet, MantenimientoViewSet, HistorialMantenimientoViewSet, inventarios_por_area, responsable_area

# Router para las rutas automáticas
router = DefaultRouter()
router.register(r'inventario', InventarioViewSet)
router.register(r'mantenimiento', MantenimientoViewSet)
router.register(r'historial', HistorialMantenimientoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('inventarios_por_area/<int:area_id>/', inventarios_por_area, name='inventarios_por_area'),
    path('api/responsable_area/<int:area_id>/', responsable_area, name='responsable_area'),
]
