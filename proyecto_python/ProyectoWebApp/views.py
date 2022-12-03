from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from datetime import datetime
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from .models import Database, Tarea
from .forms import TareaJsonForm
from .funciones import *
from os import remove
import json

def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('Tareas')
            # manejo el error integrity (sacando el try catch podemos ver el error)
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords does not match'
        })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error':'Username or password is incorrect'
        })
        else:
            login(request,user)
            return redirect('Tareas')

def signout(request):
    logout(request)
    return redirect('Home')

def listar_tareas(request):
    db = Database()
    info = db.all_task()

    # for user in info:
    #     print(user[1])

    nro_pagina = request.GET.get('page', 1)

    try:
        paginado = Paginator(info, 6)
        info = paginado.page(nro_pagina)
    except:
        raise Http404

    return render(request, 'tareas.html', {'tareas': info, 'paginado': paginado})

def modificar_tarea(request, id):
    db = Database()
    tarea = db.get_tarea(id)

    fecha_inicio_t = tarea[3].strftime('%Y-%m-%d')
    hora_inicio_t = tarea[3].strftime('%H:%M')
    fecha_fin_t = tarea[4].strftime('%Y-%m-%d')

    data = {
        'tarea': tarea,
        'prioridad_t': convertir_prioridad(tarea[6]),
        'fecha_inicio_t': fecha_inicio_t,
        'hora_inicio_t': hora_inicio_t,
        'fecha_fin_t': fecha_fin_t
    }

    if request.method == "POST":

        fecha_inicio_aux = request.POST.get('fecha_inicio')
        hora_inicio_aux = request.POST.get('hora_inicio')

        nombre_tarea_m = request.POST.get('nombre')
        prioridad_m = request.POST.get('prioridad')
        descripcion_m = request.POST.get('descripcion')
        fecha_inicio_m = fecha_inicio_aux + ' ' + hora_inicio_aux
        fecha_fin_m = request.POST.get('fecha_fin')
        db.update_tarea(id, nombre_tarea_m, prioridad_m,
                        descripcion_m, fecha_inicio_m, fecha_fin_m)

        return redirect('/tareas')

    return render(request, 'modificartarea.html', data)

def crear_tarea(request):
    db = Database()
    form = TareaJsonForm()

    if request.method == "POST":

        # if request.POST.get('archivoJson'):
        form = TareaJsonForm(request.POST, request.FILES)

        # En caso de utilizar el formulario input file
        if form.is_valid():

            # Crea el archivo data.json con la info recibida y lo cierra
            tareaJson = open('ProyectoWebApp/static/data.json', "wb+")
            for i in request.FILES['file'].chunks():
                tareaJson.write(i)
            tareaJson.close()

            # Abre el archivo cerado, lo lee y almacena como str en una variable, y lo cierra
            tareaJson = open('ProyectoWebApp/static/data.json', "r")
            tareas = tareaJson.read()
            tareaJson.close()

            # Transformama el json leido a un diccionario, lo recorre y almacena cada valor
            try:
                data = json.loads(tareas)
                username_m = request.user.username
                for i in data:
                    nombre_tarea_m = i['nombre_tarea']
                    descripcion_m = i['descripcion']
                    fecha_inicio_m = i['fecha_inicio']
                    fecha_fin_m = i['fecha_fin']
                    prioridad_m = i['prioridad']
                    db.create_tarea(nombre_tarea_m, prioridad_m,
                                    descripcion_m, fecha_inicio_m, fecha_fin_m, username_m)

                # Elimina el archivo
                remove('ProyectoWebApp/static/data.json')

                return redirect('/tareas')

            except:
                print('Error al crear tarea mediante archivo JSON')
                return redirect('/')

        # En caso de utilizar el formulario manual
        else:

            username_m = request.user.username
            fecha_inicio_aux = request.POST.get('fecha_inicio')
            hora_inicio_aux = request.POST.get('hora_inicio')
            nombre_tarea_m = request.POST.get('nombre')
            prioridad_m = request.POST.get('prioridad')
            descripcion_m = request.POST.get('descripcion')
            fecha_inicio_m = fecha_inicio_aux + ' ' + hora_inicio_aux
            fecha_fin_m = request.POST.get('fecha_fin')
            db.create_tarea(nombre_tarea_m, prioridad_m,
                            descripcion_m, fecha_inicio_m, fecha_fin_m,username_m)

            return redirect('/tareas')

    return render(request, 'creartarea.html', {'form': form})

def eliminar_tarea(request, id):
    db = Database()
    db.delete_tarea(id)

    return redirect('/tareas')

def tarea_id(request, id):
    db = Database()
    tarea = db.get_tarea(id)
    # prod = Item.objects.get(idproducto = id)

    fecha_inicio_t = tarea[3].strftime('%Y-%m-%d')
    hora_inicio_t = tarea[3].strftime('%H:%M')
    fecha_fin_t = tarea[4].strftime('%Y-%m-%d')

    data = {
        'tarea': tarea,
        'prioridad_t': convertir_prioridad(tarea[6]),
        'fecha_inicio_t': fecha_inicio_t,
        'hora_inicio_t': hora_inicio_t,
        'fecha_fin_t': fecha_fin_t
    }

    return render(request, 'tareaid.html', data)

def exportar_tarea(request, id):
    db = Database()
    tarea = db.get_tarea(id)

    fecha_inicio_t = tarea[3].strftime('%Y-%m-%d')
    hora_inicio_t = tarea[3].strftime('%H:%M')
    fecha_fin_t = tarea[4].strftime('%Y-%m-%d')

    prioridad = convertir_prioridad(tarea[6])
    estado = convertir_estado(tarea[5])
    # usuario = db.get_user(tarea[7])

    objeto_tarea = Tarea(tarea[1],tarea[2],fecha_inicio_t + ' ' + hora_inicio_t,fecha_fin_t,estado,prioridad,tarea[7])
    objeto_tarea = objeto_tarea.__dict__

    tarea_json = json.dumps(objeto_tarea)
    nombre_archivo = str(tarea[1]) + '.json'
    
    jsonFile = open('ProyectoWebApp/static/data.json','w+')
    jsonFile.write(tarea_json)
    jsonFile.close()

    jsonFile = open('ProyectoWebApp/static/data.json','rb')
    data = jsonFile.read()
    jsonFile.close()

    response = HttpResponse(data,content_type='text/plain')
    response['Content-Disposition'] = 'attachement; filename=%s' % nombre_archivo

    remove('ProyectoWebApp/static/data.json')

    return response

