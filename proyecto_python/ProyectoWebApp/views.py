from django.shortcuts import render
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