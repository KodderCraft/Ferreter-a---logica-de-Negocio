from decimal import Decimal

from django.test import TestCase

from empleados.models import Empleado
from productos.models import Producto
from .models import DetalleVenta, Venta


class VentaEmpleadoIntegrationTest(TestCase):
    def test_venta_puede_guardar_empleado_y_calcular_total(self):
        empleado = Empleado.objects.create(
            nombre_empleado="Juan",
            apellido_empleado="Pérez",
            cedula_empleado="1234567890",
            correo_empleado="juan@test.com",
            telefono_empleado="0999999999",
            cargo_empleado="Vendedor",
            salario_empleado=Decimal("800.00"),
            fecha_ingreso="2024-01-01",
            activo=True,
        )
        producto = Producto.objects.create(
            nombre_producto="Taladro",
            descripsion_producto="Taladro básico",
            categoria_producto="Herramientas",
            precio_producto=Decimal("10.00"),
            stock_producto=10,
            ventas_producto=0,
            activo=True,
        )

        venta = Venta.objects.create(estado_venta="PAGADA", empleado=empleado)
        DetalleVenta.objects.create(venta=venta, producto=producto, cantidad=2)

        venta.refresh_from_db()

        self.assertEqual(venta.empleado, empleado)
        self.assertEqual(venta.total_venta, Decimal("23.00"))
