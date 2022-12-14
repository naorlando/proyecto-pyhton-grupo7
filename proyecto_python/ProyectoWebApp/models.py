from django.db import models
import pymysql
import datetime as d

#definimos la clase Tarea
class Tarea():
    def __init__(self, nombre_tarea, descripcion, fecha_inicio, fecha_fin, estado, prioridad, usuario):
        self.nombre_tarea = nombre_tarea
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.prioridad = prioridad
        self.usuario = usuario


#definimos la clase de nuestra Base de datos
class Database():
    #creamos el constructor con la bbdd elegida a traves de pymysql
    def __init__(self):
        self.connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='db-proyecto'
    ) 
    #chequeo que la bbdd este en funcionamiento, sino no se conecta
    #y lanza un error (no llega al print)
        self.cursor = self.connection.cursor()
        print("La conexion fue exitosa")
    
    #METODOS
    def all_task(self):
        query = "SELECT * FROM tareas WHERE archivado = 0 ORDER BY prioridad_idprioridad, fecha_fin"
        try:
            self.cursor.execute(query)
            tasks = self.cursor.fetchall()
            tasks = list(tasks)
            return tasks
        except Exception:
            print("No se pudieron obtener las tareas")
            raise

    def tareas_archivadas(self):
        query = "SELECT * FROM tareas WHERE archivado = 1 ORDER BY prioridad_idprioridad, fecha_fin"     
        try: 
            self.cursor.execute(query)
            tasks = self.cursor.fetchall()
            tasks = list(tasks)
            return tasks
        except Exception:
            print("No se pudieron obtener las tareas archivadas")
            raise

    def get_tarea(self, ide):
        query = "SELECT * FROM tareas WHERE idtarea = '{}'".format(ide)
        try:
            self.cursor.execute(query)
            task = self.cursor.fetchone()
            return task
        except Exception:
            print("La tarea no existe")
            raise

    def get_tareas_x_prioridad(self, prioridad_m):
        query = "SELECT * FROM tareas WHERE prioridad = '{}'".format(prioridad_m)
        try:
            self.cursor.execute(query)
            tasks = self.cursor.fetchall()
            return tasks
        except Exception:
            print("Error al obtener las tareas segun su prioridad")
            raise

    def get_user(self, ide):
        query = "SELECT username FROM auth_user WHERE id = '{}'".format(ide)
        try:
            self.cursor.execute(query)
            username = self.cursor.fetchone()
            return username
        except Exception:
            print("El usuario no existe")
            raise

    def get_tareas_usuario(self, usuario):
        query = "SELECT * FROM tareas WHERE auth_user_id = (SELECT id FROM auth_user WHERE username = '{}')\
            AND archivado = 0 ORDER BY prioridad_idprioridad, fecha_fin".format(usuario)
        try:
            self.cursor.execute(query)
            tareas_encontradas = self.cursor.fetchall()
            return tareas_encontradas
        except Exception:
            print("No se pudo encontrar ninguna tarea")
            raise

    def get_tarea_buscada(self, tarea_buscada):
        query = "SELECT * FROM tareas WHERE nombre_tarea LIKE '%{}%'\
            AND archivado = 0".format(tarea_buscada)
        try:
            self.cursor.execute(query)
            tareas_encontradas = self.cursor.fetchall()
            return tareas_encontradas
        except Exception:
            print("No se pudo encontrar ninguna tarea")
            raise

    def update_tarea(self, ide, nombre_tarea_m, prioridad_m, descripcion_m, fecha_inicio_m, fecha_fin_m):
        query = "UPDATE tareas SET nombre_tarea = '{}', descripcion = '{}', fecha_inicio = '{}',\
            fecha_fin = '{}', prioridad_idprioridad = (SELECT idprioridad FROM prioridad WHERE nombre_prioridad = '{}')\
            WHERE idtarea = '{}'".format(nombre_tarea_m, descripcion_m, fecha_inicio_m, fecha_fin_m, prioridad_m, ide)
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception:
            print("Error al modificar la tarea")
            raise

    def update_estado_tarea(self, ide, estado):
        query = "UPDATE tareas SET estado_idestado = '{}' WHERE idtarea = '{}'".format(estado, ide)
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception:
            print("Error al modificar el estado de la tarea")
            raise

    def archivar_tarea(self, ide):
        query = "UPDATE tareas SET archivado = '1' WHERE idtarea = '{}'".format(ide)
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception:
            print("Error al archivar la tarea")
            raise

    def desarchivar_tarea(self, ide):
        query = "UPDATE tareas SET archivado = '0' WHERE idtarea = '{}'".format(ide)
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception:
            print("Error al desarchivar la tarea")
            raise

    def create_tarea(self, nombre_tarea_m, prioridad_m, descripcion_m, fecha_inicio_m, fecha_fin_m, username_m):
        query= "INSERT INTO tareas(nombre_tarea, descripcion, fecha_inicio, fecha_fin, prioridad_idprioridad, auth_user_id)\
            VALUES ('{}','{}','{}','{}',(SELECT idprioridad FROM prioridad WHERE nombre_prioridad='{}'),\
            (SELECT id FROM auth_user WHERE username='{}'))".format(nombre_tarea_m, descripcion_m, fecha_inicio_m, fecha_fin_m, prioridad_m, username_m)
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