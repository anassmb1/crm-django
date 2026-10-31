from django.contrib import admin
from django.urls import path
from clientes.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', VistaHome.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('clientes/', ClientesView.as_view(), name="lista_clientes"),
    path('clientes/crear/', CrearClienteView.as_view(), name="crear_cliente"),
    path('clientes/<pk>/', DetalleClienteView.as_view(), name="detalle_cliente"),
    path('clientes_editar/<pk>/', EditarClienteView.as_view(), name="editar_cliente"),
    path('clientes_borrar/<pk>/', BorrarClienteView.as_view(), name="borrar_cliente"),
    path('empresas/', EmpresasView.as_view(), name="lista_empresas"),
    path('empresas/crear/', CrearEmpresaView.as_view(), name="crear_empresa"),
    path('empresas/<pk>/', DetalleEmpresaView.as_view(), name="detalle_empresa"),
    path('empresas_editar/<pk>/', EditarEmpresaView.as_view(), name="editar_empresa"),
    path('empresas_borrar/<pk>/', BorrarEmpresaView.as_view(), name="borrar_empresa"),
    path('clientes/<pk>/interaccion/crear', CrearInteraccionView.as_view(), name="crear_interaccion"),
    path('interacciones/<pk>/borrar', BorrarInteraccionView.as_view(), name="borrar_interaccion"),
]
