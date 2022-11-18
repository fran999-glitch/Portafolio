from django.contrib import admin
from .models import contacto,Cliente
from .models import *
from  utilidades import formularios
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

class UsersMetadataAdmin(admin.ModelAdmin):

    list_display = ('id', 'correo', 'telefono', 'direccion', formularios.set_user)
    list_per_page = 20

    
class TramiteCategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('id', 'nombre', 'slug')

class ReservaDeHoraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre','apellido','fecha','hora','correo','telefono','CategoriaTramite','total')
    search_fields = ('id', 'nombre', 'slug')
    

        
class CliAdmin(admin.ModelAdmin):
    list_display = ('id','user' ,'name','apellido','email')
    search_fields = ('id', 'nombre', 'slug')

class AboAdmin(admin.ModelAdmin):
    list_display = ('id','user' ,'name','apellido','email')
    search_fields = ('id', 'nombre', 'slug')

class SecreAdmin(admin.ModelAdmin):
    list_display = ('id','user' ,'name','apellido','email')
    search_fields = ('id', 'nombre', 'slug')    

class NotaAdmin(admin.ModelAdmin):
    list_display = ('id','user' ,'name','apellido','email')
    search_fields = ('id', 'nombre', 'slug')


class ClienteInline(admin.StackedInline):
    model = Cliente
    list_display = ('id','user' ,'name','apellido','email')

    verbose_name_plural = 'Cliente'


class Administradoruser(admin.ModelAdmin):
    list_display = ('id','user' ,'name','apellido','email')
    search_fields = ('id', 'nombre', 'slug')    

class AdminInline(admin.StackedInline):
    model = Administrador
    list_display = ('id','user' ,'name','apellido','email')

    verbose_name_plural = 'Cliente'    

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ClienteInline,AdminInline)
    list_display = ('id','username' ,'first_name','last_name','email')
    list_per_page = 10

# Re-register Clase usuario
admin.site.unregister(User)
admin.site.register(User, UserAdmin)        
#Contacto
admin.site.register(contacto)
#Usuarios
admin.site.register(Cliente,CliAdmin)
admin.site.register(Administrador,Administradoruser)
admin.site.register(Secretaria, SecreAdmin)
admin.site.register(Abogado,AboAdmin)
admin.site.register(Notario,NotaAdmin)
#Reservas de Hora
admin.site.register(Categoria , TramiteCategoriaAdmin)
admin.site.register(ReservaDeHora,ReservaDeHoraAdmin)
#Title Backend pagina
admin.site.site_header = 'Administración NewHelpNotary'
admin.site.index_title = 'Administración NewHelpNotary'
admin.site.site_title = 'Administración NewHelpNotary'




