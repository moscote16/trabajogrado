from django.urls import path
from . import views





urlpatterns = [
    path('',views.hello,name='index'),
    path('login/', views.loginview, name='login'),
    path('registro/', views.registroview, name='registro'),
    path('principal/', views.principal, name='principal'),
    path('listado_paciente/', views.listado_paciente, name='listado_paciente'),
    path('listado_datos/', views.listado_datos, name='listado_datos'),
    path('prueba/', views.prueba, name='prueba'),
    path('actualizar/', views.actualizar, name='actualizar'),
    path('logout/',views.signout, name='logout'),
    path('registro1/', views.registro1, name='registro1'),
    path('formulario/', views.formulario, name='formulario'),
    path('bancodatos/', views.bancodatos, name='bancodatos'),
    path('resultadodatos/', views.resultadodatos, name='resultadodatos'),
    path('resultadospacientes/', views.resultadospacientes, name='resultadospacientes'),
]
