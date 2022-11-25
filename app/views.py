import json
from email.headerregistry import Group
from multiprocessing import context
from tokenize import group
from unicodedata import name
from urllib import request
from django.shortcuts import render
from .forms import ContactoForm, CreateUserForm, UserCreationForm, ReservaDeHoraForm, RegistroUsuariosForm
from .models import *
from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .import views
from django.contrib.auth.models import User
from .filters import OrderFilter
from utilidades import utilidades, formularios
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic import TemplateView, CreateView


# paypal
from .paypal import PayPalClient
from paypalcheckoutsdk.orders import OrdersGetRequest

# Create your views here.

def home(request):
    return render(request, 'app/home.html')


def Equipo(request):
    return render(request, 'app/equipo.html')


def Tramites(request):
    return render(request, 'app/Tramites.html')


def Servicios(request):
    return render(request, 'app/Servicios.html')


def PreguntasFrecuentes(request):
    return render(request, 'app/PreguntasFrecuentes.html')


def ReservarHora(request):
    return render(request, 'app/ReservaClientes/ReservarHora.html')


@login_required(login_url='login')
def ReservarHoraClientes(request):
    """ Vista para reserva hora del cliente y pedir el pago via paypal"""
    data = {
        'form': ReservaDeHoraForm()
    }
    if request.method == 'POST':
        formulario = ReservaDeHoraForm(data=request.POST)
        if formulario.is_valid():
            instance = formulario.save()
            return redirect(payment_complete, instance.id)
            # messages.success(
            #     request, "Reserva de hora realizada correctamente")
            # return redirect(to="ReservarHoraClientes")
        else:
            data["form"] = formulario

    return render(request, 'app/ReservaClientes/ReservarHoraClientes.html', data)

# def payment_checkout

def payment_complete(request, pk):
    """ 
    * Creamos una conexion con paypal
    * recopilamos la información de respuesta al procesar el pago
    * obtenemos la información de los pedidos procesados a traves de su id
    """

    # reserva = ReservaDeHora.objects.get(id=pk)
    reserva = get_object_or_404(ReservaDeHora, id=pk)
    # ayuda a conectarse a paypal
    PPClient = PayPalClient()

    # respuesta de paypal
    if request.body:
        body = json.loads(request.body)
        data = body['orderID']
        print(data)
        user_id = request.user.id
        if data: 
            requestorder = OrdersGetRequest(data)
            response = PPClient.client.execute(requestorder)
            print(response)
            print('codigo',  response.result.id)

            reserva = ReservaDeHora.objects.get(id=pk)
            reserva.order_key = response.result.id
            reserva.payment_option = "paypal"
            reserva.save()
            return JsonResponse({'order_key': response.result.id})
            # return redirect('payment_successful', response.result.id)
            # return redirect(reverse('payment_successful', args=[response.result.id]))

    # obtenemos datos de orden

    # total_paid = response.result.purchase_units[0].amount.value

    # basket = Basket(request)

    # if request.method == 'POST':
    #     formulario = ReservaDeHoraForm(data=request.POST)
    #     if formulario.is_valid():
    #         instance = formulario.save()
    #         reserva = ReservaDeHora.objects.get(id=instance.id)
    #         reserva.order_key = response.result.id
    #         reserva.payment_option = "paypal"
    #         reserva.save()



    return render(request, 'app/ReservaClientes/payment_complete.html', {'reserva': reserva})

def payment_successful(request, order_key):

    try:
        reserva = ReservaDeHora.objects.get(order_key=order_key)
    except ReservaDeHora.DoesNotExist:
        print('no existe')
        raise Http404
    return render(request, 'app/ReservaClientes/payment_successful.html', {'reserva': reserva})

def logout_usuario(request):
    logout(request)

    return HttpResponseRedirect('/accounts/login/')


def Adminvista(request):

    return render(request, 'app/admin/index.html')

# crear reserva en admin
def ReservarHoraClientesAdmin(request):
    data = {
        'form': ReservaDeHoraForm()
    }
    if request.method == 'POST':
        formulario = ReservaDeHoraForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(
                request, "Reserva de hora realizada correctamente")
            return redirect(to="listadoreservas")
        else:
            data["form"] = formulario

    return render(request, 'app/ReservaClientes/ReservarHoraClientes.html', data)

