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
    def all_users (self):
        sql='SELECT * FROM tarea'

        self.cursor.execute(sql)
        users=self.cursor.fetchall()
        users=list(users)
        for user in users:
            print(user[1])
        return users

    def get_tarea (self,id):
        
        query = "SELECT * FROM tarea WHERE idtarea={}".format(id)

        try:
            self.cursor.execute(query)
            task = self.cursor.fetchone()

            print("ID:",task[0])
            print("Nombre:",task[1])
            print("fechaini:",task[3])
            print("prioridad:",task[5])

            return task

        except Exception as e:
            print("El producto no existe")
            raise

    def update_producto (self, id,nombre_tarea_m,descripcion_m,fecha_inicio_m,fecha_finalizacion_m,prioridad_m):

        query= "UPDATE producto SET nombre_tarea = '{}', descripcion = '{}', prioridad = '{}',fecha_inicio ={}, fecha_fin={}, WHERE idproducto = {};".format(nombre_tarea_m,descripcion_m,prioridad_m,fecha_inicio_m,fecha_finalizacion_m,id)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al modificar el tarea")
            raise



