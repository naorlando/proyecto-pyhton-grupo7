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
    def all_users (self):
        sql='SELECT * FROM producto'

        self.cursor.execute(sql)
        users=self.cursor.fetchall()
        users=list(users)
        for user in users:
            print(user[1])
        return users



    