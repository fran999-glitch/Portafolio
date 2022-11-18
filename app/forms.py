
from django import forms
from .models import *
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.forms import PasswordInput
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from utilidades import formularios
from app.models import*
from django.core.exceptions import ValidationError
from allauth.account.forms import LoginForm




class ReservaDeHoraForm(forms.ModelForm):
	nombre = forms.CharField(required=True,  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese su Nombre', 'autocomplete': 'off'}))
	apellido = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese su Apellido', 'autocomplete': 'off'}))
	correo = forms.CharField(required=True, 
		widget=forms.TextInput(
			attrs={'class': 'form-control', 'placeholder': 'EMail@gmail.com'}
			),
			validators=[
				validators.MinLengthValidator(4, message="El E-Mail es demasiado corto"),
				validators.RegexValidator('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', message="El E-Mail ingresado no es válido")
			],
			error_messages={'required':'El campo E-Mail está vacío' }
		)
	telefono = forms.CharField(required=True, widget=forms.TextInput(
			attrs={'class': 'form-control', 'placeholder': 'Teléfono', 'autocomplete':'off'}
			),
			validators=[
                validators.MinLengthValidator(9, message="El Teléfono es demasiado corto"),
                validators.RegexValidator('^[+0-9 ]*$', message="El Teléfono contiene caracteres inválidos, por favor use sólo números, por ejemplo +5691652132")
            ]
	)	

	total = forms.CharField(required=False, widget=forms.TextInput(attrs={ 'disabled':'disabled', 'placeholder': '5000', 'onkeypress': 'return soloNumeros(event)', 'autocomplete':'off'}))

	class Meta:

			model = ReservaDeHora
			fields =["fecha", "hora", "nombre", "apellido","correo","telefono","CategoriaTramite","total"]
			#fields = '__all__'
			widgets = {
			"fecha": AdminDateWidget( attrs={'placeholder':'Ingrese fecha de reserva'}) ,
            "hora": AdminTimeWidget( attrs={'placeholder':'Ingrese hora de reserva'}) ,

        }

			



class ContactoForm(forms.ModelForm):

    class Meta:
        model = contacto
        #fields =["nombre", "correo", "tipo_consulta", "mensaje"]
        fields = '__all__'




class MyCustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):

        # Add your own processing here.

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)

#REGISTRO USUARIOS
class RegistroUsuariosForm(UserCreationForm):

	email = forms.CharField(required=True, 
		widget=forms.TextInput(
			attrs={'class': 'form-control', 'placeholder': 'EMail@gmail.com'}
			),
			validators=[
				validators.MinLengthValidator(4, message="El E-Mail es demasiado corto"),
				validators.RegexValidator('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', message="El E-Mail ingresado no es válido")
				
			],
			error_messages={'required':'El campo E-Mail está vacío' }
	)

	class Meta:
		
		model = User
		fields = [	'username','first_name','last_name','email','groups','password1','password2' ]
		#fields = '__all__'
		

		
		def clean_email(self, *args, **kwargs):
			email = self.cleaned_data.get('email')
			if User.objects.filter(email=email).exists():
				raise forms.ValidationError("El email ya está registrado, prueba con otro.")
			return self.cleaned_data
				
		help_texts = {k:"" for k in fields  }





#REGISTRO CLIENTES

class CreateUserForm(UserCreationForm):
	username = forms.CharField(label='Nombre de usuario',   min_length=5, max_length=150)  
	email = forms.CharField(required=True, 
		widget=forms.TextInput(
			attrs={'class': 'form-control', 'placeholder': 'EMail@gmail.com'}
			),
			validators=[
				validators.MinLengthValidator(4, message="El E-Mail es demasiado corto"),
				validators.RegexValidator('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', message="El E-Mail ingresado no es válido")
				
			],
			error_messages={'required':'El campo E-Mail está vacío' }
	)	
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
			'email':'email',
			'password1': 'Contraseña1',
			'password2': 'Contraseña2',
		}
			
		help_texts = {k:"" for k in fields  }

		def email_clean(self):  
			email = self.cleaned_data['email'].lower()  
			new = User.objects.filter(email=email)  
			if new.count():  
				raise ValidationError(" Email Already Exist")  
			return email  


