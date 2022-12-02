from django.db import models
import pymysql
import datetime as d

#definimos la clase Tarea
class Tarea():
    def __init__(self, nombre_tarea, prioridad, descripcion, fecha_inicio, fecha_fin):
        self.nombre_tarea = nombre_tarea
        self.prioridad = prioridad
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

#definimos la clase de nuestra Base de datos
class Database():
    #creamos el constructor con la bbdd elegida a traves de pymysql
    def __init__(self):
        self.connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='usuariospython'
    ) 
    #chequeo que la bbdd este en funcionamiento, sino no se conecta
    #y lanza un error (no llega al print)
        self.cursor = self.connection.cursor()
        print("La conexion fue exitosa")
    
    #METODOS
    def all_task(self):
        query ='SELECT * FROM tareas WHERE archivado = 0 ORDER BY prioridad_idprioridad, fecha_fin;'
        try:
            self.cursor.execute(query)
            tasks = self.cursor.fetchall()
            tasks = list(tasks)
            return tasks
        except Exception:
            print("No se pudieron obtener las tareas")
            raise

    def get_tarea(self, ide):
        query = "SELECT * FROM tareas WHERE idtarea = '{}'".format(ide)

        try:
            self.cursor.execute(query)
            task = self.cursor.fetchone()
            return task

        except Exception as e:
            print("La tarea no existe")
            raise

    def get_tareas_x_prioridad(self, prioridad_m):
        query = "SELECT * FROM tareas WHERE prioridad = '{}'".format(prioridad_m)
        
        try:
            self.cursor.execute(query)
            tasks = self.cursor.fetchall()
            return tasks
        except Exception as e:
            print("Error al obtener las tareas segun su prioridad")
            raise

    def get_tareas_caducadas(self):
        query = 'SELECT * FROM tareas WHERE fecha_fin < CURDATE()'
        try:
            self.cursor.execute(query)
            tasks = self.cursor.fetchall()
            return tasks
        except Exception:
            print("No se pudieron obtener las tareas caducadas")
            raise

    def update_tarea(self, ide, nombre_tarea_m, prioridad_m, descripcion_m, fecha_inicio_m, fecha_fin_m):
        query = "UPDATE tareas SET nombre_tarea='{}', prioridad_idprioridad=(SELECT idprioridad FROM prioridad WHERE nombre_prioridad='{}'),\
            descripcion='{}', fecha_fin='{}' WHERE idtarea = '{}'".format(nombre_tarea_m, prioridad_m, descripcion_m, fecha_fin_m, ide)
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print("Error al modificar la tarea")
            raise

    def create_tarea(self, nombre_tarea_m, prioridad_m, descripcion_m, fecha_inicio_m, fecha_fin_m, username_m):
        query = "INSERT INTO tareas(nombre_tarea, prioridad_idprioridad, descripcion, fecha_fin,auth_user_id)\
        VALUES ('{}',(SELECT idprioridad FROM prioridad WHERE nombre_prioridad='{}'),'{}','{}',(SELECT id FROM auth_user WHERE username='{}'))"\
        .format(nombre_tarea_m, prioridad_m , descripcion_m, fecha_fin_m, username_m)
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception:
            print("No se pudo agregar la tarea")
            raise

    def archivo_tarea(self, ide, valor): #Si valor = 1 se archiva, si valor = 0 se desarchiva
        query = "UPDATE tareas SET archivado = '{}' WHERE idtarea = '{}'".format(valor, ide)
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception:
            print("No se pudo archivar la tarea")
            raise

    def all_task_arch(self):
        query ='SELECT * FROM tareas WHERE archivado = 1 ORDER BY prioridad_idprioridad, fecha_fin;'     
        try: 
            self.cursor.execute(query)
            tasks = self.cursor.fetchall()
            tasks = list(tasks)
            return tasks
        except Exception:
            print("No se pudieron obtener las tareas archivadas")
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

