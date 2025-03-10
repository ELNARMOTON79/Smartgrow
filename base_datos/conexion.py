import mysql.connector

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='', 
        database='smarthgrow'
    )

def cerrar(conexion):
    conexion.close()

if __name__ == '__main__':
    conexion = conectar()
    cerrar(conexion)