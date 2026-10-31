from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=16)    
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre}'

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=16)
    email = models.EmailField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="clientes")
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="clientes_asignados")

    def __str__(self):
        return f'{self.nombre}'

class Interaccion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="interacciones")
    trabajador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="interacciones")
    fecha = models.DateTimeField()
    notas = models.TextField(max_length=500)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f'{self.cliente} de {self.cliente.empresa} ({self.trabajador})'


