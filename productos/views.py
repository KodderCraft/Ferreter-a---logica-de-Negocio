from django.shortcuts import render

from .models import Producto


def productos_index(request):
    """
    Lista (Read) todos los productos, activos e inactivos.

    El campo 'activo' no se usa para filtrar aqui: la idea es que
    esta pantalla sea el panel de control completo del inventario,
    y sea la plantilla la que distinga visualmente (con un badge)
    cuales productos estan disponibles para la venta y cuales fueron
    desactivados (ver 'eliminar_producto' mas adelante en este archivo).
    """
    productos = Producto.objects.all().order_by("-id")
    return render(request, "productos/productos_index.html", {"productos": productos})
