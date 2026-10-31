from django.shortcuts import render, redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.db.models import Count 
from .models import *
from .forms import *

class VistaHome(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empresas"] = Empresa.objects.all()
        context["clientes"] = Cliente.objects.all()
        context["interacciones"] = Interaccion.objects.all()
        context["ultimas_interacciones"] = Interaccion.objects.all()[:5]
        context["empresas_con_clientes"] = Empresa.objects.annotate(
            numero_clientes=Count("clientes")
        )
        context["trabajadores_con_interacciones"] = User.objects.annotate(
            numero_interacciones=Count("interacciones")
        )
        return context
    
class RegisterView(CreateView):
    template_name = "register.html"
    model = User
    success_url = reverse_lazy('login')
    form_class = RegisterForm 

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Perfil creado")
        return super(RegisterView, self).form_valid(form)    

class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self,form):
        usuario = form.cleaned_data.get('username')
        contraseña = form.cleaned_data.get('password')
        user = authenticate(username=usuario, password=contraseña)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f"Bienvenido {usuario}")
            return redirect('home')
        
        messages.add_message(self.request, messages.ERROR, "Usuario y/o contraseña no válidos")
        return self.form_invalid(form)
    
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, f"Sesión cerrada correctamente")
    return redirect('login')

@method_decorator(login_required, name='dispatch')
class ClientesView(ListView):
    template_name = "cliente/clientes_lista.html"
    model = Cliente
    context_object_name = "clientes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empresas"] = Empresa.objects.all()
        context["trabajadores"] = User.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        busqueda = self.request.GET.get("q")
        empresa = self.request.GET.get("empresa")
        trabajador = self.request.GET.get("trabajador")

        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) | 
                Q(apellido__icontains=busqueda) | 
                Q(email__icontains=busqueda)
            )

        if empresa:
            queryset = queryset.filter(empresa__nombre__icontains=empresa)

        if trabajador:
            queryset = queryset.filter(asignado_a__first_name__icontains=trabajador)

        return queryset

@method_decorator(login_required, name='dispatch')
class DetalleClienteView(DetailView):    
    template_name = "cliente/cliente_detalle.html"
    model = Cliente
    context_object_name = "cliente"

@method_decorator(login_required, name='dispatch')
class CrearClienteView(CreateView):
    template_name = "cliente/cliente_crear.html"
    form_class = ClienteForm
    success_url = reverse_lazy('lista_clientes')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Nuevo cliente creado")
        return super(DetalleClienteView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class EditarClienteView(UpdateView):
    model = Cliente
    template_name = "cliente/cliente_editar.html"
    form_class = ClienteForm
    
    def get_success_url(self):
        return reverse('detalle_cliente', kwargs={'pk' : self.object.pk})
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Cambios guardados correctamente")
        return super(EditarClienteView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')    
class BorrarClienteView(DeleteView):
    template_name = "cliente/cliente_borrar.html"
    model = Cliente
    context_object_name = "cliente"
    success_url = reverse_lazy('lista_clientes')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Cliente eliminado")
        return super(BorrarClienteView, self).form_valid(form)
    
@method_decorator(login_required, name='dispatch')   
class EmpresasView(ListView):
    template_name = "empresa/empresas_lista.html"
    model = Empresa
    context_object_name = "empresas"

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre_empresa = self.request.GET.get("nombre_empresa")

        if nombre_empresa:
            queryset = queryset.filter(nombre__icontains=nombre_empresa)

        return queryset 

@method_decorator(login_required, name='dispatch')
class DetalleEmpresaView(DetailView):    
    template_name = "empresa/empresa_detalle.html"
    model = Empresa
    context_object_name = "empresa"

@method_decorator(login_required, name='dispatch')
class CrearEmpresaView(CreateView):
    template_name = "empresa/empresa_crear.html"
    form_class = EmpresaForm
    success_url = reverse_lazy('lista_empresas')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Nueva empresa creada")
        return super(CrearEmpresaView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class EditarEmpresaView(UpdateView):
    model = Empresa
    template_name = "empresa/empresa_editar.html"
    form_class = EmpresaForm
    
    def get_success_url(self):
        return reverse('detalle_empresa', kwargs={'pk' : self.object.pk})
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Cambios guardados correctamente")
        return super(EditarEmpresaView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')    
class BorrarEmpresaView(DeleteView):
    template_name = "empresa/empresa_borrar.html"
    model = Empresa
    context_object_name = "empresa"
    success_url = reverse_lazy('lista_empresas')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Clientea eliminada")
        return super(BorrarEmpresaView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class CrearInteraccionView(CreateView):
    template_name = "interaccion/interaccion_crear.html"
    form_class = InteraccionForm

    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(pk=self.kwargs["pk"])
        form.instance.trabajador = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detalle_cliente', kwargs={'pk' : self.object.cliente.pk})

@method_decorator(login_required, name='dispatch')    
class BorrarInteraccionView(DeleteView):
    template_name = "interaccion/interaccion_borrar.html"
    model = Interaccion
    context_object_name = "interaccion"

    def get_success_url(self):
        return reverse('detalle_cliente', kwargs={'pk' : self.object.cliente.pk})