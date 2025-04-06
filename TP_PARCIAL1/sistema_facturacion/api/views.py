from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Cliente, Producto, Factura, Proveedor, Reporte
from .serializers import ClienteSerializer, ProductoSerializer, FacturaSerializer, ProveedorSerializer, ReporteSerializer
from rest_framework.views import APIView

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer

'''
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
'''

# Lista de proveedores GET Y POST
class ProveedorList(APIView):
    def get(self, request):
        proveedores = Proveedor.objects.all()  # Obtener todos los proveedores
        data = [{"id": proveedor.id, "nombre": proveedor.nombre, "correo": proveedor.correo, "telefono": proveedor.telefono} for proveedor in proveedores]  # Serialización manual
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        nombre = request.data.get('nombre')
        correo = request.data.get('correo') 
        telefono = request.data.get('telefono')
        proveedor = Proveedor.objects.create(nombre=nombre, correo=correo, telefono=telefono)  # Crear un proveedor
        return Response({"id": proveedor.id, "nombre": proveedor.nombre, "correo": proveedor.correo, "telefono": proveedor.telefono}, status=status.HTTP_201_CREATED)

# DetalleS de proveedor PUT, DELETE
class ProveedorDetail(APIView):
    def get(self, request, pk):
        try:
            proveedor = Proveedor.objects.get(pk=pk)  # Buscar proveedor por ID
            data = {"id": proveedor.id, "nombre": proveedor.nombre, "correo": proveedor.correo, "telefono": proveedor.telefono}
            return Response(data, status=status.HTTP_200_OK)
        except Proveedor.DoesNotExist:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            proveedor = Proveedor.objects.get(pk=pk)  # Buscar proveedor por ID
            proveedor.nombre = request.data.get('nombre', proveedor.nombre)  # Actualizar campos
            proveedor.direccion = request.data.get('correo', proveedor.correo)
            proveedor.telefono = request.data.get('telefono', proveedor.telefono)
            proveedor.save()
            data = {"id": proveedor.id, "nombre": proveedor.nombre, "correo": proveedor.correo, "telefono": proveedor.telefono}
            return Response(data, status=status.HTTP_200_OK)
        except Proveedor.DoesNotExist:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            proveedor = Proveedor.objects.get(pk=pk)  # Buscar proveedor por ID
            proveedor.delete()  # Eliminar proveedor
            return Response({"message": "Proveedor eliminado"}, status=status.HTTP_204_NO_CONTENT)
        except Proveedor.DoesNotExist:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)


# Lista de reportes GET Y POST
class ReporteList(APIView):
    def get(self, request):
        reportes = Reporte.objects.all()  # Obtener todos los reportes
        data = [{"id": reporte.id, "nombre": reporte.nombre, "fecha_inicio": reporte.fecha_inicio, 
                 "fecha_fin": reporte.fecha_fin, "contenido": reporte.contenido} for reporte in reportes]  # Serialización manual
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        nombre = request.data.get('nombre')
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')
        contenido = request.data.get('contenido')
        reporte = Reporte.objects.create(nombre=nombre, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, contenido=contenido)  # Crear un reporte
        return Response({"id": reporte.id, "nombre": reporte.nombre, "fecha_inicio": reporte.fecha_inicio, 
                         "fecha_fin": reporte.fecha_fin, "contenido": reporte.contenido}, status=status.HTTP_201_CREATED)

# Detalle de reporte PUT y DELETE
class ReporteDetail(APIView):
    def get(self, request, pk):
        try:
            reporte = Reporte.objects.get(pk=pk)  # Buscar reporte por ID
            data = {"id": reporte.id, "nombre": reporte.nombre, "fecha_inicio": reporte.fecha_inicio, 
                    "fecha_fin": reporte.fecha_fin, "contenido": reporte.contenido}
            return Response(data, status=status.HTTP_200_OK)
        except Reporte.DoesNotExist:
            return Response({"error": "Reporte no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            reporte = Reporte.objects.get(pk=pk)  # Buscar reporte por ID
            reporte.nombre = request.data.get('nombre', reporte.nombre)  # Actualizar campos
            reporte.fecha_inicio = request.data.get('fecha_inicio', reporte.fecha_inicio)
            reporte.fecha_fin = request.data.get('fecha_fin', reporte.fecha_fin)
            reporte.contenido = request.data.get('contenido', reporte.contenido)
            reporte.save()
            data = {"id": reporte.id, "nombre": reporte.nombre, "fecha_inicio": reporte.fecha_inicio, 
                    "fecha_fin": reporte.fecha_fin, "contenido": reporte.contenido}
            return Response(data, status=status.HTTP_200_OK)
        except Reporte.DoesNotExist:
            return Response({"error": "Reporte no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            reporte = Reporte.objects.get(pk=pk)  # Buscar reporte por ID
            reporte.delete()  # Eliminar reporte
            return Response({"message": "Reporte eliminado"}, status=status.HTTP_204_NO_CONTENT)
        except Reporte.DoesNotExist:
            return Response({"error": "Reporte no encontrado"}, status=status.HTTP_404_NOT_FOUND)
