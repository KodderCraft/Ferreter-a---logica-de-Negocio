from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ProductoForm
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


def crear_producto(request):
    """
    Crea (Create) un nuevo producto.

    GET: muestra el formulario vacio.
    POST: valida los datos con ProductoForm; si son validos, guarda el
    producto (poniendole la fecha actual, ya que no se pide en el form)
    y redirige al listado con un mensaje de exito. Si no son validos,
    vuelve a mostrar el mismo formulario con los errores.
    """
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.fecha_producto = timezone.now()
            producto.save()
            messages.success(request, f"¡Producto '{producto.nombre_producto}' creado exitosamente!")
            return redirect("productos_index")
        messages.error(request, "Revisa los datos del formulario, hay errores.")
    else:
        form = ProductoForm()

    return render(
        request,
        "productos/producto_form.html",
        {"form": form, "titulo": "Nuevo Producto"},
    )
