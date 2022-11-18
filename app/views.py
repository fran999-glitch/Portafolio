from email import message
from email.headerregistry import Group
from multiprocessing import context
from tokenize import group
from unicodedata import name
from urllib import request
from django.shortcuts import render
from .forms import ContactoForm,CreateUserForm,UserCreationForm,ReservaDeHoraForm,RegistroUsuariosForm
from .models import *
from django import  forms
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .import views
from django.contrib.auth.models import User
from .filters import OrderFilter
from utilidades import utilidades,formularios
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator






# Create your views here.

def home (request):
    return render (request, 'app/home.html')

def Equipo (request):
    return render (request, 'app/equipo.html')

def Tramites (request):
    return render (request, 'app/Tramites.html')

def Servicios (request):
    return render (request, 'app/Servicios.html')

def PreguntasFrecuentes (request):
    return render (request, 'app/PreguntasFrecuentes.html')

def ReservarHora (request):
    return render (request, 'app/ReservaClientes/ReservarHora.html')

@login_required(login_url='login')
def ReservarHoraClientes (request):
    data = {
        'form': ReservaDeHoraForm()
    }
    if request.method == 'POST':
        formulario = ReservaDeHoraForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Reserva de hora realizada correctamente")
            return redirect(to="ReservarHoraClientes")
        else:
            data["form"] = formulario

    return render (request, 'app/ReservaClientes/ReservarHoraClientes.html',data)



def logout_usuario(request):
    logout(request)
    
    return HttpResponseRedirect('/accounts/login/')    

def Adminvista (request):
    
    return render (request, 'app/admin/index.html')

def ReservarHoraClientesAdmin (request):
    data = {
        'form': ReservaDeHoraForm()
    }
    if request.method == 'POST':
        formulario = ReservaDeHoraForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Reserva de hora realizada correctamente")
            return redirect(to="listadoreservas")
        else:
            data["form"] = formulario

    return render (request, 'app/ReservaClientes/ReservarHoraClientes.html',data)

def listadoreservas(request):
    reservashoras = ReservaDeHora.objects.all()
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(reservashoras, 5)
        reservashoras = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': reservashoras,
        'paginator': paginator

    }
   
  
    return render(request, 'app/admin/ListadoClientesReservas.html',data)            



def modificarReservas(request, id ):
  
    reservahora=get_object_or_404(ReservaDeHora, id=id)
    data = {
        'form':ReservaDeHoraForm(instance=reservahora)
    }
    if request.method=='POST':
        formulario = ReservaDeHoraForm(data=request.POST, instance=reservahora)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Reserva de hora modificado Correctamente")
 
            return redirect ( to = "listadoreservas")
        data["form"]=formulario    

      
  
    return render(request, 'app/admin/actualizarReserva.html', data )           


def modificarModalReservas(request, id ):
  
    reservahora=get_object_or_404(ReservaDeHora, id=id)
    data = {
        'form':ReservaDeHoraForm(instance=reservahora)
    }
    if request.method=='POST':
        formulario = ReservaDeHoraForm(data=request.POST, instance=reservahora)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Reserva de hora modificado Correctamente")
 
            return redirect ( to = "listadoreservas")
        data["form"]=formulario    

      
  
    return render(request, 'app/admin/actualizarReserva.html', data )           



    

def EliminaReserva (request,id):

    reserva = get_object_or_404(ReservaDeHora,id=id)
    reserva.delete()
    messages.success(request, f"Reserva {reserva.CategoriaTramite}  Eliminado Correctamente")

    return redirect(to="listadoreservas")

       

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
            cliente, created = Cliente.objects.get_or_create(user=user ,name=request.POST['username'],apellido=request.POST['last_name'],email=request.POST['email'] )
      #      if request.user.groups.f

            group=Group.objects.get(name= 'cliente')
            user.groups.add(group)
            
            messages.success(request, f'Usuario {username} creado')
            return redirect('home')
    else:
        form = CreateUserForm()

    context = {'form':form}        
    return render (request, 'registration/registro.html', context)