# ADMIN
def dashboard(request):
    # print(ReservaDeHora.objects.filter(fecha__month=11).count())
    print(request.user.date_joined.month)
    reservas_mensuales_count = [ReservaDeHora.objects.filter(fecha__month=i).count() for i in range(1,13)]
    clientes_mensuales_count = [Cliente.objects.filter(user__date_joined__month=i).count() for i in range(1,13)]
    context = {
        'reservas_mensuales_count' :  reservas_mensuales_count,
        'clientes_mensuales_count' :  clientes_mensuales_count
    }
    return render(request, 'app/admin/dashboard.html', context)


# class ReservarHoraClientesAdminCreateView(CreateView):
#     model = ReservaDeHora
#     template_name = 'app/admin/ReservaHoraClientes.html'


def listadoreservas(request):
    reservashoras = ReservaDeHora.objects.all()
    page = request.GET.get('page', 1)
    if request.method == 'POST':
        form = ReservaDeHoraForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ReservaDeHoraForm()
    try:
        paginator = Paginator(reservashoras, 5)
        reservashoras = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': reservashoras,
        'paginator': paginator,
        'form': form
    }

    return render(request, 'app/admin/ListadoClientesReservas.html', data)


def modificarReservas(request, id):

    reservahora = get_object_or_404(ReservaDeHora, id=id)
    data = {
        'form': ReservaDeHoraForm(instance=reservahora)
    }
    if request.method == 'POST':
        formulario = ReservaDeHoraForm(data=request.POST, instance=reservahora)
        if formulario.is_valid():
            formulario.save()
            messages.success(
                request, "Reserva de hora modificado Correctamente")

            return redirect(to="listadoreservas")
        data["form"] = formulario

    return render(request, 'app/admin/actualizarReserva.html', data)


def modificarModalReservas(request, id):

    reservahora = get_object_or_404(ReservaDeHora, id=id)
    formulario = ReservaDeHoraForm(request.POST or None, instance=reservahora)
    # if request.method == 'POST':
    #     if ReservaDeHora.objects.filter(nombre=request.POST['nombre']).exclude(id=reservahora.id).exists():
    #         formulario.errors['nombre'] = ['El nombre esta duplicado']
    #     if ReservaDeHora.objects.filter(nombre=request.POST['nombre']).exclude(id=reservahora.id).exists():
    #         formulario.errors['nombre'] = ['El nombre esta duplicado']
    #     if ReservaDeHora.objects.filter(nombre=request.POST['nombre']).exclude(id=reservahora.id).exists():
    #         formulario.errors['nombre'] = ['El nombre esta duplicado']
    #     else:
    if formulario.is_valid():
        formulario.save()
        messages.success(
            request, "Reserva de hora modificado Correctamente")

        return redirect(to="listadoreservas")
    # else:
    #     formulario.errors['apellido'] = ['Solo feo']
    # print(formulario.errors.as_data())
    data = {
        'form': formulario
    }
    return render(request, 'app/admin/actualizarReserva.html', data)


def EliminaReserva(request, id):

    reserva = get_object_or_404(ReservaDeHora, id=id)
    reserva.delete()
    messages.success(
        request, f"Reserva {reserva.CategoriaTramite}  Eliminado Correctamente")

    return redirect(to="listadoreservas")


def Contacto(request):
    data = {
        'form': ContactoForm()
    }
    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()

            messages.success(request, "Mensaje Enviado Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'app/Contacto.html', data)


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, f'Usuario {username} Inicio Sesion')

            login(request, user)

            return redirect('home')
            # Redirect to a success page.
        else:
            messages.success(
                request, "a ocurrido un error en el Login ,Intente nuevamente...")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def registro(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            cliente, created = Cliente.objects.get_or_create(
                user=user, name=request.POST['username'], apellido=request.POST['last_name'], email=request.POST['email'])
      #      if request.user.groups.f

            group = Group.objects.get(name='cliente')
            user.groups.add(group)

            messages.success(request, f'Usuario {username} creado')
            return redirect('home')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'registration/registro.html', context)


# CRUD  USUARIOS
def registroCli(request):
    form = RegistroUsuariosForm()
    if request.method == 'POST':
        form = RegistroUsuariosForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            Cliente.objects.get_or_create(
                user=user, name=request.POST['username'], apellido=request.POST['last_name'], email=request.POST['email'])
            group = Group.objects.get(name='CLIENTE')

            user.groups.add(group)

            messages.success(request, f'Usuario {username} creado')
            return redirect('ListaUsuarios')
    else:
        form = RegistroUsuariosForm()

    context = {'form': form}
    return render(request, 'app/admin/registro/register.html', context)


def registroNotario(request):
    form = RegistroUsuariosForm()
    if request.method == 'POST':
        form = RegistroUsuariosForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            Notario.objects.get_or_create(
                user=user, name=request.POST['username'], apellido=request.POST['last_name'], email=request.POST['email'])
            group = Group.objects.get(name='NOTARIO')

            user.groups.add(group)

            messages.success(request, f'Usuario {username} creado')
        return redirect('ListaUsuarios')
    else:
        form = RegistroUsuariosForm()

    context = {'form': form}
    return render(request, 'app/admin/registro/registerNotario.html', context)


def registroAdmin(request):
    form = RegistroUsuariosForm()
    if request.method == 'POST':
        form = RegistroUsuariosForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            Notario.objects.get_or_create(
                user=user, name=request.POST['username'], apellido=request.POST['last_name'], email=request.POST['email'])
            group = Group.objects.get(name='ADMINISTRADOR')

            user.groups.add(group)

            messages.success(request, f'Usuario {username} creado')
        return redirect('ListaUsuarios')
    else:
        form = RegistroUsuariosForm()

    context = {'form': form}
    return render(request, 'app/admin/registro/registerAdmin.html', context)


def registroAbogado(request):
    form = RegistroUsuariosForm()
    if request.method == 'POST':
        form = RegistroUsuariosForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            Notario.objects.get_or_create(
                user=user, name=request.POST['username'], apellido=request.POST['last_name'], email=request.POST['email'])
            group = Group.objects.get(name='ABOGADO')

            user.groups.add(group)

            messages.success(request, f'Usuario {username} creado')
        return redirect('ListaUsuarios')
    else:
        form = RegistroUsuariosForm()

    context = {'form': form}
    return render(request, 'app/admin/registro/registerAbogado.html', context)


def registroSecretaria(request):
    form = RegistroUsuariosForm()
    if request.method == 'POST':
        form = RegistroUsuariosForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            Notario.objects.get_or_create(
                user=user, name=request.POST['username'], apellido=request.POST['last_name'], email=request.POST['email'])
            group = Group.objects.get(name='SECRETARIA')

            user.groups.add(group)

            messages.success(request, f'Usuario {username} creado')
        return redirect('ListaUsuarios')
    else:
        form = RegistroUsuariosForm()

    context = {'form': form}
    return render(request, 'app/admin/registro/registerSecretaria.html', context)


def ListaUsuarios(request):
    usuarios = User.objects.all()
    myFilter = OrderFilter(request.POST, queryset=usuarios)
    usuarios = myFilter.qs
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(usuarios, 6)
        usuarios = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': usuarios,
        'myFilter': myFilter,
        'paginator': paginator

    }
    return render(request, 'app/admin/ListaUsuario.html', data)


def ModificarUsuarios(request, id):

    usuario = get_object_or_404(User, id=id)
    data = {
        'form': CreateUserForm(instance=usuario)
    }
    if request.method == 'POST':
        formulario = CreateUserForm(data=request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            username = formulario.cleaned_data['username']
            messages.success(
                request, f"Usuario {username} modificado correctamente")
            return redirect(to="ListaUsuarios")
        data['form'] = formulario

    return render(request, 'app/admin/ModificarUsuario.html', data)


def EliminarUsuarios(request, id):

    usuario = get_object_or_404(User, id=id)
    usuario.delete()
    messages.success(
        request, f"Usuario {usuario.username}  Eliminado Correctamente")
    return redirect(to="ListaUsuarios")
