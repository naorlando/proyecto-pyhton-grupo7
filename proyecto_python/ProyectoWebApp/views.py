from django.shortcuts import render, redirect
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

    if request.method == "POST":
        nombre_tarea_m = request.POST.get('nombre')
        prioridad_m = request.POST.get('prioridad')
        descripcion_m = request.POST.get('descripcion')
        fecha_inicio_m = request.POST.get('fecha_inicio')
        fecha_fin_m = request.POST.get('fecha_fin')
        db.update_tarea(id,nombre_tarea_m,prioridad_m,descripcion_m,fecha_inicio_m,fecha_fin_m)
        return redirect('/')

    return render(request,'modificartarea.html',{'tarea': tarea})

def crear_tarea(request):
    return render(request,'creartarea.html')