from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProveedorList, ProveedorDetail, ReporteList, ReporteDetail, ClienteList, ClienteDetail, ProductoList, ProductoDetail,FacturaList, FacturaDetail, CompraList, CompraDetail, InventarioViewSet, VentaList, ReporteMovimientosMensualesView, ProductosMasVendidosView, TopClientesView, TopProveedoresView, ReporteUtilidadesView,ReporteComprasPorFechaView,ReporteVentasPorFechaView,CrearFacturaCompraView,CrearFacturaVentaView,ListarFacturasView

'''
from .views import ClienteViewSet, ProductoViewSet, FacturaViewSet,
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'facturas', FacturaViewSet)
#router.register(r'proveedores', ProveedorViewSet)
#router.register(r'reportes', ReporteViewSet)
router.register(r'inventario', InventarioViewSet)
'''
router = DefaultRouter()
router.register(r'inventario', InventarioViewSet)

urlpatterns = [
   # path('', include(router.urls)),
    # Clientes
    path('clientes/', ClienteList.as_view(), name='cliente-list'),
    path('clientes/<int:pk>/', ClienteDetail.as_view(), name='cliente-detail'),

    # Productos
    path('productos/', ProductoList.as_view(), name='producto-list'),
    path('productos/<int:pk>/', ProductoDetail.as_view(), name='producto-detail'),

    # Facturas
    path('facturas/', FacturaList.as_view(), name='factura-list'),
    path('facturas/<int:pk>/', FacturaDetail.as_view(), name='factura-detail'),

    # Proveedores
    path('proveedores/', ProveedorList.as_view(), name='proveedor-list'),  
    path('proveedores/<int:pk>/', ProveedorDetail.as_view(), name='proveedor-detail'), 

    # Reportes
    path('reportes/', ReporteList.as_view(), name='reporte-list'), 
    path('reportes/<int:pk>/', ReporteDetail.as_view(), name='reporte-detail'), 
    
    #Compras
    path('compras/', CompraList.as_view()),
    path('compras/<int:pk>/', CompraDetail.as_view()),

    #Ventas
    path('ventas/', VentaList.as_view(), name='venta-list'),

    #Movimientos Mensuales
    path('reporte-mensual/', ReporteMovimientosMensualesView.as_view(), name='reporte-mensual'),
    
    #Reporte top productos 
    path('reporte-productos-mas-vendidos/', ProductosMasVendidosView.as_view(), name='reporte-productos-mas-vendidos'),

    #Reporte top clientes TopClientesView
    path('reporte-top-clientes/', TopClientesView.as_view(), name='reporte-top-clientes'),
    
    #Reporte Top proveedores
    path('reporte-top-proveedores/', TopProveedoresView.as_view(), name='reporte-top-proveedores'),
    
    #Reporte Top Utilidades
    path('reporte-utilidades/', ReporteUtilidadesView.as_view(), name='reporte-utilidades'),

    #Reporte de compras
    path('reporte-compras-fechas/', ReporteComprasPorFechaView.as_view(), name='reporte_compras_fechas'),
    
    #Reporte de ventas
    path('reporte-ventas-fechas/', ReporteVentasPorFechaView.as_view(), name='reporte_ventas_fechas'),

    #Asignacion de facturas
    path('factura/compra/<int:compra_id>/', CrearFacturaCompraView.as_view(), name='crear_factura_compra'),
    path('factura/venta/<int:venta_id>/', CrearFacturaVentaView.as_view(), name='crear_factura_venta'),
    path('facturass/', ListarFacturasView.as_view(), name='listar_facturas'),

    path('', include(router.urls)),
    
]

