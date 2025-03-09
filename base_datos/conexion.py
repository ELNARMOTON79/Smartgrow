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
    print('Conexión cerrada')

if __name__ == '__main__':
    conexion = conectar()
    print("Conexión exitosa")
    cerrar(conexion)