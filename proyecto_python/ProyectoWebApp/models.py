from django.db import models
import pymysql
import datetime as d

# Create your models here.

#definimos un objetos Base de datos
class Database():
    #creamos el constructor con la bbdd elegida a traves de pymysql
    def __init__(self):
        self.connection = pymysql.connect(
        host='localhost',
        user='root',
        password='01023',
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

    def get_tarea (self, ide):
        query = "SELECT * FROM tareas WHERE idtarea = '{}'".format(ide)

        try:
            self.cursor.execute(query)
            task = self.cursor.fetchone()

            print("ID:", task[0])
            print("Nombre:", task[1])
            print("Prioidad:", task[2])
            print("Descripcion:", task[3])
            print("Fecha de inicio:", task[4])
            print("Fecha de fin:", task[5])

            return task

        except Exception as e:
            print("La tarea no existe")
            raise

    def get_tareas_x_prioridad(self, prioridad_m):
        query = "SELECT * FROM tareas WHERE prioridad = '{}'".format(prioridad_m)
        
        try:
            self.cursor.execute(query)
            tasks = self.cursor.fetchall()
            for task in tasks:
                print("-----")
                print("Nombre:", task[1])
                print("Descripcion:", task[3])
            return tasks

        except Exception as e:
            print("Error al obtener las tareas segun su prioridad")
            raise

    def update_tarea(self, ide, nombre_tarea_m, prioridad_m, descripcion_m, fecha_inicio_m, fecha_fin_m):
        query = "UPDATE tareas SET nombre_tarea = '{}', prioridad = '{}', descripcion = '{}', fecha_inicio = '{}',\
        fecha_fin = '{}' WHERE idtarea = '{}'".format(nombre_tarea_m, prioridad_m, descripcion_m, fecha_inicio_m, fecha_fin_m, ide)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al modificar la tarea")
            raise
    
    def update_nombre_tarea(self, ide, nombre_tarea_m):
        query = "UPDATE tareas SET nombre_tarea = '{}' WHERE idtarea = '{}'".format(nombre_tarea_m, ide)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al modificar el nombre")
            raise

    def update_prioridad_tarea(self, ide, prioridad_m):
        query = "UPDATE tareas SET prioridad = '{}' WHERE idtarea = '{}'".format(prioridad_m, ide)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al modificar la prioridad")
            raise
    
    def update_descripcion_tarea(self, ide, prioridad_m):
        query = "UPDATE tareas SET descripcion = '{}' WHERE idtarea = '{}'".format(prioridad_m, ide)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al modificar la prioridad")
            raise
    
    def update_fecha_inicio_tarea(self, ide, fecha_inicio_m):
        query = "UPDATE tareas SET fecha_inicio = '{}' WHERE idtarea = '{}'".format(fecha_inicio_m, ide)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al modificar la fecha de inicio")
            raise

    def update_fecha_fin_tarea(self, ide, fecha_fin_m):
        query = "UPDATE tareas SET fecha_fin = '{}' WHERE idtarea = '{}'".format(fecha_fin_m, ide)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al modificar la fecha de fin")
            raise

    def create_tarea(self, nombre_tarea_m, prioridad_m, descripcion_m, fecha_inicio_m, fecha_fin_m):
        query="INSERT INTO tareas(nombre_tarea, prioridad, descripcion, fecha_inicio, fecha_fin)\
        VALUES ('{}','{}','{}','{}','{}')".format(nombre_tarea_m, prioridad_m, descripcion_m, fecha_inicio_m, fecha_fin_m)
        
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception:
            print("No se pudo agregar la tarea")
            raise
        
    def delete_tarea(self, ide):
        query = "DELETE FROM tareas WHERE idtarea = '{}'".format(ide)
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception:
            print("No se pudo eliminar la tarea")
            raise
    
    def close(self):
        self.connection.close()

f1 = d.datetime(2022, 11, 23, 16, 45) #23-11-2022 16:45
f2 = d.datetime(2022, 12, 24, 0, 0) 
db = Database()
#db.update_descripcion_tarea(6, "tarea dos")
#db.update_prioridad_tarea(6, "alta")
#db.update_fecha_fin_tarea(5, f2)
db.get_tareas_x_prioridad("baja")
db.close()