from cProfile import label
from tkinter import Widget
from tkinter.ttk import Style
from django import forms
from .models import contacto,Cliente
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. 254 carácteres como máximo y debe ser válido.")

    class Meta:
        model = User
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Requerido. 254 carácteres como máximo y debe ser válido.")

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email

class ContactoForm(forms.ModelForm):

    class Meta:
        model = contacto
        #fields =["nombre", "correo", "tipo_consulta", "mensaje"]
        fields = '__all__'

class CreateUserForm(UserCreationForm):
	
	email = forms.EmailField()
	password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)
	class Meta:
		
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',

				 ]
		label = {
			'username': 'Nombre de usuario',
			'first_name':'Nombre',
			'last_name':'Apellido',
			'email':'Correo',
			'password1': 'Contraseña1',
			'password2': 'Contraseña2',

		}
			
		widget = {
				'username': forms.TextInput(attrs={'class':'form-control-color', 'placeholder': 'Usuario' }),
				'first_name': forms.TextInput(attrs={'class':'form-control-color', 'placeholder': 'Usuario' }),
				'password1': forms.TextInput(attrs={'class':'form-control-color', 'placeholder': 'Usuario' }),
			}
		help_texts = {k:"" for k in fields  }