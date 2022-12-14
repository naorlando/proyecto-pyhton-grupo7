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
import cv2 as cv
import numpy as np
import pytesseract
import PIL.Image


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
                    'error': 'El Username ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
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
                'error': 'El Username o la Contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('Tareas')


def signout(request):
    logout(request)
    return redirect('Home')


def listar_tareas(request):
    db = Database()

    if request.method == "POST":
        info = db.get_tarea_buscada(request.POST.get('tarea_buscada'))
    else:
        info = db.all_task()

    nro_pagina = request.GET.get('page', 1)

    try:
        paginado = Paginator(info, 6)
        info = paginado.page(nro_pagina)
    except:
        raise Http404

    return render(request, 'tareas.html', {'tareas': info, 'paginado': paginado})


def listar_tareas_archivadas(request):
    db = Database()
    info = db.tareas_archivadas()

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

        try:
            username_m = request.user.username
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
        
        except:

            mensaje = 'Hubo un error al intentar modificar la tarea: ' + tarea[1]
            return render(request,'error.html',{'mensaje': mensaje})


    return render(request, 'modificartarea.html', data)


def modificar_estado(request, id, estado):

    try:

        db = Database()
        db.update_estado_tarea(id, estado)

    except:

        mensaje = 'Hubo un error al modificar el estado de la tarea'
        return render(request,'error.html',{'mensaje': mensaje})

    return redirect('/tareas/' + str(id))


def archivar_tarea(request, id):

    try:

        db = Database()
        db.archivar_tarea(id)

    except:

        mensaje = 'Hubo un error al intentar archivar la tarea'
        return render(request,'error.html',{'mensaje': mensaje})

    return redirect('/tareas/' + str(id))


def desarchivar_tarea(request, id):

    try:

        db = Database()
        db.desarchivar_tarea(id)

    except:

        mensaje = 'Hubo un error al intentar desarchivar la tarea'
        return render(request,'error.html',{'mensaje': mensaje})

    return redirect('/tareas/' + str(id))


def crear_tarea(request):
    db = Database()
    form = TareaJsonForm()

    if request.method == "POST":

        form = TareaJsonForm(request.POST, request.FILES)

        # En caso de utilizar el formulario input file
        if form.is_valid():

            try:
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

                        if i['fecha_inicio'] == 'Actual' or i['fecha_inicio'] == 'ACTUAL' or i['fecha_inicio'] == 'actual':
                            fecha_actual = datetime.now()
                            fecha_inicio_m = fecha_actual.strftime("%Y/%m/%d %H:%M")
                        else:
                            fecha_inicio_m = i['fecha_inicio']

                        fecha_fin_m = i['fecha_fin']
                        prioridad_m = i['prioridad']
                        db.create_tarea(nombre_tarea_m, prioridad_m,
                                        descripcion_m, fecha_inicio_m, fecha_fin_m, username_m)

                    # Elimina el archivo
                    remove('ProyectoWebApp/static/data.json')

                    return redirect('/tareas')

                except:
                    mensaje = 'Error al crear tarea mediante archivo JSON'
                    return render(request,'error.html',{'mensaje': mensaje})
            except:
                mensaje = 'Error al intentar abrir el archivo'
                return render(request,'error.html',{'mensaje': mensaje})

        # En caso de utilizar el formulario manual
        else:

            try:
                username_m = request.user.username
                fecha_inicio_aux = request.POST.get('fecha_inicio')
                hora_inicio_aux = request.POST.get('hora_inicio')
                nombre_tarea_m = request.POST.get('nombre')
                prioridad_m = request.POST.get('prioridad')
                descripcion_m = request.POST.get('descripcion')
                fecha_inicio_m = fecha_inicio_aux + ' ' + hora_inicio_aux
                fecha_fin_m = request.POST.get('fecha_fin')
                db.create_tarea(nombre_tarea_m, prioridad_m,
                                descripcion_m, fecha_inicio_m, fecha_fin_m, username_m)

                return redirect('/tareas')
            except:

                mensaje = 'Error al crear la tarea'
                return render(request,'error.html',{'mensaje': mensaje})

    return render(request, 'creartarea.html', {'form': form})


def mis_tareas(request):
    db = Database()

    info = db.get_tareas_usuario(request.user.username)

    nro_pagina = request.GET.get('page', 1)

    try:
        paginado = Paginator(info, 6)
        info = paginado.page(nro_pagina)
    except:
        raise Http404

    return render(request, 'tareas.html', {'tareas': info, 'paginado': paginado})


