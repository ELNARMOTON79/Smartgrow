from base_datos import conexion
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

def obtener_todos():
    conn = conexion.conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT fecha, hora, temperatura, ph FROM historial ORDER BY fecha, hora")
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as err:
        print(f"Error al obtener los contactos: {err}")
        return []
    finally:
        cursor.close()
        conexion.cerrar(conn)

def filtrar_por_fecha(fecha):
    conn = conexion.conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT fecha, hora, temperatura, ph FROM historial WHERE fecha = %s ORDER BY hora", (fecha,))
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as err:
        print(f"Error al filtrar por fecha: {err}")
        return []
    finally:
        cursor.close()
        conexion.cerrar(conn)

def filtrar_por_hora(fecha, hora_inicio, hora_fin):
    conn = conexion.conectar()
    cursor = conn.cursor()
    try:
        query = """
            SELECT fecha, hora, temperatura, ph 
            FROM historial 
            WHERE fecha = %s AND hora BETWEEN %s AND %s 
            ORDER BY hora
        """
        cursor.execute(query, (fecha, hora_inicio, hora_fin))
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as err:
        print(f"Error al filtrar por hora: {err}")
        return []
    finally:
        cursor.close()
        conexion.cerrar(conn)