#CRUD  USUARIOS 
def registroCli (request):
    form = RegistroUsuariosForm()
    if request.method == 'POST':
        form = RegistroUsuariosForm  (request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            Cliente.objects.get_or_create(user=user ,name=request.POST['username'],apellido=request.POST['last_name'],email=request.POST['email'] )
            group=Group.objects.get(name= 'CLIENTE')

            user.groups.add(group)

                 
            messages.success(request, f'Usuario {username} creado')
            return redirect('ListaUsuarios')
    else:
        form = RegistroUsuariosForm()

    context = {'form':form}        
    return render (request, 'app/admin/registro/register.html', context)


def registroNotario (request):
    form = RegistroUsuariosForm()
    if request.method == 'POST':
        form = RegistroUsuariosForm  (request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            Notario.objects.get_or_create(user=user ,name=request.POST['username'],apellido=request.POST['last_name'],email=request.POST['email'] )
            group=Group.objects.get(name= 'NOTARIO')

            user.groups.add(group)
     
            messages.success(request, f'Usuario {username} creado')
        return redirect('ListaUsuarios')
    else:
        form = RegistroUsuariosForm()

    context = {'form':form}        
    return render (request, 'app/admin/registro/registerNotario.html', context)

    
def registroAdmin (request):
    form = RegistroUsuariosForm()
    if request.method == 'POST':
        form = RegistroUsuariosForm  (request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            Notario.objects.get_or_create(user=user ,name=request.POST['username'],apellido=request.POST['last_name'],email=request.POST['email'] )
            group=Group.objects.get(name= 'ADMINISTRADOR')

            user.groups.add(group)
     
            messages.success(request, f'Usuario {username} creado')
        return redirect('ListaUsuarios')
    else:
        form = RegistroUsuariosForm()

    context = {'form':form}        
    return render (request, 'app/admin/registro/registerAdmin.html', context)


def registroAbogado (request):
    form = RegistroUsuariosForm()
    if request.method == 'POST':
        form = RegistroUsuariosForm  (request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            Notario.objects.get_or_create(user=user ,name=request.POST['username'],apellido=request.POST['last_name'],email=request.POST['email'] )
            group=Group.objects.get(name= 'ABOGADO')

            user.groups.add(group)
     
            messages.success(request, f'Usuario {username} creado')
        return redirect('ListaUsuarios')
    else:
        form = RegistroUsuariosForm()

    context = {'form':form}        
    return render (request, 'app/admin/registro/registerAbogado.html', context)

    
def registroSecretaria (request):
    form = RegistroUsuariosForm()
    if request.method == 'POST':
        form = RegistroUsuariosForm  (request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            Notario.objects.get_or_create(user=user ,name=request.POST['username'],apellido=request.POST['last_name'],email=request.POST['email'] )
            group=Group.objects.get(name= 'SECRETARIA')

            user.groups.add(group)
     
            messages.success(request, f'Usuario {username} creado')
        return redirect('ListaUsuarios')
    else:
        form = RegistroUsuariosForm()

    context = {'form':form}        
    return render (request, 'app/admin/registro/registerSecretaria.html', context)


def ListaUsuarios (request):
    usuarios = User.objects.all()
    myFilter= OrderFilter(request.POST, queryset=usuarios)
    usuarios=myFilter.qs
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(usuarios, 6)
        usuarios = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity':usuarios,
        'myFilter':myFilter,
        'paginator': paginator

    }
    return render (request, 'app/admin/ListaUsuario.html',data)    

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
  
    return render (request, 'app/admin/ModificarUsuario.html',data)


def EliminarUsuarios (request,id):

    usuario = get_object_or_404(User,id=id)
    usuario.delete()
    messages.success(request, f"Usuario {usuario.username}  Eliminado Correctamente")
    return redirect(to="ListaUsuarios")    