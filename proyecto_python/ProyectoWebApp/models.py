from django.db import models
import pymysql

# Create your models here.

#definimos un objetos Base de datos
class Database():
    #creamos el constructor con la bbdd elegida a traves de pymysql
    def __init__(self):
        self.connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='python-utn'
    ) 
    #chequeo que la bbdd este en funcionamiento, sino no se conecta
    #y lanza un error (no llega al print)
        self.cursor = self.connection.cursor()
        print("La conexion fue exitosa")
    
    #METODOS
    def all_tareas (self):
        query ='SELECT * FROM tareas'

        self.cursor.execute(query)
        tareas=self.cursor.fetchall()
        tareas=list(tareas)
        for tarea in tareas:
            print(tarea[1])
        return tareas

    def get_tarea (self,id):
        query = "SELECT * FROM tareas WHERE idtarea = '{}'".format(id)

        try:
            self.cursor.execute(query)
            tarea = self.cursor.fetchone()

            print("ID:",tarea[0])
            print("Nombre:",tarea[1])
            print("Prioidad:",tarea[2])
            print("Descripcion:",tarea[3])
            print("Fecha de inicio:", tarea[5])
            print("Fecha de fin:", tarea[6])

            return tarea

        except Exception as e:
            print("La tarea no existe")
            raise

    def update_tarea(self, id, nombre_tarea_m, prioridad_m, descripcion_m, fecha_inicio_m, fecha_fin_m):

        query = "UPDATE tareas SET nombre_tarea = '{}', prioridad = '{}', descripcion = '{}',fecha_inicio = '{}', \
        fecha_fin = '{}' WHERE idtarea = '{}';".format(nombre_tarea_m, prioridad_m, descripcion_m, fecha_inicio_m, fecha_fin_m,id)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al modificar la tarea")
            raise



