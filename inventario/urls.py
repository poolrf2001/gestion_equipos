from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventarioViewSet, MantenimientoViewSet, HistorialMantenimientoViewSet

# Router para las rutas automáticas
router = DefaultRouter()
router.register(r'inventario', InventarioViewSet)
router.register(r'mantenimiento', MantenimientoViewSet)
router.register(r'historial', HistorialMantenimientoViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
