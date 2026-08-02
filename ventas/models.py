from django.db import models
from decimal import Decimal
from productos.models import Producto  # Tu modelo original de Producto
# from clientes.models import Cliente     # Importa tu modelo de Cliente
# from empleados.models import Empleado

class Venta(models.Model):
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # cliente = models.ForeignKey(
    #     Cliente, 
    #     on_delete=models.SET_NULL, 
    #     null=True, 
    #     related_name="ventas"
    # )
    # empleado = models.ForeignKey(
    #     Empleado, 
    #     on_delete=models.SET_NULL, 
    #     null=True, 
    #     related_name="ventas"
    # )

    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADA', 'Pagada')
    ]

    estado_venta = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
       
    )

def __str__(self):
    return f"Venta #{self.id} - Total: ${self.total_venta} - Cliente: {self.cliente} - Vendedor: {self.empleado}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True  # Se llena automáticamente con el precio del Producto
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True
    )

    iva = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True
    )

    def save(self, *args, **kwargs):
        # 1. Si no especificaste precio, toma automáticamente el precio_producto de tu modelo
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio_producto

        # 2. Cálculo del subtotal e IVA (15%)
        self.subtotal = self.cantidad * self.precio_unitario
        self.iva = self.subtotal * Decimal("0.15")

        # 3. Validar y actualizar el Stock y las Ventas en el modelo Producto
        # Si es un nuevo detalle de venta (no una edición existente)
        if not self.pk:
            if self.producto.stock_producto >= self.cantidad:
                # Descontar stock y sumar a las ventas acumuladas
                self.producto.stock_producto -= self.cantidad
                self.producto.ventas_producto += self.cantidad
                self.producto.save()
            else:
                raise ValueError(f"Stock insuficiente para {self.producto.nombre_producto}. Disponible: {self.producto.stock_producto}")

        # 4. Guardar el registro del detalle
        super().save(*args, **kwargs)

        # 5. Recalcular el total acumulado en la Venta principal
        total = sum(
            detalle.subtotal + detalle.iva
            for detalle in self.venta.detalles.all()
        )
        self.venta.total_venta = total
        self.venta.save()

    def __str__(self):
        return f"Detalle #{self.id} - Producto: {self.producto.nombre_producto} (x{self.cantidad})"
# from django.db import models
# from decimal import Decimal
# from productos.models import Producto


# class Venta(models.Model):
#     fecha_venta = models.DateTimeField(auto_now_add=True)
#     total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     estado_venta = models.CharField(
#         max_length=20,
#         choices=[
#             ('PENDIENTE', 'Pendiente'),
#             ('PAGADA', 'Pagada')
#         ],
#         default='PAGADA'
#     )

#     def __str__(self):
#         return f"Venta #{self.id}"


# class DetalleVenta(models.Model):
#     venta = models.ForeignKey(
#         Venta,
#         on_delete=models.CASCADE,
#         related_name='detalles'
#     )

#     producto = models.ForeignKey(
#         Producto,
#         on_delete=models.CASCADE
#     )

#     cantidad = models.PositiveIntegerField()

#     precio_unitario = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )

#     subtotal = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         blank=True
#     )

#     iva = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         blank=True
#     )

#     def save(self, *args, **kwargs):
#         self.subtotal = self.cantidad * self.precio_unitario
#         self.iva = self.subtotal * Decimal("0.15")

#         super().save(*args, **kwargs)

#         total = sum(
#             detalle.subtotal + detalle.iva
#             for detalle in self.venta.detalles.all()
#         )

#         self.venta.total_venta = total
#         self.venta.save()

#     def __str__(self):
#         return f"Detalle #{self.id} - Venta #{self.venta.id}"
