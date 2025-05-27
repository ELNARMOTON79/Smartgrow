import conexion
import mysql.connector

def crear(fecha, hora, temperatura, ph, conductividad):
    conn = conexion.conectar()
    cursor = conn.cursor()
    try:
        sentencia = "INSERT INTO historial (fecha, hora, temperatura, ph, conductividad) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sentencia, (fecha, hora, temperatura, ph, conductividad))
        conn.commit()
        print("Contacto creado correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al crear el contacto: {err}")
    finally:
        cursor.close()
        conexion.cerrar(conn)