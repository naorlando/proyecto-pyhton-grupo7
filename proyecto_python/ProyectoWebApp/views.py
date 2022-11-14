from django.shortcuts import render, HttpResponse

# Create your views here.


def home(request):
    return HttpResponse("Inicio")

def eventos(request):
    return HttpResponse("Eventos")

def edicion(request):
    return HttpResponse("Edicion")
