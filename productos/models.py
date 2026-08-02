from django.db import models

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=300)
    descripsion_producto = models.TextField(blank=True, null=True)
    categoria_producto = models.CharField(max_length=100)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    stock_producto = models.IntegerField()
    ventas_producto = models.IntegerField(default=0)
    fecha_producto = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    # Distinto de 'activo': 'activo' controla si se puede vender: 'oculto'
    # controla si aparece en el listado del CRUD. Un producto desactivado
    # se puede "Eliminar" desde la lista, lo que solo pone oculto=True
    # (nunca se borra la fila de la base de datos, para no perder su
    # historial de ventas via el CASCADE de DetalleVenta.producto).
    oculto = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_producto  
    

