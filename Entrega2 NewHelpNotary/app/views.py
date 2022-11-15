from cgitb import text
from email import message
from email.headerregistry import Group
from multiprocessing import context
from tokenize import group
from unicodedata import name
from urllib import request
from django.shortcuts import render
from .forms import ContactoForm,CreateUserForm,UserCreationForm
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import Http404
from .filters import OrderFilter
from django.db.models import Q
from django.contrib.auth.models import Group
from .import views
from django.contrib.auth.models import User
from .serializers import contacto_serial



# Create your views here.

from rest_framework import viewsets




class contactoViw(viewsets.ModelViewSet):
    queryset = contacto.objects.all()
    serializer_class = contacto_serial



def home (request):
    return render (request, 'app/home.html')

def Equipo (request):
    return render (request, 'app/equipo.html')

def Tramites (request):
    return render (request, 'app/Tramites.html')


def infodocuExtranjeros (request):
    return render (request, 'app/infodocuExtranjeros.html')

def infoPagare (request):
    return render (request, 'app/infoTramites/infoPagare.html')    


def infoImpuesto (request):
    return render (request, 'app/infoTramites/infoImpuesto.html')


def infoGuardas (request):
    return render (request, 'app/infoTramites/infoGuardas.html')


def infoMandato (request):
    return render (request, 'app/infoTramites/infoMandato.html')

    
def infoPoder (request):
    return render (request, 'app/infoTramites/infoPoder.html')   
    
def infoBien (request):
    return render (request, 'app/infoTramites/infoBien.html') 

def infoPromesa (request):
    return render (request, 'app/infoTramites/infoPromesa.html') 


def infoRevocacion (request):
    return render (request, 'app/infoTramites/infoRevocacion.html') 

def infoJuris (request):
    return render (request, 'app/infoTramites/infoJuris.html') 

    
def infoMenores (request):
    return render (request, 'app/infoTramites/infoMenores.html')


def infoVehiculos (request):
    return render (request, 'app/infoTramites/infoVehiculos.html') 
      

def Servicios (request):
    return render (request, 'app/Servicios.html')

def PreguntasFrecuentes (request):
    return render (request, 'app/PreguntasFrecuentes.html')

@login_required(login_url='login')

def ReservarHora (request):
    return render (request, 'app/ReservaClientes/ReservarHora.html')


def mostrarFormRegistrar(request):


    return render (request, 'app/ReservaClientes/ReservarHoraClientes.html')


def ReservarHoraClientes (request):
    
    if request.method =='POST' :
        fecha = request.POST['txtfereserva']
        nom = request.POST['txtnombre']
        ape = request.POST['txtapellido']
        correo = request.POST['txtemail']
        cel = request.POST['txtelefono']
        tipocon = request.POST['tipoconsulta']

        reservacli =ReservaDeHora(fecha_solicitud=fecha,nombre=nom,apellido=ape,correo=correo,telefono=cel,tiporeserva=tipocon)
        reservacli.save()
        datos = { 'r' : 'Reserva de Hora Registrado Correctamente!!' }
        return render (request, 'app/ReservaClientes/ReservarHoraClientes.html',datos)
    else:
        datos = { 'r2' : 'Debe Presionar El Botón Para Registrar!!' }

        return render (request, 'app/ReservaClientes/ReservarHoraClientes.html',datos)

def NotarioListaReserva(request):
    reservashoras = ReservaDeHora.objects.all()
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(reservashoras, 8)
        reservashoras = paginator.page(page)
    except:
        raise Http404
   
  
    return render(request, 'app/CrudNotario/NotarioListaReserva.html', {"Areservas":reservashoras})

def NotarioListadoReserva(request):
    busqueda = request.POST.get("buscar")
    NotarioListado = ReservaDeHora.objects.all()

    if busqueda:
        NotarioListado = ReservaDeHora.objects.filter(
            Q(nombre__icontains = busqueda) | 
            Q(apellido__icontains = busqueda) |
            Q(correo__icontains = busqueda) |
            Q(telefono__icontains = busqueda)
        ).distinct()
        
    return render(request, 'app/CrudNotario/NotarioListadoReserva.html', {"NotarioListado":NotarioListado})

