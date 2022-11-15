from email.policy import default
from django.db import models
from django.contrib.auth.models import User

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

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name        



class ReservaDeHora(models.Model):
    fecha_solicitud = models.DateTimeField(verbose_name='Fecha Solicitud')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    telefono = models.CharField(max_length=50)
    tiporeserva = models.TextField(max_length = 50)
    total = models.IntegerField(default=5000)

    def __str__(self):
         return self.nombre                                        



class Order(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.cliente.user)
