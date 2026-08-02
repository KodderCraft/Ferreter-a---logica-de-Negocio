from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
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


def editar_producto(request, id):
    """
    Actualiza (Update) un producto existente.

    Reusa exactamente el mismo template que crear_producto
    (producto_form.html); la unica diferencia es que el form se crea
    con 'instance=producto' para que salga precargado, y que al guardar
    no se toca 'fecha_producto' (esa fecha es la de creacion, no la de
    la ultima edicion).
    """
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡Producto '{producto.nombre_producto}' actualizado exitosamente!")
            return redirect("productos_index")
        messages.error(request, "Revisa los datos del formulario, hay errores.")
    else:
        form = ProductoForm(instance=producto)

    return render(
        request,
        "productos/producto_form.html",
        {"form": form, "titulo": f"Editar Producto: {producto.nombre_producto}"},
    )


def eliminar_producto(request, id):
    """
    "Elimina" (Delete) un producto -- en realidad lo desactiva.

    Nunca se llama producto.delete(): Producto tiene un ForeignKey desde
    DetalleVenta con on_delete=CASCADE, asi que borrar de verdad un
    producto con ventas asociadas destruiria ese historial de ventas.
    En su lugar, este CRUD usa el campo 'activo' que ya existia en el
    modelo (y que 'ventas.views.registrar_venta' ya usa para filtrar
    el combo de productos disponibles): desactivar un producto hace que
    deje de ofrecerse para nuevas ventas, sin tocar lo ya vendido.

    GET: muestra una pantalla de confirmacion.
    POST: pone activo=False y redirige al listado.
    """
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        producto.activo = False
        producto.save()
        messages.success(request, f"El producto '{producto.nombre_producto}' fue desactivado.")
        return redirect("productos_index")

    return render(request, "productos/producto_confirm_delete.html", {"producto": producto})


def activar_producto(request, id):
    """
    Reactiva un producto previamente desactivado (activo=True).

    Es un toggle simple via GET+redirect, igual que
    'ventas.views.cambiar_estado_venta': no hace falta pantalla de
    confirmacion porque reactivar no tiene ningun efecto destructivo.
    """
    producto = get_object_or_404(Producto, id=id)
    producto.activo = True
    producto.save()
    messages.success(request, f"El producto '{producto.nombre_producto}' fue reactivado.")
    return redirect("productos_index")
