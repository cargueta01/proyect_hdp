from django.urls import path
from . import views

urlpatterns =[
    path('', views.inicio, name='inicio'),
    path('sesion/', views.inicioSesion, name='inicioSesion'),
    path('sesion/menu/', views.menu, name='menu')
]