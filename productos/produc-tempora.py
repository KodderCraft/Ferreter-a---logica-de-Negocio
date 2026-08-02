from .models import Producto

# Producto 1
Producto.objects.create(
    nombre_producto="Laptop Gamer Lenovo Legion 5",
    descripsion_producto="Pantalla 15.6 FHD 144Hz, AMD Ryzen 7, 16GB RAM, 512GB SSD, RTX 3060",
    categoria_producto="Tecnología",
    precio_producto=1250.00,
    stock_producto=10,
    ventas_producto=3,
    activo=True
)

# Producto 2
Producto.objects.create(
    nombre_producto="Auriculares Inalámbricos Sony WH-1000XM5",
    descripsion_producto="Cancelación de ruido activa, autonomía de 30 horas, Bluetooth 5.2",
    categoria_producto="Audio",
    precio_producto=399.99,
    stock_producto=25,
    ventas_producto=12,
    activo=True
)

# Producto 3
Producto.objects.create(
    nombre_producto="Silla Ergonómica de Oficina",
    descripsion_producto="Malla transpirable, soporte lumbar ajustable, reclinable 135 grados",
    categoria_producto="Muebles",
    precio_producto=185.50,
    stock_producto=8,
    ventas_producto=5,
    activo=True
)