from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    """
    Formulario de creacion/edicion de un Producto.

    Se excluyen a proposito dos campos del modelo:
    - 'ventas_producto': solo lo actualiza DetalleVenta.save() cuando se
      registra una venta, nunca debe editarse a mano desde este form.
    - 'activo': se maneja aparte con las vistas eliminar_producto /
      activar_producto (borrado logico), para no tener dos controles
      distintos (el form y el boton de la lista) cambiando lo mismo.
    'fecha_producto' tampoco aparece aqui: la vista de creacion la llena
    sola con la fecha/hora actual.
    """

    class Meta:
        model = Producto
        fields = [
            "nombre_producto",
            "descripsion_producto",
            "categoria_producto",
            "precio_producto",
            "stock_producto",
        ]
        labels = {
            "nombre_producto": "Nombre del Producto",
            "descripsion_producto": "Descripcion",
            "categoria_producto": "Categoria",
            "precio_producto": "Precio ($)",
            "stock_producto": "Stock disponible",
        }
        widgets = {
            "nombre_producto": forms.TextInput(attrs={"class": "form-control"}),
            "descripsion_producto": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "categoria_producto": forms.TextInput(attrs={"class": "form-control"}),
            "precio_producto": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "stock_producto": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }

    def clean_precio_producto(self):
        # El modelo no impone que el precio sea positivo; se valida aqui
        # para no permitir productos con precio negativo desde el form.
        precio = self.cleaned_data["precio_producto"]
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_stock_producto(self):
        # Mismo caso que el precio: el modelo permite cualquier entero,
        # aqui se restringe a valores no negativos.
        stock = self.cleaned_data["stock_producto"]
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock
