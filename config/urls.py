"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Módulo de ventas
    path('', include('ventas.urls')),

    # Módulo de empleados
    path('empleados/', include('empleados.urls')),

    # Módulo de productos
    path('productos/', include('productos.urls')),

    # Módulo de clientes
    path('clientes/', include('clientes.urls')),
]