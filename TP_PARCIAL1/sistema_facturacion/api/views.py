import json 
import uuid
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Cliente, Producto, Factura, Proveedor, Reporte, Compra, Inventario, Venta, Auditoria, Facturas
from .serializers import ClienteSerializer, ProductoSerializer, FacturaSerializer, ProveedorSerializer, ReporteSerializer, CompraSerializer, InventarioSerializer, VentaSerializer
from rest_framework.views import APIView
from datetime import datetime
from django.db.models import Sum, F, FloatField
from django.utils.timezone import now
from calendar import monthrange



# Lista de clientes GET Y POST
class ClienteList(APIView):
    def get(self, request):
        clientes = Cliente.objects.all() # Obtener todos los clientes
         # Serializar manualmente los datos de los clientes
        data = [{"id": cliente.id, "nombre": cliente.nombre, "correo": cliente.correo} for cliente in clientes]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        print("Datos recibidos en POST:", request.data)  # 🔍 Agregar esta línea
        nombre = request.data.get('nombre')
        correo = request.data.get('correo')
        cliente = Cliente.objects.create(nombre=nombre, correo=correo)   # Crear un nuevo cliente

         # Guardar auditoría
        Auditoria.objects.create(
        modelo='Cliente',
        operacion='CREATE',
        id_registro=cliente.id,
        datos_nuevos=json.dumps({"nombre": nombre, "correo": correo})
    )
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
            datos_anteriores = {"nombre": cliente.nombre, "correo": cliente.correo}
            cliente.nombre = request.data.get('nombre', cliente.nombre)  # Actualizar campos correspondientes
            cliente.correo = request.data.get('correo', cliente.correo)
            cliente.save()

            datos_nuevos = {"nombre": cliente.nombre, "correo": cliente.correo}

            Auditoria.objects.create(
            modelo='Cliente',
            operacion='UPDATE',
            id_registro=cliente.id,
            datos_anteriores=json.dumps(datos_anteriores),
            datos_nuevos=json.dumps(datos_nuevos))

            data = {"id": cliente.id, "nombre": cliente.nombre, "correo": cliente.correo}
            return Response(data, status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            cliente = Cliente.objects.get(pk=pk)  # Buscar cliente por ID
            datos_anteriores = {"nombre": cliente.nombre, "correo": cliente.correo}
            cliente.delete()  # Eliminar cliente

            Auditoria.objects.create(
            modelo='Cliente',
            operacion='DELETE',
            id_registro=cliente.id,
            datos_anteriores=json.dumps(datos_anteriores)
        )
            return Response({"message": "Cliente eliminado"}, status=status.HTTP_204_NO_CONTENT)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# Lista de productos GET y POST
class ProductoList(APIView):
    def get(self, request):
        productos = Producto.objects.all()
        data = [
            {
                "id": p.id,
                "nombre": p.nombre,
                "precio_compra": str(p.precio_compra),
                "precio_venta": str(p.precio_venta),
                "descripcion": p.descripcion
            }
            for p in productos
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = serializer.save()  # Esto llama al método create del serializer
             # Auditoría create
            Auditoria.objects.create(
                modelo='Producto',
                operacion='CREATE',
                id_registro=producto.id,
                datos_nuevos=json.dumps(serializer.data)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Detalles de producto GET, PUT y DELETE por un ID específico
class ProductoDetail(APIView):
    def get(self, request, pk):
        try:
            p = Producto.objects.get(pk=pk)
            data = {
                "id": p.id,
                "nombre": p.nombre,
                "precio_compra": str(p.precio_compra),
                "precio_venta": str(p.precio_venta),
                "descripcion": p.descripcion
            }
            return Response(data, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            p = Producto.objects.get(pk=pk)
            datos_anteriores = {
                "nombre": p.nombre,
                "precio_compra": str(p.precio_compra),
                "precio_venta": str(p.precio_venta),
                "descripcion": p.descripcion
            }
            p.nombre = request.data.get('nombre', p.nombre)
            p.precio_compra = request.data.get('precio_compra', p.precio_compra)
            p.precio_venta = request.data.get('precio_venta', p.precio_venta)
            p.descripcion = request.data.get('descripcion', p.descripcion)
            p.save()

            datos_nuevos = {
                "nombre": p.nombre,
                "precio_compra": str(p.precio_compra),
                "precio_venta": str(p.precio_venta),
                "descripcion": p.descripcion
            }
            
            # Auditoría update
            Auditoria.objects.create(
                modelo='Producto',
                operacion='UPDATE',
                id_registro=p.id,
                datos_anteriores=json.dumps(datos_anteriores),
                datos_nuevos=json.dumps(datos_nuevos)
            )

            data = {
                "id": p.id,
                "nombre": p.nombre,
                "precio_compra": str(p.precio_compra),
                "precio_venta": str(p.precio_venta),
                "descripcion": p.descripcion
            }


            return Response(data, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            p = Producto.objects.get(pk=pk)
            datos_anteriores = {
                "nombre": p.nombre,
                "precio_compra": str(p.precio_compra),
                "precio_venta": str(p.precio_venta),
                "descripcion": p.descripcion
            }
            p.delete()
            # Auditoría delete
            Auditoria.objects.create(
                modelo='Producto',
                operacion='DELETE',
                id_registro=pk,
                datos_anteriores=json.dumps(datos_anteriores)
            )
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

         # Auditoría create
        Auditoria.objects.create(
            modelo='Proveedor',
            operacion='CREATE',
            id_registro=proveedor.id,
            datos_nuevos=json.dumps({"nombre": nombre, "correo": correo, "telefono": telefono})
        )
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
            datos_anteriores = {"nombre": proveedor.nombre, "correo": proveedor.correo, "telefono": proveedor.telefono}
            proveedor.nombre = request.data.get('nombre', proveedor.nombre)  # Actualizar campos
            proveedor.correo = request.data.get('correo', proveedor.correo)
            proveedor.telefono = request.data.get('telefono', proveedor.telefono)
            proveedor.save()
            datos_nuevos = {"nombre": proveedor.nombre, "correo": proveedor.correo, "telefono": proveedor.telefono}

             # Auditoría update
            Auditoria.objects.create(
                modelo='Proveedor',
                operacion='UPDATE',
                id_registro=proveedor.id,
                datos_anteriores=json.dumps(datos_anteriores),
                datos_nuevos=json.dumps(datos_nuevos)
            )

            data = {"id": proveedor.id, "nombre": proveedor.nombre, "correo": proveedor.correo, "telefono": proveedor.telefono}
            return Response(data, status=status.HTTP_200_OK)
        except Proveedor.DoesNotExist:
            return Response({"error": "Proveedor no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            proveedor = Proveedor.objects.get(pk=pk)  # Buscar proveedor por ID
            datos_anteriores = {"nombre": proveedor.nombre, "correo": proveedor.correo, "telefono": proveedor.telefono}
            proveedor.delete()  # Eliminar proveedor

            # Auditoría delete
            Auditoria.objects.create(
                modelo='Proveedor',
                operacion='DELETE',
                id_registro=pk,
                datos_anteriores=json.dumps(datos_anteriores)
            )
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
        
# Lista y creación de compras
class CompraList(APIView):
    def get(self, request):
        compras = Compra.objects.all()
        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("📦 Datos recibidos en el POST de compras:")
        print(request.data)  # <-- Este es el log importante
        serializer = CompraSerializer(data=request.data)
        if serializer.is_valid():
            compra = serializer.save()
            Auditoria.objects.create(
                modelo='Compra',
                operacion='CREATE',
                id_registro=compra.id,
                datos_nuevos=json.dumps(serializer.data)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Detalle, actualización y eliminación por ID
class CompraDetail(APIView):    
    def get_object(self, pk):
        try:
            return Compra.objects.get(pk=pk)
        except Compra.DoesNotExist:
            return None

    def get(self, request, pk):
        compra = self.get_object(pk)
        if not compra:
            return Response({"error": "Compra no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompraSerializer(compra)
        return Response(serializer.data)

    def put(self, request, pk):
        compra = self.get_object(pk)
        if not compra:
            return Response({"error": "Compra no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompraSerializer(compra, data=request.data)
        if serializer.is_valid():
            datos_anteriores = CompraSerializer(compra).data
            compra = serializer.save()
            datos_nuevos = CompraSerializer(compra).data
            Auditoria.objects.create(
                modelo='Compra',
                operacion='UPDATE',
                id_registro=compra.id,
                datos_anteriores=json.dumps(datos_anteriores),
                datos_nuevos=json.dumps(datos_nuevos)
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        compra = self.get_object(pk)
        if not compra:
            return Response({"error": "Compra no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        datos_anteriores = CompraSerializer(compra).data
        compra.delete()
        Auditoria.objects.create(
            modelo='Compra',
            operacion='DELETE',
            id_registro=pk,
            datos_anteriores=json.dumps(datos_anteriores)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class VentaList(APIView):
    def get(self, request):
        ventas = Venta.objects.all()
        data = [
            {
                "id": v.id,
                "fecha": v.fecha,
                "cantidad": v.cantidad,
                "producto_id": v.producto.id,
                "producto_nombre": v.producto.nombre,
                "cliente_id": v.cliente.id,
                "cliente_nombre": v.cliente.nombre,
            }
            for v in ventas
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        producto_id = request.data.get("producto_id")
        cliente_id = request.data.get("cliente_id")
        cantidad = int(request.data.get("cantidad"))
        print("Producto ID:", producto_id)
        print("Cliente ID:", cliente_id)
        print("Cantidad:", cantidad)
        try:
            producto = Producto.objects.get(id=producto_id)
            cliente = Cliente.objects.get(id=cliente_id)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
        except Cliente.DoesNotExist:
            return Response({"error": "Cliente no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            inventario = Inventario.objects.get(producto_id=producto.id)
        except Inventario.DoesNotExist:
            return Response({"error": "No hay inventario para este producto"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si hay suficiente stock
        if inventario.stock < cantidad:
            return Response({"error": f"Stock insuficiente. Solo hay {inventario.stock} unidades disponibles."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Registrar la venta
        venta = Venta.objects.create(
            producto=producto,
            cliente=cliente,
            cantidad=cantidad,
            fecha=request.data.get("fecha")
        )

        Auditoria.objects.create(
            modelo='Venta',
            operacion='CREATE',
            id_registro=venta.id,
            datos_nuevos=json.dumps({
                "producto_id": producto.id,
                "producto_nombre": producto.nombre,
                "cliente_id": cliente.id,
                "cliente_nombre": cliente.nombre,
                "cantidad": cantidad,
                "fecha": venta.fecha
            }, default=str)
        )

        # Actualizar el inventario
        inventario.stock -= cantidad
        inventario.save()
          # Auditoría para Inventario (stock actualizado tras la venta)
        Auditoria.objects.create(
            modelo='Inventario',
            operacion='UPDATE',
            id_registro=inventario.id,
            datos_anteriores=json.dumps({
                "stock": inventario.stock + cantidad  # el valor anterior
            }, default=str),
            datos_nuevos=json.dumps({
                "stock": inventario.stock  # el nuevo valor ya actualizado
            }, default=str)
        )

        return Response({
            "id": venta.id,
            "fecha": venta.fecha,
            "cantidad": venta.cantidad,
            "producto_id": venta.producto.id,
            "cliente_id": venta.cliente.id,
            "mensaje": "Venta registrada y stock actualizado correctamente"
        }, status=status.HTTP_201_CREATED)

    
class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer


class ReporteMovimientosMensualesView(APIView):
    def get(self, request):
        mes = request.query_params.get('mes')   # formato: '2025-05'
        if not mes:
            return Response({"error": "Debe enviar el parámetro 'mes' (ejemplo: 2025-05)"}, status=400)
        
        try:
            year, month = map(int, mes.split('-'))
        except ValueError:
            return Response({"error": "Formato de mes inválido. Use 'YYYY-MM'"}, status=400)

        # Definir rango de fechas
        fecha_inicio = datetime(year, month, 1)
        if month == 12:
            fecha_fin = datetime(year + 1, 1, 1)
        else:
            fecha_fin = datetime(year, month + 1, 1)

        # Obtener ventas y compras en ese rango
        ventas = Venta.objects.filter(fecha__gte=fecha_inicio, fecha__lt=fecha_fin)
        compras = Compra.objects.filter(fecha__gte=fecha_inicio, fecha__lt=fecha_fin)

        total_ventas = ventas.aggregate(total=Sum('cantidad'))['total'] or 0
        total_compras = compras.aggregate(total=Sum('cantidad'))['total'] or 0

        ventas_detalle = [
            {
                "id": v.id,
                "fecha": v.fecha,
                "producto": v.producto.nombre,
                "cliente": v.cliente.nombre,
                "cantidad": v.cantidad
            } for v in ventas
        ]

        compras_detalle = [
            {
                "id": c.id,
                "fecha": c.fecha,
                "producto": c.producto.nombre,
                "cantidad": c.cantidad
            } for c in compras
        ]

        return Response({
            "mes": mes,
            "total_ventas": total_ventas,
            "total_compras": total_compras,
            "ventas": ventas_detalle,
            "compras": compras_detalle
        }, status=status.HTTP_200_OK)
        
class ProductosMasVendidosView(APIView):
    def get(self, request):
        mes = request.query_params.get('mes')  # formato esperado: 'YYYY-MM'

        if not mes:
            return Response({"error": "Debe enviar el parámetro 'mes' (ejemplo: 2025-05)"}, status=400)

        try:
            year, month = map(int, mes.split('-'))
        except ValueError:
            return Response({"error": "Formato de mes inválido. Use 'YYYY-MM'"}, status=400)

        # Definir rango de fechas
        fecha_inicio = datetime(year, month, 1)
        if month == 12:
            fecha_fin = datetime(year + 1, 1, 1)
        else:
            fecha_fin = datetime(year, month + 1, 1)

        # Consultar productos más vendidos en ese mes
        productos_vendidos = (
            Venta.objects.filter(fecha__gte=fecha_inicio, fecha__lt=fecha_fin)
            .values('producto__nombre')
            .annotate(cantidad_total=Sum('cantidad'))
            .order_by('-cantidad_total')[:15]  # top 15
        )

        # Armar lista con nombre legible
        resultado = [
            {
                "producto": item["producto__nombre"],
                "cantidad_total": item["cantidad_total"]
            }
            for item in productos_vendidos
        ]

        return Response({
            "mes": mes,
            "productos_mas_vendidos": resultado
        }, status=status.HTTP_200_OK)
        
class TopClientesView(APIView):
    def get(self, request):
        mes = request.query_params.get('mes')  # formato esperado: 'YYYY-MM'

        if not mes:
            return Response({"error": "Debe enviar el parámetro 'mes' (ejemplo: 2025-05)"}, status=400)

        try:
            year, month = map(int, mes.split('-'))
        except ValueError:
            return Response({"error": "Formato de mes inválido. Use 'YYYY-MM'"}, status=400)

        # Definir rango de fechas para ese mes
        fecha_inicio = datetime(year, month, 1)
        if month == 12:
            fecha_fin = datetime(year + 1, 1, 1)
        else:
            fecha_fin = datetime(year, month + 1, 1)

        # Consultar top 15 clientes por total ventas (cantidad * precio_venta) en ese rango
        clientes_top = (
            Venta.objects.filter(fecha__gte=fecha_inicio, fecha__lt=fecha_fin)
            .values('cliente__id', 'cliente__nombre')
            .annotate(
                total_ventas=Sum(F('cantidad') * F('producto__precio_venta'), output_field=FloatField())
            )
            .order_by('-total_ventas')[:15]
        )

        resultado = [
            {
                "cliente_id": item['cliente__id'],
                "nombre_cliente": item['cliente__nombre'],
                "total_ventas": round(item['total_ventas'], 2) if item['total_ventas'] else 0
            }
            for item in clientes_top
        ]

        return Response({
            "mes": mes,
            "top_clientes": resultado
        }, status=status.HTTP_200_OK)
        
class TopProveedoresView(APIView):
    def get(self, request):
        mes = request.query_params.get('mes')  # esperado 'YYYY-MM'

        if not mes:
            return Response({"error": "Debe enviar el parámetro 'mes' (ejemplo: 2025-05)"}, status=400)

        try:
            year, month = map(int, mes.split('-'))
        except ValueError:
            return Response({"error": "Formato de mes inválido. Use 'YYYY-MM'"}, status=400)

        fecha_inicio = datetime(year, month, 1)
        if month == 12:
            fecha_fin = datetime(year + 1, 1, 1)
        else:
            fecha_fin = datetime(year, month + 1, 1)

        proveedores_top = (
            Compra.objects.filter(fecha__gte=fecha_inicio, fecha__lt=fecha_fin)
            .values('proveedor__id', 'proveedor__nombre')
            .annotate(
                total_compras=Sum(F('cantidad') * F('producto__precio_compra'), output_field=FloatField())
            )
            .order_by('-total_compras')[:15]
        )

        resultado = [
            {
                "proveedor_id": item['proveedor__id'],
                "nombre_proveedor": item['proveedor__nombre'],
                "total_compras": round(item['total_compras'], 2) if item['total_compras'] else 0
            }
            for item in proveedores_top
        ]

        return Response({
            "mes": mes,
            "top_proveedores": resultado
        }, status=status.HTTP_200_OK)
        
class ReporteUtilidadesView(APIView):
    def get(self, request):
        mes = request.query_params.get('mes')  # Formato 'YYYY-MM'

        if not mes:
            return Response({"error": "Debe enviar el parámetro 'mes' (ejemplo: 2025-05)"}, status=400)

        try:
            year, month = map(int, mes.split('-'))
        except ValueError:
            return Response({"error": "Formato de mes inválido. Use 'YYYY-MM'"}, status=400)

        fecha_inicio = datetime(year, month, 1)
        fecha_fin = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

        # Total ventas (cantidad * precio_venta)
        ventas_total = Venta.objects.filter(fecha__gte=fecha_inicio, fecha__lt=fecha_fin) \
            .aggregate(total=Sum(F('cantidad') * F('producto__precio_venta'), output_field=FloatField()))['total'] or 0

        # Total costos (cantidad * precio_compra)
        costos_total = Compra.objects.filter(fecha__gte=fecha_inicio, fecha__lt=fecha_fin) \
            .aggregate(total=Sum(F('cantidad') * F('producto__precio_compra'), output_field=FloatField()))['total'] or 0

        utilidad = ventas_total - costos_total

        return Response({
            "mes": mes,
            "ventas_totales": round(ventas_total, 2),
            "costos_totales": round(costos_total, 2),
            "utilidad": round(utilidad, 2)
        }, status=status.HTTP_200_OK)

class ReporteComprasPorFechaView(APIView):
    def get(self, request):
        desde = request.query_params.get('desde')
        hasta = request.query_params.get('hasta')

        if not desde or not hasta:
            return Response({"error": "Debe enviar los parámetros 'desde' y 'hasta' en formato YYYY-MM-DD"}, status=400)

        try:
            fecha_desde = datetime.strptime(desde, "%Y-%m-%d")
            fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "Fechas inválidas. Formato requerido: YYYY-MM-DD"}, status=400)

        compras = Compra.objects.filter(fecha__range=(fecha_desde, fecha_hasta)).values(
            'fecha',
            'producto__nombre',
            'proveedor__nombre',
            'cantidad',
            'producto__precio_compra'
        ).order_by('fecha')

        resultado = []
        for c in compras:
            total = c['cantidad'] * c['producto__precio_compra']
            resultado.append({
                "fecha": c['fecha'].strftime("%Y-%m-%d"),  # formato string para JSON
                "producto": c['producto__nombre'],
                "proveedor": c['proveedor__nombre'],
                "cantidad": c['cantidad'],
                "total_comprado": total
            })

        return Response({
            "desde": desde,
            "hasta": hasta,
            "compras": resultado
        })
class ReporteVentasPorFechaView(APIView):
    def get(self, request):
        desde = request.query_params.get('desde')
        hasta = request.query_params.get('hasta')

        if not desde or not hasta:
            return Response({"error": "Debe enviar los parámetros 'desde' y 'hasta' en formato YYYY-MM-DD"}, status=400)

        try:
            fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date()
            fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Fechas inválidas. Formato requerido: YYYY-MM-DD"}, status=400)

        ventas = Venta.objects.filter(fecha__range=(fecha_desde, fecha_hasta)).values(
            'fecha',
            'producto__nombre',
            'cliente__nombre',
            'cantidad',
            'producto__precio_venta'
        ).order_by('fecha')

        resultado = []
        for v in ventas:
            total = v['cantidad'] * v['producto__precio_venta']
            resultado.append({
                "fecha": v['fecha'].strftime("%Y-%m-%d"),
                "producto": v['producto__nombre'],
                "cliente": v['cliente__nombre'],
                "cantidad": v['cantidad'],
                "total_venta": total
            })

        return Response({
            "desde": desde,
            "hasta": hasta,
            "ventas": resultado
        })

class CrearFacturaCompraView(APIView):
    def post(self, request, compra_id):
        try:
            compra = Compra.objects.get(id=compra_id)
        except Compra.DoesNotExist:
            return Response({"error": "Compra no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(compra, 'factura'):
            return Response({"error": "Factura ya generada para esta compra"}, status=status.HTTP_400_BAD_REQUEST)

        total = compra.cantidad * compra.producto.precio_compra  # Suponiendo que precio_compra existe en Producto
        nro_factura = str(uuid.uuid4())[:8].upper()  # Genera un nro factura único simple

        factura = Facturas.objects.create(
            nro_factura=nro_factura,
            tipo='compra',
            fecha=now().date(),
            total=total,
            compra=compra
        )
        return Response({"mensaje": "Factura creada", "factura_id": factura.id})

class CrearFacturaVentaView(APIView):
    def post(self, request, venta_id):
        try:
            venta = Venta.objects.get(id=venta_id)
        except Venta.DoesNotExist:
            return Response({"error": "Venta no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(venta, 'factura'):
            return Response({"error": "Factura ya generada para esta venta"}, status=status.HTTP_400_BAD_REQUEST)

        total = venta.cantidad * venta.producto.precio_venta  # Suponiendo que precio_venta existe en Producto
        nro_factura = str(uuid.uuid4())[:8].upper()

        factura = Facturas.objects.create(
            nro_factura=nro_factura,
            tipo='venta',
            fecha=now().date(),
            total=total,
            venta=venta
        )
        return Response({"mensaje": "Factura creada", "factura_id": factura.id})

class ListarFacturasView(APIView):
    def get(self, request):
        facturas = Facturas.objects.all().values('id', 'nro_factura', 'tipo', 'fecha', 'total')
        return Response(list(facturas))