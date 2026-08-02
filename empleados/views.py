from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado
from .forms import EmpleadoForm
from django.contrib import messages
from django.core.paginator import Paginator


from django.db.models import Q


def empleados_index(request):

    buscar = request.GET.get('buscar')

    empleados = Empleado.objects.all().order_by('id_empleado')

    if buscar:
        empleados = empleados.filter(
            Q(nombre_empleado__icontains=buscar) |
            Q(apellido_empleado__icontains=buscar) |
            Q(cedula_empleado__icontains=buscar) |
            Q(cargo_empleado__icontains=buscar)
        )

    paginador = Paginator(empleados, 5)

    numero_pagina = request.GET.get('page')

    empleados = paginador.get_page(numero_pagina)

    return render(request, 'empleados/index.html', {
        'empleados': empleados,
        'total_empleados': Empleado.objects.count(),
        'empleados_activos': Empleado.objects.filter(activo=True).count(),
        'empleados_inactivos': Empleado.objects.filter(activo=False).count(),
    })

def crear_empleado(request):
    if request.method == 'POST':
        formulario = EmpleadoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Empleado registrado correctamente.')
            return redirect('empleados_index')
    else:
        formulario = EmpleadoForm()

    return render(request, 'empleados/formulario.html', {
        'formulario': formulario
    })


def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id_empleado=id)

    if request.method == 'POST':
        formulario = EmpleadoForm(request.POST, instance=empleado)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Empleado actualizado correctamente.')
            return redirect('empleados_index')
    else:
        formulario = EmpleadoForm(instance=empleado)

    return render(request, 'empleados/formulario.html', {
        'formulario': formulario
    })
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id_empleado=id)

    empleado.delete()
    messages.success(request, 'Empleado eliminado correctamente.')

    return redirect('empleados_index')