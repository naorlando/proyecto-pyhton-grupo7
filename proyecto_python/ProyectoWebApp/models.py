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
        password='1234',
        db='python-utn'
    ) 
    #chequeo que la bbdd este en funcionamiento, sino no se conecta
    #y lanza un error (no llega al print)
        self.cursor = self.connection.cursor()
        print("La conexion fue exitosa")
    
    #METODOS
    def all_task(self):
        sql='SELECT * FROM tareas'

        self.cursor.execute(sql)
        tasks=self.cursor.fetchall()
        tasks=list(tasks)
        # for task in tasks:
        #     print(task[1])
        return tasks

    def get_tarea (self,id):
        
        query = "SELECT * FROM tareas WHERE idtarea={}".format(id)

        try:
            self.cursor.execute(query)
            task = self.cursor.fetchone()

            # print("ID:",task[0])
            # print("Nombre:",task[1])
            # print("Prioridad:",task[2])
            # print("Descripcion:",task[3])
            # print("Fecha Inicio:",task[4])
            # print("Fecha Fin:",task[5])

            return task

        except Exception as e:
            print("La tarea no existe")
            raise

    def update_tarea (self, id,nombre_tarea_m,prioridad_m,descripcion_m,fecha_inicio_m,fecha_fin_m):

        query= "UPDATE tareas SET nombre_tarea = '{}', prioridad = '{}', descripcion = '{}', fecha_inicio = '{}',fecha_fin = '{}' WHERE idtarea = {};".format(nombre_tarea_m,prioridad_m,descripcion_m,fecha_inicio_m,fecha_fin_m,id)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al modificar la tarea")
            raise
    
    def delete_tarea (self,id):

        query = "DELETE FROM tareas WHERE idtarea = {};".format(id)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al eliminar la tarea")
            raise

    def create_tarea (self,nombre_tarea_m,prioridad_m,descripcion_m,fecha_inicio_m,fecha_fin_m):

        query= "INSERT INTO tareas (nombre_tarea,prioridad,descripcion,fecha_inicio,fecha_fin) VALUES ('{}','{}','{}','{}','{}');".format(nombre_tarea_m,prioridad_m,descripcion_m,fecha_inicio_m,fecha_fin_m)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al crear la tarea")
            raise
