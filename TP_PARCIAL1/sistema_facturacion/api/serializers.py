# serializers.py
from rest_framework import serializers
from .models import Cliente, Producto, Factura, Proveedor, Reporte, Compra, Inventario

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
    
    def create(self, validated_data):
        producto = super().create(validated_data)
        Inventario.objects.create(producto=producto, stock=0)
        return producto

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'
        
    def create(self, validated_data):
        compra = super().create(validated_data)
        producto = validated_data['producto']
        cantidad = validated_data.get('cantidad', 0)

        # Actualizar o crear el inventario
        inventario, created = Inventario.objects.get_or_create(producto=producto)
        inventario.stock += cantidad
        inventario.save()
        
        return compra

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'
