import re
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


	nombre = forms.CharField(required=True,  widget=forms.TextInput(attrs={'placeholder': 'Ingrese su Nombre', 'autocomplete': 'off'}))
	apellido = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su Apellido', 'autocomplete': 'off'}))
	correo = forms.CharField(required=True, 
		widget=forms.TextInput(
			attrs={'placeholder': 'Email@gmail.com'}
			),
			# validators=[
			# 	validators.MinLengthValidator(4, message="El E-Mail es demasiado corto"),
			# 	validators.RegexValidator('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', message="El E-Mail ingresado no es válido")
			# ],
			# error_messages={'required':'El campo E-Mail está vacío' }
		)
	telefono = forms.CharField(required=True, max_length=9,widget=forms.TextInput(
			attrs={'placeholder': 'Teléfono ej. 916521321', 'autocomplete':'off'}
			)
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

			
	def clean_base(self, value, attr):
		reserva_list = ReservaDeHora.objects.all()
		if self.instance.pk is not None:
			reserva_list = reserva_list.exclude(id=self.instance.pk)
		reserva_list = reserva_list.values_list(attr, flat=True)
		if value.lower() in reserva_list:
			msg = f'Este {attr} "{value}" ya se encuentra registrado'
			raise forms.ValidationError(msg)
		return value


	def clean_nombre(self):
		nombre = self.cleaned_data.get('nombre')
		reserva = ReservaDeHora.objects.filter(nombre=nombre)
		if self.instance.pk is not None:
			reserva = reserva.exclude(id=self.instance.pk)
		if reserva.exists():
			msg = f'Este nombre ya se encuentra registrado'
			raise forms.ValidationError(msg)
		patron = "^[a-zA-Z ]+$"
		if re.search(patron, nombre) == None:
			msg = 'Solo debe contener letras'
			raise forms.ValidationError(msg)
		return nombre

	def clean_apellido(self):
		apellido = self.cleaned_data.get('apellido')
		patron = "^[a-zA-Z ]+$"
		if re.search(patron, apellido) == None:
			msg = 'Solo debe contener letras'
			raise forms.ValidationError(msg)
		return self.clean_base(apellido, 'apellido')

	def clean_correo(self):
		correo = self.cleaned_data.get('correo')
		return self.clean_base(correo, 'correo')

	def clean_telefono(self):
		telefono = self.cleaned_data.get('telefono')
		# patron = "^\+569[0-9]{8}$"
		patron = "^[9][0-9]{8}$"
		# patron = "^\+?[56]{2}?\s?[9]?\s?[0-9]{8}|[9]?\s?[0-9]{8}$"
		# patron = "/^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$/"
		if re.search(patron, telefono) == None:
			msg = 'Ingrese formato correcto ej: 916521321'
			raise forms.ValidationError(msg)
		return self.clean_base(telefono, 'telefono')


	def clean_hora(self):
		hora = self.cleaned_data.get('hora').strftime('%H:%M')
		fecha = self.cleaned_data.get('fecha')
		reserva_list = ReservaDeHora.objects.all()
		if self.instance.pk is not None:
			reserva_list = reserva_list.exclude(pk=self.instance.pk)
		reserva_list = reserva_list.values_list('fecha', 'hora')
		for reserva in reserva_list:
			if reserva[0] == fecha and reserva[1].strftime('%H:%M') == hora:
				raise forms.ValidationError('Esta hora ya esta reservada')
		return hora


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


