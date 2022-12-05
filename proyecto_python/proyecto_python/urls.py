"""proyecto_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ProyectoWebApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='Home'),
    path('tareas/',views.listar_tareas,name='Tareas'),
    path('tareas/archivadas',views.listar_tareas_archivadas,name='TareasArchivadas'),
    path('signup/',views.signup, name='signup'),
    path('signin/',views.signin, name='signin'),
    path('logout/',views.signout, name='logout'),
    path('tareas/modificar/<int:id>',views.modificar_tarea,name='ModificarTarea'),
    path('tareas/modificar-estado/<int:id>/<int:estado>',views.modificar_estado,name='ModificarEstado'),
    path('tareas/archivar-tarea/<int:id>',views.archivar_tarea,name='ArchivarTarea'),
    path('tareas/desarchivar-tarea/<int:id>',views.desarchivar_tarea,name='DesarchivarTarea'),
    path('tareas/crear',views.crear_tarea,name='CrearTarea'),
    path('tareas/crear/camera',views.scanner,name='CrearTareaCamera'),
    path('tareas/eliminar/<int:id>',views.eliminar_tarea,name='EliminarTarea'),
    path('tareas/<int:id>',views.tarea_id,name='VerTarea'),
    path('tareas/exportar/<int:id>',views.exportar_tarea,name='ExportarTarea')
]
