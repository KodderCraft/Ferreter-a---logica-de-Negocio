from django.urls import path
from . import views
urlpatterns = [
    path('', views.ventas_index , name='ventas_index'),
    path('/importar_ventas', views.importar_ventas , name='importar_ventas'),
    path('/registrar_venta', views.registrar_venta , name='registrar_venta'),
    path('/detalle/<int:id>/', views.detalle_venta, name='detalle_venta'),
    path('/eliminar/<int:id>/', views.eliminar_venta, name='eliminar_venta'),
    path('ventas/confirmar-pago/<int:id>/', views.cambiar_estado_venta, name='confirmar_pago'),

]