def scanner(request):
    
    db = Database()
    
    frameWidth = 1280
    frameHeight = 720
    cap = cv.VideoCapture(0,cv.CAP_DSHOW)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, 150)

    #abro la camara y scaneo la foto con la 'q'
    while True:
        success, img = cap.read()
        img = cv.resize(img, (frameWidth, frameHeight))

        imgThres = preProcessing(img)
        biggest = getContours(imgThres)
        if biggest.size != 0:
            cv.drawContours(img, biggest, -1, (0, 255, 0), 23)
            cv.rectangle(img,(0,0),(460,90),(0,255,0),cv.FILLED)
            cv.putText(img,'Presiona Q para capturar',(10,30),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2,cv.LINE_AA)
            cv.putText(img,'y cerrar la pestaña',(10,60),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2,cv.LINE_AA)
            imgWarped = getWarp(img, biggest, frameWidth, frameHeight)
            imgAdaptativeThre = paperProcessing(imgWarped)
        else:
            img

        cv.imshow("Result", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            try:
                cv.imwrite('ProyectoWebApp/static/tarea.jpg', imgAdaptativeThre)
                break
            except:
                cap.release() #dejo de grabar
                cv.destroyAllWindows() #con esta linea ya deja abrir mas de una vez para escanear
                mensaje = 'Hubo un error al iniciar la cámara'
                return render(request,'error.html',{'mensaje': mensaje})

    cap.release() #dejo de grabar
    cv.destroyAllWindows() #con esta linea ya deja abrir mas de una vez para escanear

    #agarro la foto y la paso a una lista
    myconfig = r"--psm 6 --oem 3"
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    text = pytesseract.image_to_string(PIL.Image.open('ProyectoWebApp/static/tarea.jpg'), lang='eng', config=myconfig)

    texto_limpio = text.replace("\n\n", "\n")
    lineas = texto_limpio.split('\n')
    lineas.remove('')

    try:

        fecha_actual = datetime.now()

        username_m = request.user.username

        nombre_tarea_m = lineas[0]
        descripcion_m = lineas[1]
        fecha_inicio_m = fecha_actual.strftime("%Y/%m/%d %H:%M")
        fecha_fin_m = lineas[2]
        prioridad_m = lineas[3]

        db.create_tarea(nombre_tarea_m,prioridad_m,descripcion_m,fecha_inicio_m,fecha_fin_m,username_m)
        remove('ProyectoWebApp/static/tarea.jpg')

        return redirect('/tareas')

    except:
        print('Error al crear tarea mediante WebCam')
        print(lineas)
        remove('ProyectoWebApp/static/tarea.jpg')
        mensaje = 'Hubo un error al intentar crear la tarea'
        return render(request,'error.html',{'mensaje': mensaje})


def eliminar_tarea(request, id):
    db = Database()
    db.delete_tarea(id)

    return redirect('/tareas')


def detalle_tarea(request, id):
    db = Database()
    tarea = db.get_tarea(id)
    # prod = Item.objects.get(idproducto = id)

    try:
        fecha_inicio_t = tarea[3].strftime('%Y-%m-%d')
        hora_inicio_t = tarea[3].strftime('%H:%M')
        fecha_fin_t = tarea[4].strftime('%Y-%m-%d')
        usuario = db.get_user(tarea[7])

        data = {
            'tarea': tarea,
            'archivado': tarea[8],
            'prioridad': convertir_prioridad(tarea[6]),
            'estado': convertir_estado(tarea[5]),
            'fecha_inicio_t': fecha_inicio_t,
            'hora_inicio_t': hora_inicio_t,
            'fecha_fin_t': fecha_fin_t,
            'usuario': usuario
        }
    except:
        mensaje = 'Hubo un error al intentar abrir la tarea: ' + tarea[1]
        return render(request,'error.html',{'mensaje': mensaje})

    return render(request, 'detalleTarea.html', data)


def exportar_tarea(request, id):
    db = Database()
    tarea = db.get_tarea(id)

    fecha_inicio_t = tarea[3].strftime('%Y-%m-%d')
    hora_inicio_t = tarea[3].strftime('%H:%M')
    fecha_fin_t = tarea[4].strftime('%Y-%m-%d')

    prioridad = convertir_prioridad(tarea[6])
    estado = convertir_estado(tarea[5])
    usuario = db.get_user(tarea[7])

    objeto_tarea = Tarea(tarea[1], tarea[2], fecha_inicio_t + ' ' +
                         hora_inicio_t, fecha_fin_t, estado, prioridad, usuario[0])
    objeto_tarea = objeto_tarea.__dict__

    tarea_json = json.dumps(objeto_tarea)
    nombre_archivo = str(tarea[1]) + '.json'

    jsonFile = open('ProyectoWebApp/static/data.json', 'w+')
    jsonFile.write(tarea_json)
    jsonFile.close()

    jsonFile = open('ProyectoWebApp/static/data.json', 'rb')
    data = jsonFile.read()
    jsonFile.close()

    response = HttpResponse(data, content_type='text/plain')
    response['Content-Disposition'] = 'attachement; filename=%s' % nombre_archivo

    remove('ProyectoWebApp/static/data.json')

    return response


def pagina_error(request):
    return render(request, 'error.html')
