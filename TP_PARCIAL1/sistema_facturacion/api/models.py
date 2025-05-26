from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.numero

class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    contenido = models.TextField()

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField(default=1)  # <- Nuevo campo

    def __str__(self):
        return f"Compra de {self.cantidad} x {self.producto.nombre} por {self.proveedor.nombre} en {self.fecha}"

class Venta(models.Model):
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='producto_id')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='cliente_id')

    def __str__(self):
        return f"Venta #{self.id} - Producto: {self.producto.nombre} - Cliente: {self.cliente.nombre}"
    
class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='inventario')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.producto.nombre}: {self.stock} unidades"

class Auditoria(models.Model):
    modelo = models.CharField(max_length=100)
    operacion = models.CharField(max_length=10)  # 'CREATE', 'UPDATE', 'DELETE'
    datos_anteriores = models.TextField(null=True, blank=True)
    datos_nuevos = models.TextField(null=True, blank=True)
    id_registro = models.IntegerField(null=True, blank=True)  # ID del objeto auditado
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} - {self.operacion} en {self.modelo} (ID {self.id_registro})"