def NotarioModificarReserva (request, id):
  try :
     
      Areservas = ReservaDeHora.objects.get(id=id)
      
      fa = Areservas.fecha_solicitud

      if fa.day>=1 and fa.day<=9:
            dia = "0" + str(fa.day)
      else:
            dia = str(fa.day)

      if fa.month>=1 and fa.month<=9:
            mes = "0" + str(fa.month)
      else:
            mes = str(fa.month)

      if fa.hour>=1 and fa.hour<=9:
            hora = "0" + str(fa.hour)
      else:
            hora = str(fa.hour)    

      if fa.minute>=1 and fa.minute<=9:
            minutos = "0" + str(fa.minute)
      else:
            minutos = str(fa.minute)    
    
      fecha = str(fa.year ) + "-" + mes + "-" + dia +"-"+hora+":"+minutos

      datos = {
            'Areservas' : Areservas,
            'fecha' : fecha
      }

      return render(request, 'app/CrudNotario/NotarioModificarReserva.html',datos)     

  except:     
    Areservas = ReservaDeHora.objects.all()
    datos = {
            'Areservas' : Areservas,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Mostrar Para Actualizar!!'
            }
  return render(request, 'app/CrudNotario/NotarioListaReserva.html',datos)        
  
def NotarioEditarReserva (request, id):
 if request.method == 'POST':
    try:
        fecha = request.POST['txtfereserva']
        nom = request.POST['txtnombre']
        ape = request.POST['txtapellido']
        correo = request.POST['txtemail']
        cel = request.POST['txtelefono']
        tipocon = request.POST['tipoconsulta']

        Areservas = ReservaDeHora.objects.get(id=id)
        Areservas.fecha_solicitud=fecha
        Areservas.nombre=nom
        Areservas.apellido=ape
        Areservas.correo=correo
        Areservas.telefono=cel
        Areservas.tiporeserva=tipocon
        Areservas.save()

        Areservas = ReservaDeHora.objects.all()
        datos = {
            'Areservas' : Areservas,
            'r' : 'Datos Modificados Correctamente!!' 
            }
        return render(request, 'app/CrudNotario/NotarioListaReserva.html',datos)     
    except:
        Areservas = ReservaDeHora.objects.all()
        datos = {
            'Areservas' : Areservas,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!'
            }
        
        return render(request, 'app/CrudNotario/NotarioListaReserva.html',datos)

def NotarioEliminarReserva (request, id):
    reservacli = get_object_or_404(ReservaDeHora, id=id)
    reservacli.delete()
    return redirect(to='NotarioListadoReserva')

def listadoreservas(request):
    reservashoras = ReservaDeHora.objects.all()
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(reservashoras, 8)
        reservashoras = paginator.page(page)
    except:
        raise Http404
   
  
    return render(request, 'app/ReservaClientes/ListadoClientesReservas.html', {"reservas":reservashoras})        

def eliminarReserva(request, id ):
    try :
     
      reservashoras = ReservaDeHora.objects.get(id=id)
      reservashoras.delete()
      reservas = ReservaDeHora.objects.all()
      datos = {
            'reservas' : reservas,
            'r' : 'Reserva Eliminado Correctamente!!' 
      }
      return render(request, 'app/ReservaClientes/ListadoClientesReservas.html',datos)        
    except:     

     reservashoras = ReservaDeHora.objects.all()
    datos = {

             'reservas' : reservas,
             'r2' : 'El ID ('+str(id)+') No Existe. Imposible Eliminar' 
        }
 
    return render(request, 'app/ReservaClientes/ListadoClientesReservas.html',datos)        


def  Listar(request):


    return render (request, 'app/ReservaClientes/listar.html')


def mostrarFormActualizar (request, id):
  try :
     
      reservas = ReservaDeHora.objects.get(id=id)
      
      fa = reservas.fecha_solicitud

      if fa.day>=1 and fa.day<=9:
            dia = "0" + str(fa.day)
      else:
            dia = str(fa.day)

      if fa.month>=1 and fa.month<=9:
            mes = "0" + str(fa.month)
      else:
            mes = str(fa.month)

      if fa.hour>=1 and fa.hour<=9:
            hora = "0" + str(fa.hour)
      else:
            hora = str(fa.hour)    

      if fa.minute>=1 and fa.minute<=9:
            minutos = "0" + str(fa.minute)
      else:
            minutos = str(fa.minute)    
    
      fecha = str(fa.year ) + "-" + mes + "-" + dia +"-"+hora+":"+minutos

      datos = {
            'reservas' : reservas,
            'fecha' : fecha
      }

      return render(request, 'app/ReservaClientes/form_actualizar.html',datos)     

  except:     
    reservas = ReservaDeHora.objects.all()
    datos = {
            'reservas' : reservas,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Mostrar Para Actualizar!!'
            }
  return render(request, 'app/ReservaClientes/ListadoClientesReservas.html',datos)        
  


     
