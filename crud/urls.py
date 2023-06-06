from django.urls import path
from . import views

urlpatterns =[
    path('', views.inicio, name='inicio'),
    path('login/', views.inicioSesion, name='inicioSesion'),
    path('logout/', views.cerrarSesion, name='cerrarSesion'),
    path('login/menu/', views.menu, name='menu'),
    path('login/menu/agregar', views.agregar, name='agregar'),
    path('login/menu/editar', views.editar, name='editar'),
    path('login/menu/eliminar', views.eliminar, name='eliminar'),
    path('consulta/', views.consulta, name='consulta')
]