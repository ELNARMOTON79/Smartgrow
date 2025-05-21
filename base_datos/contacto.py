import conexion
import mysql.connector
from datetime import datetime

def guardar_registro(temperatura, ph, conductividad, nivel_agua):
    conn = conexion.conectar()
    cursor = conn.cursor()
    try:
        sentencia = """
            INSERT INTO registros (temperatura, ph, conductividad, nivel_agua, fecha_hora)
            VALUES (%s, %s, %s, %s, %s)
        """
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sentencia, (temperatura, ph, conductividad, nivel_agua, fecha_actual))
        conn.commit()
        print("✅ Registro guardado correctamente.")
    except mysql.connector.Error as err:
        print(f"❌ Error al guardar el registro: {err}")
    finally:
        cursor.close()
        conexion.cerrar(conn)

def listar_registros():
    conn = conexion.conectar()
    cursor = conn.cursor()
    try:
        cursor.executor("SELECT * FROM registros")
        registros = cursor.fetchall()
        for registro in registros:
            print(f"ID: {registro[0]}, Temperatura: {registro[1]}, pH: {registro[2]}, Conductividad: {registro[3]}, Nivel de Agua: {registro[4]}, Fecha y Hora: {registro[5]}")
    except mysql.connector.Error as err:
        print(f"❌ Error al listar los registros: {err}")
    finally:
        cursor.close()
        conexion.cerrar(conn)