def FormActualizarCliente (request, id):
 if request.method == 'POST':
    try:
        fecha = request.POST['txtfereserva']
        nom = request.POST['txtnombre']
        ape = request.POST['txtapellido']
        correo = request.POST['txtemail']
        cel = request.POST['txtelefono']
        tipocon = request.POST['tipoconsulta']

        reservas = ReservaDeHora.objects.get(id=id)
        reservas.fecha_solicitud=fecha
        reservas.nombre=nom
        reservas.apellido=ape
        reservas.correo=correo
        reservas.telefono=cel
        reservas.tiporeserva=tipocon
        reservas.save()

        reservas = ReservaDeHora.objects.all()
        datos = {
            'reservas' : reservas,
            'r' : 'Datos Modificados Correctamente!!' 
            }
        return render(request, 'app/ReservaClientes/ListadoClientesReservas.html',datos)     
    except:
        reservas = ReservaDeHora.objects.all()
        datos = {
            'reservas' : reservas,
            'r2' : 'El ID ('+str(id)+') No Existe. Imposible Actualizar!!'
            }
        
        return render(request, 'app/ReservaClientes/ListadoClientesReservas.html',datos)     
        

def GestionarHora (request):
    busqueda = request.POST.get( "txtnombre")
    busqueda = request.POST.get( "txtmail")
    reservas = ReservaDeHora.objects.all()
    if busqueda :
        reservas = ReservaDeHora.objects.filter(
            Q(nombre__icontains    = busqueda) |
            Q(apellido= busqueda) |
            Q(correo= busqueda) |
            Q(telefono= busqueda) |
            Q(tiporeserva= busqueda) 
            
        ).distinct()

        return render (request, 'app/ReservaClientes/GestionarMisHoras.html',{'reservas':reservas})

    else   :            
            
     return render (request, 'app/ReservaClientes/GestionarMisHoras.html')        
    

def Contacto (request):
    data= {  
        'form':ContactoForm()
    }
    if request.method=='POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()

            messages.success(request, "Mensaje Enviado Correctamente")
        else:
            data["form"]=formulario    
 
    return render (request, 'app/Contacto.html',data)
    
def ListadoContacto(request):  
    Lcontactos = contacto.objects.all()
    data = {
        'Lcontactos':Lcontactos
    }
    return render(request, 'app/CrudContacto/ListadoContacto.html',data)

def ContactoEliminar (request, id):
    Lcontactos = get_object_or_404(contacto, id=id)
    Lcontactos.delete()
    return redirect(to='ListadoContacto')

def login (request):
    if request.method == "POST" :
        username = request.POST ['username']
        password = request.POST ['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
                messages.success(request, f'Usuario {username} Inicio Sesion')

                login(request, user)

                return redirect('home')
                # Redirect to a success page.
        else:
         messages.success(request, "a ocurrido un error en el Login ,Intente nuevamente...")
         return redirect('login')
    else:
     return render (request, 'accounts/login.html')


def registro (request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm  (request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            cliente, created = Cliente.objects.get_or_create(user=user ,name=user.get_username, email=user.get_email_field_name)

            group=Group.objects.get(name= 'cliente')
            user.groups.add(group)
            
            messages.success(request, f'Usuario {username} creado')
            return redirect('home')
    else:
        form = CreateUserForm()

    context = {'form':form}        
    return render (request, 'registration/registro.html', context)

def ListaUsuarios (request):
  
    usuarios = User.objects.all()
    myFilter= OrderFilter(request.POST, queryset=usuarios)
    usuarios=myFilter.qs

    data = {
        'usuarios':usuarios,
        'myFilter':myFilter
    }
    return render (request, 'registration/ListaUsuario.html',data)


def ModificarUsuarios (request,id):

    usuario = get_object_or_404(User,id=id)
    data = {
        'form':CreateUserForm(instance=usuario)
    }
    if request.method == 'POST':
     formulario = CreateUserForm  (data=request.POST, instance=usuario)
     if formulario.is_valid():
         formulario.save()
         username=formulario.cleaned_data['username']
         messages.success(request, f"Usuario {username} modificado correctamente")
         return redirect(to="ListaUsuarios")
     data['form'] = formulario 
  
    return render (request, 'registration/ModificarUsuario.html',data)


def EliminarUsuarios (request,id):

    usuario = get_object_or_404(User,id=id)
    usuario.delete()
    messages.success(request, f"Usuario {usuario.username}  Eliminado Correctamente")
    return redirect(to="ListaUsuarios")

  


def checkout (request):
    
    return render (request, 'app/ReservaClientes/checkout.html')

   


