from django.shortcuts import render, redirect
from .models import Database
# Create your views here.


def home(request):
    return render(request,'home.html')

def productos(request):
    db=Database()
    info=db.all_users()
    for user in info:
        print(user[1])
    return render(request,'productos.html',{'productos': info})

def modificar_producto(request,id):
    db=Database()
    prod = db.get_producto(id)
    # prod = Item.objects.get(idproducto = id)

    if request.method == "POST":
        nombre_producto_m = request.POST.get('nombre')
        precio_m = request.POST.get('precio')
        categoria_m = request.POST.get('categoria')
        db.update_producto(id,nombre_producto_m,precio_m,categoria_m)
        return redirect('/')

    return render(request,'modificarproducto.html',{'producto': prod})

def crear_producto(request):
    return render(request,'crearproducto.html')