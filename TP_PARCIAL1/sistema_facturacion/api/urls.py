from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProductoViewSet, FacturaViewSet, ProveedorList, ProveedorDetail, ReporteList, ReporteDetail

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'facturas', FacturaViewSet)
#router.register(r'proveedores', ProveedorViewSet)
#router.register(r'reportes', ReporteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('proveedores/', ProveedorList.as_view(), name='proveedor-list'),  
    path('proveedores/<int:pk>/', ProveedorDetail.as_view(), name='proveedor-detail'), 

    path('reportes/', ReporteList.as_view(), name='reporte-list'), 
    path('reportes/<int:pk>/', ReporteDetail.as_view(), name='reporte-detail'), 
]
