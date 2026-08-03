from django.db import models

class Cliente(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=200)
    correo = models.EmailField()

    def __str__(self):
        return self.nombres