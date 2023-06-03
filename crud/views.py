from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Facultad, TipoDiscapacidad
from django.contrib import messages

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def inicioSesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')  # Redirecciona a la página después del inicio de sesión exitoso
        else:
            # Lógica para manejar el inicio de sesión fallido
            return render(request, 'registration/login.html', {'error_message': 'Credenciales inválidas'})
    else:
        return render(request, 'registration/login.html')


def cerrarSesion(request):
    logout(request)
    return redirect('inicio')


@login_required
def menu(request):
    facultades = Facultad.objects.all()
    return render(request,'menu.html', {"Facultad" : facultades})

#def eleccion(seleccion, femenino, masculino):
    #if seleccion == 1:
     #   datos = Facultad.objects.create(facultad = seleccion, femenino = femenino, masculino = masculino)

@login_required
def agregar(request):
    if request.method == 'POST':
        seleccion = request.POST['seleccion']
        femenino = request.POST['femenino']
        masculino = request.POST['masculino']

        datos = Facultad.objects.create(facultad = seleccion, femenino = femenino, masculino = masculino)
        return redirect('agregar')
    else:
        facultades = Facultad.objects.all()
        return render(request, 'agregar.html', {"Facultad" : facultades})
 
@login_required
def editar(request):
    facultades = Facultad.objects.all()
    return render(request, 'editar.html', {"Facultad" : facultades})

@login_required
def eliminar(request):
    if request.method == 'POST':
        seleccion = request.POST.get('btnradio')
        facultad = Facultad.objects.get(idFacultad = seleccion)
        facultad.delete()
        messages.success(request, 'Eliminacion completa')
        return redirect('eliminar')
    else:
        facultades = Facultad.objects.all()
        return render(request, 'eliminar.html', {"Facultad" : facultades})
    