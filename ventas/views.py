from decimal import Decimal
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

# Importa tus modelos y formularios
from productos.models import Producto
from .models import Venta, DetalleVenta
from .forms import CSVForm

# from clientes.models import Cliente
from empleados.models import Empleado


def ventas_index(request):
    ventas = Venta.objects.all().order_by("-fecha_venta")
    return render(request, 'ventas/ventas_index.html' , {"ventas": ventas})

def cambiar_estado_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    
    # Cambiamos el estado a PAGADA
    venta.estado_venta = 'PAGADA'
    venta.save()
    
    messages.success(request, f"¡El estado de la Venta #{venta.id} se actualizó a PAGADA!")
    return redirect('ventas_index') # o 'ventas_index' según el nombre en tu urls.py

def registrar_venta(request):

    productos = Producto.objects.filter(activo=True)
    empleados_disponibles = Empleado.objects.filter(activo=True).order_by("id_empleado")

    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        cantidad_str = request.POST.get("cantidad", 0)
        empleado_id = request.POST.get("empleado_id")

        try:
            cantidad = int(cantidad_str)
        except (ValueError, TypeError):
            cantidad = 0

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            messages.error(request, "El producto seleccionado no existe.")
            return redirect("registrar_venta")

        empleado = None
        if empleado_id:
            try:
                empleado = Empleado.objects.get(id_empleado=empleado_id)
            except Empleado.DoesNotExist:
                messages.error(request, "El empleado seleccionado no existe.")
                return render(
                    request,
                    "ventas/registrar_venta.html",
                    {"productos": productos, "empleados": empleados_disponibles},
                )

        if cantidad <= 0:
            messages.error(request, "Por favor, ingrese una cantidad válida mayor a 0.")
            return render(
                request,
                "ventas/registrar_venta.html",
                {"productos": productos, "empleados": empleados_disponibles},
            )

        if producto.stock_producto < cantidad:
            messages.error(
                request,
                f"Stock insuficiente para '{producto.nombre_producto}'. Solo quedan {producto.stock_producto} unidades.",
            )
            return render(
                request,
                "ventas/registrar_venta.html",
                {"productos": productos, "empleados": empleados_disponibles},
            )

        try:
            with transaction.atomic():
                estado = request.POST.get("estado_venta", "PAGADA")
                venta = Venta.objects.create(
                    total_venta=0.00,
                    estado_venta=estado,
                    empleado=empleado,
                )

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                )

            messages.success(request, f"¡Venta #{venta.id} registrada exitosamente!")
            return redirect("ventas_index")

        except Exception as e:
            messages.error(
                request, f"Ocurrió un error inesperado al procesar la venta: {str(e)}"
            )
            return render(
                request,
                "ventas/registrar_venta.html",
                {"productos": productos, "empleados": empleados_disponibles},
            )

    return render(
        request,
        "ventas/registrar_venta.html",
        {"productos": productos, "empleados": empleados_disponibles},
    )




def detalle_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    return render(
        request,
        "ventas/detalle_venta.html",
        {
            "venta": venta,
            "detalles": venta.detalles.all(),
        },
    )


def eliminar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)

    try:
        with transaction.atomic():
            # Devuelve el stock e incrementa/restringe las ventas del producto
            for detalle in venta.detalles.all():
                producto = detalle.producto
                producto.stock_producto += detalle.cantidad
                producto.ventas_producto = max(0, producto.ventas_producto - detalle.cantidad)
                producto.save()

            # Elimina la venta (y en cascada elimina los detalles)
            venta.delete()

        messages.success(
            request, f"La venta #{id} fue eliminada y el stock ha sido devuelto al inventario."
        )
    except Exception as e:
        messages.error(
            request, f"No se pudo eliminar la venta #{id}: {str(e)}"
        )

    return redirect("ventas_index")


def importar_ventas(request):
    formulario = CSVForm()
    if request.method == 'POST':
        formulario = CSVForm(request.POST, request.FILES)
        if formulario.is_valid():
            archivo = request.FILES['archivo']
            try:
                df = pd.read_csv(archivo)

                with transaction.atomic():
                    for _, fila in df.iterrows():
                        producto = Producto.objects.get(id=int(fila['producto_id']))
                        cantidad = int(fila['cantidad'])
                        empleado_id = int(fila.get('empleado_id', 0))

                        empleado = None
                        if empleado_id:
                            empleado = Empleado.objects.get(id_empleado=empleado_id)

                        if producto.stock_producto >= cantidad:
                            venta = Venta.objects.create(
                                total_venta=0.00,
                                estado_venta=str(fila.get('estado_venta', 'PAGADA')).upper(),
                                empleado=empleado,
                            )
                            DetalleVenta.objects.create(
                                venta=venta,
                                producto=producto,
                                cantidad=cantidad,
                            )

                messages.success(request, 'Ventas importadas exitosamente desde CSV')
                return redirect('ventas_index')
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo CSV: {str(e)}')
        else:
            messages.error(request, 'Error al cargar el archivo')

    return render(request, 'ventas/importar_ventas.html', {'formulario': formulario})
