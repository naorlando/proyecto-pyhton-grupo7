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
        sql='SELECT * FROM producto'

        self.cursor.execute(sql)
        users=self.cursor.fetchall()
        users=list(users)
        for user in users:
            print(user[1])
        return users

    def get_tarea (self,id):
        
        query = "SELECT * FROM producto WHERE idproducto={}".format(id)

        try:
            self.cursor.execute(query)
            prod = self.cursor.fetchone()

            print("ID:",prod[0])
            print("Nombre:",prod[1])
            print("Precio:",prod[2])
            print("Categoria:",prod[3])

            return prod

        except Exception as e:
            print("El producto no existe")
            raise

    def update_producto (self, id, nombre_producto_m, precio_m, categoria_m):

        query= "UPDATE producto SET nombre_producto = '{}', precio = {}, categoria = {} WHERE idproducto = {};".format(nombre_producto_m,precio_m,categoria_m,id)

        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print("Error al modificar el producto")
            raise



