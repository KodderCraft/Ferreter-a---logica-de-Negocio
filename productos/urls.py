from django.urls import path

from . import views

# Rutas del CRUD de productos. A diferencia de ventas/urls.py, aqui NO se
# usa un '/' al inicio de cada ruta: ese estilo rompe la generacion de URLs
# con {% url %}/reverse() cuando el include() padre usa un prefijo (ver
# config/urls.py), asi que se evita desde el principio.
urlpatterns = [
    path('', views.productos_index, name='productos_index'),
]
