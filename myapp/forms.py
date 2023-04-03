from django import forms
from .models import *
from django.contrib.auth.models import User



class Form1(forms.Form):
    Opciones=(
    ("No vengo", "No vengo"),
    ("Principal", 'Principal'),
    ("Principal C/ Guarnición", 'Principal C/ Guarnición'),
    ("Opción", 'Opción'),
    ("Opción C/ Guarnición", 'Opción C/ Guarnición'),
    ("Minuta", 'Minuta'),
    ("Ensalada", 'Ensalada'),
    ("Celíaco", 'Celíaco'),
    ("Vegetariano", 'Vegetariano'),
    ("Bandeja de Fruta", 'Bandeja de Fruta')

    )

    Lunes = forms.ChoiceField(choices=Opciones)
    Martes = forms.ChoiceField(choices=Opciones)
    Miercoles = forms.ChoiceField(choices=Opciones)
    Jueves = forms. ChoiceField(choices=Opciones)
    Viernes = forms.ChoiceField(choices=Opciones)

class SubirMenuForm(forms.ModelForm):
    class Meta:
        model = SubirMenu
        fields = ('name', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'image-upload'}),
        }

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    is_admin = forms.BooleanField(label='Set as admin', required=False)


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken')
        return username

class LoginForm(forms.Form):
    username = forms.CharField(label="", max_length=100, initial="")
    password = forms.CharField(label="", widget=forms.PasswordInput, initial="")