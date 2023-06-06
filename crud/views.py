from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Facultad, TipoDiscapacidad
from django.contrib import messages
from django.db.models import Q

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
    'FMOcc' : 'Facultad Multidisciplinaria Occidental',
    'ED' : 'Educacion a distancia'
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
        my_anio = request.POST.get('ListAnio')
        Facultad.objects.create(facultad = seleccion, femenino = femenino, masculino = masculino, anio = my_anio)

        #para discapacidad
        seleccion2 = nombre_discapacidades[request.POST.get('ListDiscapacidad')]
        femenino2 = request.POST.get('femenino2')
        masculino2 = request.POST.get('masculino2')
        #TipoDiscapacidad.objects.create(discapacidad = seleccion2, femenino = femenino2, masculino = masculino2, anio = my_anio)
        messages.success(request, 'Filas modificada con exito!!')
        return redirect('agregar')
    else:
        facultades = Facultad.objects.all()
        discapacitados = TipoDiscapacidad.objects.all()
        return render(request, 'agregar.html', {"Facultades" : facultades, "Discapacitados" : discapacitados})
 
@login_required
def editar(request):
    if request.method == 'POST':
        try:
            #para facultades
            seleccion = request.POST.get('btnradio')
            la_facultad = Facultad.objects.get(idFacultad = seleccion)
            la_facultad.facultad = nombre_facultades[request.POST.get('ListFacultad')]
            la_facultad.femenino = request.POST.get('femenino')
            la_facultad.masculino = request.POST.get('masculino')
            la_facultad.anio = request.POST.get('ListAnio')
            la_facultad.save()

            #para discapacitados
            seleccion2 = request.POST.get('btnradio2')
            discapacidades = TipoDiscapacidad.objects.get(idDiscapacidad = seleccion2)
            discapacidades.discapacidad = nombre_discapacidades[request.POST.get('ListDiscapacidad')]
            discapacidades.femenino = request.POST.get('femenino2')
            discapacidades.masculino = request.POST.get('masculino2')
            discapacidades.anio = request.POST.get('ListAnio')
            discapacidades.save()

            messages.success(request, 'Filas modificada con exito!!')

            facultades = Facultad.objects.all()
            discapacitados = TipoDiscapacidad.objects.all()
            return redirect('editar')
        except Exception as e:
            messages.error(request, 'No ha seleccionado dos fila')
            return redirect('editar')
    else:
        facultades = Facultad.objects.all()
        discapacitados = TipoDiscapacidad.objects.all()
        return render(request, 'editar.html', {"Facultades" : facultades, "Discapacitados" : discapacitados})
    
@login_required
def eliminar(request):
    if request.method == 'POST':
        try:
            #para facultad
            seleccion = request.POST.get('btnradio')
            facultad = Facultad.objects.get(idFacultad = seleccion)

            #para discapacitados
            seleccion2 = request.POST.get('btnradio2')
            discapacidades = TipoDiscapacidad.objects.get(idDiscapacidad = seleccion2)

            discapacidades.delete()
            facultad.delete()

            messages.success(request, 'Eliminaciones completa')
            return redirect('eliminar')
        except Exception as e:
            messages.error(request, 'No seleccionado dos filas fila')
            return redirect('eliminar')
    else:
        facultades = Facultad.objects.all()
        discapacitados = TipoDiscapacidad.objects.all()
        return render(request, 'eliminar.html', {"Facultades" : facultades, "Discapacitados" : discapacitados})


def consulta(request):
    facultades = Facultad.objects.all()
    discapacitados = TipoDiscapacidad.objects.all()
    if request.method == 'POST':
        general = request.POST.get('cbx')
        if general == 'cbxTodo':
           return render(request, 'consulta.html', {"Facultades" : facultades, "Discapacitados" : discapacitados})
        else :
            f_resultado = None
            d_resultado = None
            f_facultad = request.POST.get('ListFacultad')
            d_discapacidad = request.POST.get('ListDiscapacidad')
            v_anio = request.POST.get('Listfecha')
            if f_facultad == 'Todas':
                f_resultado = Facultad.objects.filter(anio = int(v_anio))
            else:
                f_resultado = Facultad.objects.filter(facultad = nombre_facultades[f_facultad] ,anio = int(v_anio))
            if d_discapacidad == 'Todas':
                d_resultado = TipoDiscapacidad.objects.filter(anio = int(v_anio))
            else:
                d_resultado = TipoDiscapacidad.objects.filter(discapacidad = nombre_discapacidades[d_discapacidad] ,anio = int(v_anio))
            print(f"esto es el resultado1: {f_resultado}")
            print(f"esto es el resultado2: {d_resultado}")
            return render(request, 'consulta.html', {"Facultades" : f_resultado, "Discapacitados" : d_resultado})
    else:
        return render(request, 'consulta.html', {"Facultades" : facultades, "Discapacitados" : discapacitados})