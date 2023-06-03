from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

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
    return render(request,'menu.html')

@login_required
def agregar(request):
    return render(request, 'agregar.html')

@login_required
def editar(request):
    return render(request, 'editar.html')

@login_required
def eliminar(request):
    return render(request, 'eliminar.html')