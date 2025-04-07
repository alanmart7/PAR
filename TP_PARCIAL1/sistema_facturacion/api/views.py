from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Cliente, Producto, Factura, Proveedor, Reporte
from .serializers import ClienteSerializer, ProductoSerializer, FacturaSerializer, ProveedorSerializer, ReporteSerializer
from rest_framework.views import APIView

'''
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
'''
# Lista de clientes GET Y POST
class ClienteList(APIView):
    def get(self, request):
        clientes = Cliente.objects.all() # Obtener todos los clientes
         # Serializar manualmente los datos de los clientes
        data = [{"id": cliente.id, "nombre": cliente.nombre, "correo": cliente.correo} for cliente in clientes]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        nombre = request.data.get('nombre')
        correo = request.data.get('correo')
        cliente = Cliente.objects.create(nombre=nombre, correo=correo)   # Crear un nuevo cliente
        return Response({"id": cliente.id, "nombre": cliente.nombre, "correo": cliente.correo}, status=status.HTTP_201_CREATED)

# Detalles de cliente GET, PUT y DELETE por un ID especifico
class ClienteDetail(APIView):
    def get(self, request, pk):
        try:
            cliente = Cliente.objects.get(pk=pk)  # Buscar cliente por ID
            data = {"id": cliente.id, "nombre": cliente.nombre, "correo": cliente.correo}
            return Response(data, status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            cliente = Cliente.objects.get(pk=pk)  # Buscar cliente por ID
            cliente.nombre = request.data.get('nombre', cliente.nombre)  # Actualizar campos correspondientes
            cliente.correo = request.data.get('correo', cliente.correo)
            cliente.save()
            data = {"id": cliente.id, "nombre": cliente.nombre, "correo": cliente.correo}
            return Response(data, status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            cliente = Cliente.objects.get(pk=pk)  # Buscar cliente por ID
            cliente.delete()  # Eliminar cliente
            return Response({"message": "Cliente eliminado"}, status=status.HTTP_204_NO_CONTENT)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# Lista de productos GET y POST
class ProductoList(APIView):
    def get(self, request):
        productos = Producto.objects.all()  # Obtener todos los productos
        # Serializar manualmente los datos de los productos
        data = [{"id": producto.id, "nombre": producto.nombre, "precio": str(producto.precio), "descripcion": producto.descripcion} for producto in productos]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        nombre = request.data.get('nombre') 
        precio = request.data.get('precio')
        descripcion = request.data.get('descripcion')  
        producto = Producto.objects.create(nombre=nombre, precio=precio, descripcion=descripcion)  # Crear un nuevo producto
        return Response({"id": producto.id, "nombre": producto.nombre, "precio": str(producto.precio), "descripcion": producto.descripcion}, status=status.HTTP_201_CREATED)

# Detalles de producto GET, PUT y DELETE por un ID específico
class ProductoDetail(APIView):
    def get(self, request, pk):
        try:
            producto = Producto.objects.get(pk=pk)  # Buscar producto por ID
            data = {"id": producto.id, "nombre": producto.nombre, "precio": str(producto.precio), "descripcion": producto.descripcion}
            return Response(data, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            producto = Producto.objects.get(pk=pk)  # Buscar producto por ID
            producto.nombre = request.data.get('nombre', producto.nombre)
            producto.precio = request.data.get('precio', producto.precio)
            producto.descripcion = request.data.get('descripcion', producto.descripcion)
            producto.save()   # Actualizar campos del producto 
            data = {"id": producto.id, "nombre": producto.nombre, "precio": str(producto.precio), "descripcion": producto.descripcion}
            return Response(data, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            producto = Producto.objects.get(pk=pk) # Buscar producto por ID
            producto.delete()  # Eliminar producto
            return Response({"message": "Producto eliminado"}, status=status.HTTP_204_NO_CONTENT)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# Lista de facturas GET y POST
class FacturaList(APIView):
    def get(self, request):
        facturas = Factura.objects.all()  # Obtener todas las facturas
        # Serializar manualmente los datos de las facturas
        data = [{"id": factura.id, "numero": factura.numero, "cliente": factura.cliente.nombre, "total": str(factura.total)} for factura in facturas]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        numero = request.data.get('numero')
        cliente_id = request.data.get('cliente') # ID del cliente
        total = request.data.get('total')
        try:
            cliente = Cliente.objects.get(pk=cliente_id)  # Buscar cliente por ID
            factura = Factura.objects.create(numero=numero, cliente=cliente, total=total)   # Crear una nueva factura
            return Response({"id": factura.id, "numero": factura.numero, "cliente": factura.cliente.nombre, "total": str(factura.total)}, status=status.HTTP_201_CREATED)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=status.HTTP_400_BAD_REQUEST)


class FacturaDetail(APIView):
    def get(self, request, pk): 
        try:
            factura = Factura.objects.get(pk=pk) # Buscar factura por ID
            data = {"id": factura.id, "numero": factura.numero, "cliente": factura.cliente.nombre, "total": str(factura.total)}
            return Response(data, status=status.HTTP_200_OK)
        except Factura.DoesNotExist:
            return Response({"error": "Factura no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            factura = Factura.objects.get(pk=pk)  # Buscar factura por ID y actualiza
            factura.numero = request.data.get('numero', factura.numero) 
            cliente_id = request.data.get('cliente')
            if cliente_id:
                try:
                    cliente = Cliente.objects.get(pk=cliente_id)
                    factura.cliente = cliente
                except Cliente.DoesNotExist:
                    return Response({"error": "Cliente no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
            factura.total = request.data.get('total', factura.total)
            factura.save()
            data = {"id": factura.id, "numero": factura.numero, "cliente": factura.cliente.nombre, "total": str(factura.total)}
            return Response(data, status=status.HTTP_200_OK)
        except Factura.DoesNotExist:
            return Response({"error": "Factura no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            factura = Factura.objects.get(pk=pk) # Buscar factura por ID
            factura.delete() # Eliminar factura
            return Response({"message": "Factura eliminada"}, status=status.HTTP_204_NO_CONTENT)
        except Factura.DoesNotExist:
            return Response({"error": "Factura no encontrada"}, status=status.HTTP_404_NOT_FOUND)


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

# Detalles de proveedor GET, PUT y DELETE por un ID especifico
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

# Detalle de reporte GET, PUT y DELETE por un ID especifico
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
            reporte.nombre = request.data.get('nombre', reporte.nombre)  # Actualizar campos correspondientes
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
