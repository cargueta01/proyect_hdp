from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Facultad, TipoDiscapacidad
from django.contrib import messages

nombre_facultades = {
    'FCH' : 'Facultad de Ciencias y Humanidades',
    'FM' : 'Facultad de Medicina',
    'FIA' : 'Facultad de Ingenieria y Arquitectura',
    'FE' : 'Facultad de C.C. Económicas',
    'FCA' : 'Facultad de Agronomia',
    'FJCS' : 'Facultad de Jurisprudencia y C.C. Sociales',
    'FQF' : 'Facultad de Quimica y Farmacia',
    'FO' : 'Facultad de Odontologia',
    'FCNMyM' : 'Facultad de Matematicas y C.C. naturales',
    'FMOri' : 'Facultad Multidisciplinaria Oriental',
    'FMOcc' : 'Facultad Multidisciplinaria Occidental'
}

nombre_discapacidades = {
    'F' : 'Fisica',
    'A' : 'Auditiva',
    'V' : 'Visual',
    'I' : 'Intelectual',
    'P' : 'Psicosocial'
}

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
    discapacitados = TipoDiscapacidad.objects.all()
    return render(request,'menu.html', {"Facultades" : facultades, "Discapacitados" : discapacitados})

@login_required
def agregar(request):
    if request.method == 'POST':
        #para facultad
        seleccion = nombre_facultades[request.POST.get('ListFacultad')]
        femenino = request.POST.get('femenino')
        masculino = request.POST.get('masculino')
        Facultad.objects.create(facultad = seleccion, femenino = femenino, masculino = masculino)

        #para discapacidad
        seleccion2 = nombre_discapacidades[request.POST.get('ListDiscapacidad')]
        femenino2 = request.POST.get('femenino2')
        masculino2 = request.POST.get('masculino2')
        TipoDiscapacidad.objects.create(discapacidad = seleccion2, femenino = femenino2, masculino = masculino2)

        return redirect('agregar')
    else:
        facultades = Facultad.objects.all()
        discapacitados = TipoDiscapacidad.objects.all()
        return render(request, 'agregar.html', {"Facultades" : facultades, "Discapacitados" : discapacitados})
 
@login_required
def editar(request):
    contador = 0
    if request.method == 'POST':
        try:
            #para facultades
            seleccion = request.POST.get('btnradio')
            la_facultad = Facultad.objects.get(idFacultad = seleccion)
            la_facultad.facultad = nombre_facultades[request.POST.get('ListFacultad')]
            la_facultad.femenino = request.POST.get('femenino')
            la_facultad.masculino = request.POST.get('masculino')
            la_facultad.save()

            #para discapacitados
            seleccion2 = request.POST.get('btnradio2')
            discapacidades = TipoDiscapacidad.objects.get(idDiscapacidad = seleccion2)
            discapacidades.discapacidad = nombre_discapacidades[request.POST.get('ListDiscapacidad')]
            discapacidades.femenino = request.POST.get('femenino2')
            discapacidades.masculino = request.POST.get('masculino2')
            discapacidades.save()

            messages.success(request, 'Filas modificada con exito!!')

            facultades = Facultad.objects.all()
            discapacitados = TipoDiscapacidad.objects.all()
            return render(request, 'editar.html', {"Facultades" : facultades, "Discapacitados" : discapacitados})
        except Exception as e:
            messages.error(request, 'No ha seleccionado una fila')
            return redirect('editar')
    else:
        facultades = Facultad.objects.all()
        discapacitados = TipoDiscapacidad.objects.all()
        return render(request, 'editar.html', {"Facultades" : facultades, "Discapacitados" : discapacitados})
    
@login_required
def eliminar(request):
    if request.method == 'POST':
        #para facultad
        seleccion = request.POST.get('btnradio')
        facultad = Facultad.objects.get(idFacultad = seleccion)
        facultad.delete()

        #para discapacitados
        seleccion2 = request.POST.get('btnradio2')
        discapacidades = TipoDiscapacidad.objects.get(idDiscapacidad = seleccion2)
        discapacidades.delete()

        messages.success(request, 'Eliminaciones completa')
        return redirect('eliminar')
    else:
        facultades = Facultad.objects.all()
        discapacitados = TipoDiscapacidad.objects.all()
        return render(request, 'eliminar.html', {"Facultades" : facultades, "Discapacitados" : discapacitados})
    