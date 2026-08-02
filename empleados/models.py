from django.db import models


class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre_empleado = models.CharField(max_length=100)
    apellido_empleado = models.CharField(max_length=100)
    cedula_empleado = models.CharField(max_length=10, unique=True)
    correo_empleado = models.EmailField(unique=True)
    telefono_empleado = models.CharField(max_length=10)
    cargo_empleado = models.CharField(max_length=100)
    salario_empleado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_empleado} {self.apellido_empleado}"