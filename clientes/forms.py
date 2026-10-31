from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Empresa, Interaccion

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = "__all__"

class InteraccionForm(forms.ModelForm):
    class Meta:
        model = Interaccion
        fields = ["fecha", "notas"]
        widgets = {
            "fecha": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
        }