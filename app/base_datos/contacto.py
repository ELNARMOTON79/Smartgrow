import conexion
import mysql.connector

def crear(nombre, apellido, telefono):
    conn = conexion.conectar()
    cursor = conn.cursor()
    try:
        sentencia = "INSERT INTO personas (nombre, apellido, telefono) VALUES (%s, %s, %s)"
        cursor.execute(sentencia, (nombre, apellido, telefono))
        conn.commit()
        print("Contacto creado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al crear el contacto: {err}")
    finally:
        cursor.close()
        conexion.cerrar(conn)

def leer():
    conn = conexion.conectar()
    cursor = conn.cursor()
    try:
        sentencia = "SELECT * FROM personas"
        cursor.execute(sentencia)
        for fila in cursor.fetchall():
            print(fila)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conexion.cerrar(conn)

def actualizar(id, nombre, apellido, telefono):
    conn = conexion.conectar()
    cursor = conn.cursor()
    try:
        sentencia = "UPDATE personas SET nombre = %s, apellido = %s, telefono = %s WHERE id = %s"
        cursor.execute(sentencia, (nombre, apellido, telefono, id))
        conn.commit()
        print("Contacto actualizado")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conexion.cerrar(conn)

def eliminar(id):
    conn = conexion.conectar()
    cursor = conn.cursor()
    try:
        sentencia = "DELETE FROM personas WHERE id = %s"
        cursor.execute(sentencia, (id,))
        conn.commit()
        print("Contacto eliminado")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conexion.cerrar(conn)