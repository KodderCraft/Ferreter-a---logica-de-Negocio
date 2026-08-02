from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ProductoForm
from .models import Producto


def productos_index(request):
    """
    Lista (Read) los productos que no fueron ocultados.

    El campo 'activo' no se usa para filtrar aqui a proposito: la idea
    es que esta pantalla siga mostrando tanto los productos disponibles
    para la venta como los desactivados (la plantilla los distingue con
    un badge), para poder reactivarlos facilmente. 'oculto' es distinto:
    un producto oculto ya no aparece en esta lista para nada (ver
    'ocultar_producto' mas abajo), aunque su fila sigue intacta en la
    base de datos -- solo se puede volver a ver desde /admin/.
    """
    productos = Producto.objects.filter(oculto=False).order_by("-id")
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


def ocultar_producto(request, id):
    """
    Boton "Eliminar" de la lista -- solo visible para productos ya
    desactivados (ver productos_index.html). Igual que eliminar_producto,
    NUNCA llama producto.delete(): solo pone oculto=True, que hace que
    productos_index deje de traerlo en su queryset. La fila sigue
    completa en la base de datos (recuperable desde /admin/, ver
    ProductoAdmin en admin.py) para no perder su historial de ventas.

    GET: muestra una pantalla de confirmacion.
    POST: pone oculto=True y redirige al listado.
    """
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        producto.oculto = True
        producto.save()
        messages.success(request, f"El producto '{producto.nombre_producto}' fue eliminado de la lista.")
        return redirect("productos_index")

    return render(request, "productos/producto_confirm_ocultar.html", {"producto": producto})
