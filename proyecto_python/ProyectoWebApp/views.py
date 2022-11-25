from django.shortcuts import render, redirect
from datetime import datetime
from django.core.paginator import Paginator
from django.http import Http404
from .models import Database
# Create your views here.


def home(request):
    return render(request, 'home.html')

<<<<<<< HEAD

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
=======
def tareas(request):
    db=Database()
    info=db.all_task()
    for task in info:
        print(task[1])
    return render(request,'tareas.html',{'tareas': info})

def modificar_tarea(request, ide):
    db=Database()
    task = db.get_tarea(ide)
    # prod = Item.objects.get(idproducto = id)

    if request.method == "POST":
        nombre_tarea_m = request.POST.get('nombre')
        fecha_inicio_m = request.POST.get('fecha_inicio')
        fecha_finalizacion_m = request.POST.get('fecha_finalizacion')
        categoria_m = request.POST.get('categoria')
        db.update_tarea(ide, nombre_tarea_m,fecha_inicio_m,fecha_finalizacion_m,categoria_m)
        return redirect('/')
>>>>>>> fabrizio


def crear_tarea(request):
    db = Database()

    if request.method == "POST":

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

    return render(request, 'creartarea.html')


def eliminar_tarea(request, id):
    db = Database()
    db.delete_tarea(id)

    return redirect('/tareas')
