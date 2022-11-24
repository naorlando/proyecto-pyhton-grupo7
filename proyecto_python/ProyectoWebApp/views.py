from django.shortcuts import render, redirect
from datetime import datetime
from .models import Database
# Create your views here.


def home(request):
    return render(request,'home.html')

def tareas(request):
    db=Database()
    info=db.all_task()
    for user in info:
        print(user[1])
    return render(request,'tareas.html',{'tareas': info})

def modificar_tarea(request,id):
    db=Database()
    tarea = db.get_tarea(id)
    # prod = Item.objects.get(idproducto = id)

    fecha_inicio_t = tarea[4].strftime('%Y-%m-%d')
    hora_inicio_t = tarea[4].strftime('%H:%M')
    fecha_fin_t = tarea[5].strftime('%Y-%m-%d')

    if request.method == "POST":

        fecha_inicio_aux = request.POST.get('fecha_inicio')
        hora_inicio_aux = request.POST.get('hora_inicio')

        nombre_tarea_m = request.POST.get('nombre')
        prioridad_m = request.POST.get('prioridad')
        descripcion_m = request.POST.get('descripcion')
        fecha_inicio_m = fecha_inicio_aux + ' ' + hora_inicio_aux
        fecha_fin_m = request.POST.get('fecha_fin')
        db.update_tarea(id,nombre_tarea_m,prioridad_m,descripcion_m,fecha_inicio_m,fecha_fin_m)
        
        return redirect('/')

    return render(request,'modificartarea.html',{'tarea': tarea,'fecha_inicio_t': fecha_inicio_t,'hora_inicio_t': hora_inicio_t,'fecha_fin_t': fecha_fin_t})

def crear_tarea(request):
    return render(request,'creartarea.html')