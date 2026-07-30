from django.shortcuts import render

# Create your views here.
def ventas_index(request):
    return render(request, 'ventas/ventas_index.html')

def importar_ventas(request):
    return render(request, 'ventas/importar_ventas.html')

def registrar_venta(request):
    return render(request, 'ventas/registrar_venta.html')