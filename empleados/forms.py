from django import forms
from .models import Empleado


class EmpleadoForm(forms.ModelForm):

    class Meta:
        model = Empleado
        fields = [
            'nombre_empleado',
            'apellido_empleado',
            'cedula_empleado',
            'correo_empleado',
            'telefono_empleado',
            'cargo_empleado',
            'salario_empleado',
            'fecha_ingreso',
            'activo',
        ]

        widgets = {
            'nombre_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_empleado': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            'salario_empleado': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }