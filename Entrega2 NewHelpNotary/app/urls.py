from tempfile import template
from django.urls import path,include
from . import views
from .views import ListaUsuarios, home ,Equipo , Tramites , Servicios , PreguntasFrecuentes , ReservarHora , ReservarHoraClientes ,GestionarHora, Listar, NotarioListadoReserva, NotarioEliminarReserva
from .views import infoPagare,infoImpuesto,infoGuardas,infoMandato,infoPoder,infoBien,infoPromesa,infoRevocacion,infoJuris,infoMenores,infoVehiculos,contactoViw, NotarioListaReserva,ListadoContacto

from .views import  ReservarHoraClientes , Contacto, mostrarFormRegistrar ,checkout,listadoreservas,ListaUsuarios,ModificarUsuarios,EliminarUsuarios,infodocuExtranjeros,NotarioModificarReserva,NotarioEditarReserva,ContactoEliminar
from django.contrib.auth import views as auth_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('contacto', contactoViw)



urlpatterns = [
    #MENU 
    path('', home, name ="home" ),
    path('Equipo',Equipo, name ="Equipo" ),
    path('Tramites',Tramites, name ="Tramites" ),
    path('infodocuExtranjeros',infodocuExtranjeros, name ="infodocuExtranjeros" ),
    path('infoPagare',infoPagare, name ="infoPagare" ),
    path('infoImpuesto',infoImpuesto, name ="infoImpuesto" ),
    path('infoGuardas',infoGuardas, name ="infoGuardas" ),
    path('infoMandato',infoMandato, name ="infoMandato" ),
    path('infoPoder',infoPoder, name ="infoPoder" ),
    path('infoBien',infoBien, name ="infoBien" ),
    path('infoPromesa',infoPromesa, name ="infoPromesa" ),
    path('infoRevocacion',infoRevocacion, name ="infoRevocacion" ),
    path('infoJuris',infoJuris, name ="infoJuris" ),
    path('infoMenores',infoMenores, name ="infoMenores" ),
    path('infoVehiculos',infoVehiculos, name ="infoVehiculos" ),
    path('Sevicios',Servicios, name ="Servicios" ),
    path('PreguntasFrecuentes',PreguntasFrecuentes, name ="PreguntasFrecuentes" ),
    path('Servicios',Servicios, name ="Servicios" ),
    path('PreguntasFrecuentes',PreguntasFrecuentes, name ="PreguntasFrecuentes" ),
    path('ReservarHora',ReservarHora, name ="ReservarHora" ),
    path('ReservarHoraClientes',mostrarFormRegistrar, name ="ReservarHoraClientes" ),
    path('Contacto',Contacto, name ="Contacto" ),
    path('Listar',Listar, name ="Listar" ),
   # CRUD RESERVA DE HORAS
    path('insertar', views.ReservarHoraClientes),
    path('listadoreservas',listadoreservas, name ="listadoreservas" ),
    path('form_actualizar/<int:id>', views.mostrarFormActualizar),
    path('actualizar/<int:id>', views.FormActualizarCliente),
    path('eliminar/<int:id>', views.eliminarReserva),
    path('checkout/',checkout, name ="checkout" ),
    path('GestionarHora',GestionarHora, name ="GestionarHora" ),
    #CRUD USUARIOS
	path('registro/', views.registro, name='registro'),
    path('ListaUsuarios',ListaUsuarios, name ="ListaUsuarios" ),
    path('ModificarUsuarios/<id>/', ModificarUsuarios, name ="ModificarUsuarios" ),
    path('EliminarUsuarios/<id>/', EliminarUsuarios, name ="EliminarUsuarios" ),
    #CRUD NOTARIOS
    path('NotarioListadoReserva',NotarioListadoReserva, name ="NotarioListadoReserva" ),
    path('NotarioModificarReserva/<int:id>', views.NotarioModificarReserva),
    path('NotarioEditarReserva/<int:id>', views.NotarioEditarReserva),
    path('NotarioEliminarReserva/<id>/', NotarioEliminarReserva, name="NotarioEliminarReserva"),
    path('NotarioListaReserva',NotarioListaReserva, name ="NotarioListaReserva" ),
    #CRUD CONTACTO
    path('ListadoContacto',ListadoContacto, name ="ListadoContacto" ),
    path('ContactoEliminar/<id>/', ContactoEliminar, name="ContactoEliminar"),
    #RECUPERAR CONTRASEÑA
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_complete' ),
    path('api/', include(router.urls)),
    
]
