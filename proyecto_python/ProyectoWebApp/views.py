from django.shortcuts import render, redirect
from .models import Database
# Create your views here.


def home(request):
    return render(request,'home.html')

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

    return render(request,'modificartarea.html',{'tarea': task})

def crear_tarea(request):
    return render(request,'creartarea.html')