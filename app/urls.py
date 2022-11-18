from tempfile import template
from django.urls import path
from . import views
from .views import home ,Equipo , Tramites , Servicios , PreguntasFrecuentes , ReservarHora , ReservarHoraClientes , Contacto ,listadoreservas,Adminvista,modificarReservas
from .views import EliminaReserva,modificarModalReservas,ReservarHoraClientesAdmin,ListaUsuarios , ModificarUsuarios ,registroAdmin,registroCli,EliminarUsuarios

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name ="home" ),
    path('Equipo',Equipo, name ="Equipo" ),
    path('Tramites',Tramites, name ="Tramites" ),
    path('Servicios',Servicios, name ="Servicios" ),
    path('PreguntasFrecuentes',PreguntasFrecuentes, name ="PreguntasFrecuentes" ),
    path('ReservarHora',ReservarHora, name ="ReservarHora" ),
    path('ReservarHoraClientes',ReservarHoraClientes, name ="ReservarHoraClientes" ),
    path('Contacto',Contacto, name ="Contacto" ),

    #ADMINISTRACION USUARIOS
    path('Adminvista',Adminvista, name ="Adminvista" ),


    #CRUD RESERVAS DE HORA 
    path('listadoreservas',listadoreservas, name ="listadoreservas" ),
    path('ReservarHoraClientesAdmin',ReservarHoraClientesAdmin, name ="ReservarHoraClientesAdmin" ),
    path('modificarReservas/<id>/',modificarReservas, name ="modificarReservas" ),
    path('modificarModalReservas/<id>/',modificarModalReservas, name ="modificarModalReservas" ),
    path('EliminaReserva/<id>/',EliminaReserva, name ="EliminaReserva" ),

    
    #registros Usuarios
    path('registroCli/', registroCli, name='registroCli'),
    path('registroAdmin/', registroAdmin, name='registroAdmin'),
    path('registroNotario/', views.registroNotario, name='registroNotario'),
    path('registroAbogado/', views.registroAbogado, name='registroAbogado'),
    path('registroSecretaria/', views.registroSecretaria, name='registroSecretaria'),


    #CRUD USUARIOS
	path('registro/', views.registro, name='registro'),
    path('ListaUsuarios',ListaUsuarios, name ="ListaUsuarios" ),
    path('ModificarUsuarios/<id>/', ModificarUsuarios, name ="ModificarUsuarios" ),
    path('EliminarUsuarios/<id>/', EliminarUsuarios, name ="EliminarUsuarios" ),


    #Login y registro de usuario
	path('registro/', views.registro, name='registro'),
	#path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    #Reset Password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_complete' ),
    
    
]
