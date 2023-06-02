from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def inicio(request):
    return HttpResponse("<h1>bienvenido al inicio</h1>")

def inicioSesion(request):
    return render(request, 'inicioSesion.html')

def menu(request):
    return redirect(request, 'menu.html')