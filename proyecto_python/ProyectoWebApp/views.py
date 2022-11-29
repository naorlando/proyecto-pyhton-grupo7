from django.shortcuts import render, redirect
from datetime import datetime
from django.core.paginator import Paginator
from django.http import Http404
from .models import Database
from .forms import TareaJsonForm
from os import remove
import json
# Create your views here.


def home(request):
    return render(request, 'home.html')


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
    # prod = Item.objects.get(idproducto = id)

    fecha_inicio_t = tarea[4].strftime('%Y-%m-%d')
    hora_inicio_t = tarea[4].strftime('%H:%M')
    fecha_fin_t = tarea[5].strftime('%Y-%m-%d')

    data = {
        'tarea': tarea,
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
                for i in data:
                    nombre_tarea_m = i['nombre_tarea']
                    prioridad_m = i['prioridad']
                    descripcion_m = i['descripcion']
                    fecha_inicio_m = i['fecha_inicio']
                    fecha_fin_m = i['fecha_fin']
                    db.create_tarea(nombre_tarea_m, prioridad_m,
                                    descripcion_m, fecha_inicio_m, fecha_fin_m)

                # Elimina el archivo
                remove('ProyectoWebApp/static/data.json')

                return redirect('/tareas')

            except:
                return redirect('/')

        # En caso de utilizar el formulario manual
        else:

            fecha_inicio_aux = request.POST.get('fecha_inicio')
            hora_inicio_aux = request.POST.get('hora_inicio')

            nombre_tarea_m = request.POST.get('nombre')
            prioridad_m = request.POST.get('prioridad')
            descripcion_m = request.POST.get('descripcion')
            fecha_inicio_m = fecha_inicio_aux + ' ' + hora_inicio_aux
            fecha_fin_m = request.POST.get('fecha_fin')
            db.create_tarea(nombre_tarea_m, prioridad_m,
                            descripcion_m, fecha_inicio_m, fecha_fin_m)

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

    fecha_inicio_t = tarea[4].strftime('%Y-%m-%d')
    hora_inicio_t = tarea[4].strftime('%H:%M')
    fecha_fin_t = tarea[5].strftime('%Y-%m-%d')

    data = {
        'tarea': tarea,
        'fecha_inicio_t': fecha_inicio_t,
        'hora_inicio_t': hora_inicio_t,
        'fecha_fin_t': fecha_fin_t
    }

    return render(request, 'tareaid.html', data)
