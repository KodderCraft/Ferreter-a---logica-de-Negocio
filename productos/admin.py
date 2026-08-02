from django.contrib import admin

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Vista secundaria del inventario dentro de /admin/, util para
    correcciones rapidas de datos (por ejemplo activar/desactivar varios
    productos desde la lista) sin pasar por el CRUD publico.
    """

    list_display = (
        "id",
        "nombre_producto",
        "categoria_producto",
        "precio_producto",
        "stock_producto",
        "ventas_producto",
        "activo",
    )
    list_filter = ("activo", "categoria_producto")
    search_fields = ("nombre_producto",)
    list_editable = ("activo",)
