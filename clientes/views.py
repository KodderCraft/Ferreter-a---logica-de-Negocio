from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm


# CONSULTAR
def lista_clientes(request):

    clientes = Cliente.objects.all()

    return render(request,
                 'clientes/lista.html',
                 {'clientes': clientes})


# REGISTRAR
def crear_cliente(request):

    if request.method == 'POST':

        formulario = ClienteForm(request.POST)

        if formulario.is_valid():

            formulario.save()

            return redirect('lista_clientes')

    else:

        formulario = ClienteForm()

    return render(request,
                  'clientes/formulario.html',
                  {'formulario': formulario})


# ACTUALIZAR
def editar_cliente(request,id):

    cliente = get_object_or_404(Cliente,id=id)

    if request.method=="POST":

        formulario = ClienteForm(request.POST,instance=cliente)

        if formulario.is_valid():

            formulario.save()

            return redirect('lista_clientes')

    else:

        formulario = ClienteForm(instance=cliente)

    return render(request,
                  'clientes/formulario.html',
                  {'formulario':formulario})


# ELIMINAR
def eliminar_cliente(request,id):

    cliente = get_object_or_404(Cliente,id=id)

    cliente.delete()

    return redirect('lista_clientes')