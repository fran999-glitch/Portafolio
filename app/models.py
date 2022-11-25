from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.db.models.signals import pre_save,post_delete,post_save
from django.dispatch import receiver
from datetime import datetime, date, timedelta
from django import forms





# Create your models here.


opciones_consulta = [
    [0, "consulta"],
    [1, "reclamo "],
    [2, "sugerencia"],
    [3, "otro"],
    
]
class contacto(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consulta)
    mensaje = models.TextField(null=True)

    def __str__(self):
        
        return self.nombre
        

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        
        return f'Perfil de {self.user.username}'


class Notario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True , unique=True) 
    name = models.CharField(max_length=200, null=True)
    apellido = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True ) 
				 

    def __str__(self):
        return self.name  


class Abogado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True , unique=True) 
    name = models.CharField(max_length=200, null=True)
    apellido = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True ) 
				 

    def __str__(self):
        return self.name          

class Secretaria(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True , unique=True) 
    name = models.CharField(max_length=200, null=True)
    apellido = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True ) 
				 

    def __str__(self):
        return self.name  


class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True , unique=True) 
    name = models.CharField(max_length=200, null=True)
    apellido = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True ) 
				 

    def __str__(self):
        return self.name        


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True ) 
    name = models.CharField(max_length=200, null=True)
    apellido = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True ) 
				 

    def __str__(self):
        return self.name  
        

class Perfiles(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'perfiles'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'            


class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'estado'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'



class Genero(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'genero'
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'        

class UsersMetadata(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    estado = models.ForeignKey(Estado, models.DO_NOTHING)
    genero = models.ForeignKey(Genero, models.DO_NOTHING)
    perfiles = models.ForeignKey(Perfiles, models.DO_NOTHING)
    slug = models.CharField(max_length=100, null=True)
    correo = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = 'users_metadata'
        verbose_name = 'User metadata'
        verbose_name_plural = 'User metadata'


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100,null=True)
    slug = AutoSlugField(populate_from='nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Categoria_Reserva'
        verbose_name = 'Categoría Reserva'
        verbose_name_plural = 'Categorias Reservas'

class ReservaDeHora(models.Model):
    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='nombre')
    apellido = models.CharField(max_length=50)
    fecha = models.DateField(verbose_name='Fecha ')
    hora = models.TimeField(verbose_name='Hora ')
    correo = models.EmailField()
    telefono = models.CharField(max_length=9)
    order_key = models.CharField('numero orden', max_length=200, blank=True)
    payment_option = models.CharField('Opción de pago', max_length=50, blank=True)
    CategoriaTramite = models.ForeignKey(Categoria, models.DO_NOTHING)
    total = models.IntegerField(default=5000)

    def __str__(self):
     
         return self.nombre                                        

