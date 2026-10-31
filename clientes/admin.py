from django.contrib import admin
from .models import Empresa, Cliente, Interaccion

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'direccion']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'empresa', 'asignado_a']
    list_filter = ['empresa', 'asignado_a']

@admin.register(Interaccion)
class InteraccionAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'trabajador', 'fecha']