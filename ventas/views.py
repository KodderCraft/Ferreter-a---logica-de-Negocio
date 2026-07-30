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
# from empleados.models import Empleado


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

    if request.method == "POST":
        producto_id = request.POST.get("producto_id")
        cantidad_str = request.POST.get("cantidad", 0)  
        # clientes = Cliente.objects.all()      # Cargar lista de clientes
        # empleados = Empleado.objects.all()

        try:
            cantidad = int(cantidad_str)
        except (ValueError, TypeError):
            cantidad = 0

        # 1. Validar selección de producto
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            messages.error(request, "El producto seleccionado no existe.")
            return redirect("registrar_venta")

        # 2. Validar cantidad introducida
        if cantidad <= 0:
            messages.error(request, "Por favor, ingrese una cantidad válida mayor a 0.")
            return render(
                request,
                "ventas/registrar_venta.html",
                {"productos": productos},
            )

        # 3. Validar disponibilidad en inventario
        if producto.stock_producto < cantidad:
            messages.error(
                request,
                f"Stock insuficiente para '{producto.nombre_producto}'. Solo quedan {producto.stock_producto} unidades.",
            )
            return render(
                request,
                "ventas/registrar_venta.html",
                {"productos": productos},
            )

        try:
            with transaction.atomic():
                # Crear la Venta (el total se calculará al guardar el detalle)
                estado = request.POST.get("estado_venta", "PAGADA")
                venta = Venta.objects.create(total_venta=0.00,estado_venta=estado,
                                            #  cliente=cliente_obj,    
                                            # empleado=empleado_obj
                                            )

                # Crear el DetalleVenta:
                # El método save() del modelo se encargará automáticamente de:
                # - Asignar precio_unitario, subtotal e IVA
                # - Descontar el stock_producto y sumar a ventas_producto
                # - Actualizar el total_venta en la cabecera Venta
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad
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
                {"productos": productos
                #  ,"clientes": clientes,
                # "empleados": empleados
                },
            )

    return render(
        request, "ventas/registrar_venta.html", {"productos": productos}
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
                        # Obtener producto por ID o Nombre desde la fila del CSV
                        producto = Producto.objects.get(id=int(fila['producto_id']))
                        cantidad = int(fila['cantidad'])

                        if producto.stock_producto >= cantidad:
                            venta = Venta.objects.create(total_venta=0.00)
                            DetalleVenta.objects.create(
                                venta=venta,
                                producto=producto,
                                cantidad=cantidad
                            )

                messages.success(request, 'Ventas importadas exitosamente desde CSV')
                return redirect('listar_ventas')
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo CSV: {str(e)}')
        else:
            messages.error(request, 'Error al cargar el archivo')

    return render(request, 'ventas/importar_ventas.html', {'formulario': formulario})

# from django.shortcuts import render , redirect
# from decimal import Decimal
# from django.contrib import messages
# from django.db import transaction
# # from productos.models import Producto
# from ventas.models import DetalleVenta, Venta
# from .forms import CSVForm
# from pandas import read_csv
# import pandas as pd 

# # Create your views here.
# def ventas_index(request):
#     ventas = Venta.objects.all().order_by("-fecha_venta")
#     return render(request, 'ventas/ventas_index.html' , {"ventas": ventas})

# def importar_ventas(request):

#     formulario = CSVForm
#     # if request.method == 'POST':
#     #     formulario = CSVForm(request.POST, request.FILES)
#     #     if formulario.is_valid():
#     #         archivo = request.FILES['archivo']
#     #         df = pd.read_csv(archivo)
#     #         for _, fila in df.iterrows():
#     #             Venta.objects.create_user(
#     #                 # faltaData
#     #             )
#     #         messages.success(request, 'Usuarios Agregados')
#     #         return redirect('usuarios_index')
#     #     else:
#     #         messages.error(request , 'Error al cargar datos ')

#     return render(request , 'ventas/importar_ventas.html' , {'formulario':formulario})




# def registrar_venta(request):
#     return render(request, 'ventas/registrar_venta.html')



# def index_ventas(request):
#     """Muestra la vista principal del módulo de ventas."""
#     ventas = Venta.objects.all().order_by("-fecha_venta")
#     return render(request, "ventas/index_ventas.html", {"ventas": ventas})


# def registrar_venta(request):
#     productos = Producto.objects.filter(activo=True)

#     if request.method == "POST":
#         producto_id = request.POST.get("producto_id")
#         cantidad_str = request.POST.get("cantidad", 0)

#         try:
#             cantidad = int(cantidad_str)
#         except (ValueError, TypeError):
#             cantidad = 0

#         # Validar selección de producto
#         try:
#             producto = Producto.objects.get(id=producto_id)
#         except Producto.DoesNotExist:
#             messages.error(request, "El producto seleccionado no existe.")
#             return redirect("registrar_venta")

#         # Validar cantidad introducida
#         if cantidad <= 0:
#             messages.error(request, "Por favor, ingrese una cantidad válida mayor a 0.")
#             return render(
#                 request,
#                 "ventas/registrar_ventas.html",
#                 {"productos": productos},
#             )

#         # Validar disponiblidad en inventario
#         if producto.stock_producto < cantidad:
#             messages.error(
#                 request,
#                 f"Stock insuficiente para '{producto.nombre_producto}'. Solo quedan {producto.stock_producto} unidades.",
#             )
#             return render(
#                 request,
#                 "ventas/registrar_ventas.html",
#                 {"productos": productos},
#             )

#         try:
#             with transaction.atomic():
#                 # 1. Descontar stock e incrementar contador de ventas
#                 producto.stock_producto -= cantidad
#                 producto.ventas_producto += cantidad
#                 producto.save()

#                 # 2. Calcular valores de la transacción
#                 precio_u = producto.precio_producto
#                 subtotal = precio_u * Decimal(cantidad)
#                 iva = subtotal * Decimal("0.15")  # Tasa del 15% de IVA
#                 total = subtotal + iva

#                 # 3. Crear cabecera de la venta
#                 venta = Venta.objects.create(total_venta=total)

#                 # 4. Crear detalle individual
#                 DetalleVenta.objects.create(
#                     venta=venta,
#                     producto=producto,
#                     cantidad=cantidad,
#                     precio_unitario=precio_u,
#                     subtotal=subtotal,
#                     iva=iva,
#                 )

#             # Notificación de éxito para SweetAlert2
#             messages.success(request, f"¡Venta #{venta.id} registrada exitosamente!")
#             return redirect("listar_ventas")

#         except Exception as e:
#             messages.error(
#                 request, f"Ocurrió un error inesperado al procesar la venta: {str(e)}"
#             )
#             return render(
#                 request,
#                 "ventas/registrar_ventas.html",
#                 {"productos": productos},
#             )

#     return render(
#         request, "ventas/registrar_ventas.html", {"productos": productos}
#     )


# def listar_ventas(request):
#     ventas = Venta.objects.all().order_by("-fecha_venta")
#     return render(
#         request,
#         "ventas/listar_ventas.html",
#         {"ventas": ventas},
#     )


# def detalle_venta(request, id):
#     venta = get_object_or_404(Venta, id=id)
#     return render(
#         request,
#         "ventas/detalles.html",
#         {
#             "venta": venta,
#             "detalles": venta.detalles.all(),
#         },
#     )


# def eliminar_venta(request, id):

#     venta = get_object_or_404(Venta, id=id)

#     try:
#         with transaction.atomic():
#             # Restaurar el stock de los productos involucrados
#             for detalle in venta.detalles.all():
#                 producto = detalle.producto
#                 producto.stock_producto += detalle.cantidad
#                 producto.ventas_producto = max(0, producto.ventas_producto - detalle.cantidad)
#                 producto.save()

#             # Eliminar la venta y sus detalles asociados
#             venta.delete()

#         # Alerta de éxito al eliminar
#         messages.success(
#             request, f"La venta #{id} fue eliminada y el stock ha sido devuelto al inventario."
#         )
#     except Exception as e:
#         messages.error(
#             request, f"No se pudo eliminar la venta #{id}: {str(e)}"
#         )

#     return redirect("listar_ventas")

