from django.urls import path
from . import views
urlpatterns = [
    path('', views.ventas_index , name='ventas_index'),
    path('/importar_ventas', views.importar_ventas , name='importar_ventas'),
    path('/registrar_venta', views.registrar_venta , name='registrar_venta'),
]