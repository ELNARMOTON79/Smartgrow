import serial
import json
import threading
import sys
sys.path.append('../base_datos')  # Add the database module path
from base_datos import contacto  # Import the contacto module directly
from datetime import datetime  # Import datetime to generate timestamps

class ArduinoController:
    def __init__(self, port="COM12", baudrate=9600, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.lock = threading.Lock()
        self.alert_callbacks = []
        try:
            self.serial = serial.Serial(port, baudrate, timeout=timeout)
        except Exception as e:
            print(f"Error opening serial port: {e}")
            self.serial = None

    def read_sensors(self):
        """Envía el comando y lee los datos JSON del Arduino"""
        if not self.serial or not self.serial.is_open:
            return None
        with self.lock:
            try:
                self.serial.reset_input_buffer()
                self.serial.write(b'READ_SENSORS\n')
                line = self.serial.readline().decode('utf-8').strip()
                if line.startswith('{') and line.endswith('}'):
                    sensor_data = json.loads(line)
                    print(f"Datos recibidos del Arduino: {sensor_data}")  # Log the received data
                    
                    # Guarda los datos en la base de datos
                    self.process_sensor_data(sensor_data)
                    
                    # Insertar datos en la base de datos
                    now = datetime.now()
                    fecha = now.strftime("%Y-%m-%d")
                    hora = now.strftime("%H:%M:%S")
                    temperatura = sensor_data.get("temp_C")  # Use the actual value from 'temp_C'
                    ph = sensor_data.get("pH")  # Use the actual value from 'pH'
                    conductividad = sensor_data.get("EC_mS_cm")  # Use the actual value from 'EC_mS_cm'
                    
                    # Ensure values are not None before inserting
                    if temperatura is not None and ph is not None and conductividad is not None:
                        contacto.crear(fecha, hora, temperatura, ph, conductividad)
                    
                    return sensor_data
            except Exception as e:
                print(f"Error reading from Arduino: {e}")
        return None

    def add_alert_callback(self, callback):
        """Add a callback to handle alerts."""
        self.alert_callbacks.append(callback)

    def process_sensor_data(self, sensor_data):
        """Process sensor data and trigger alerts if necessary."""
        if "status" in sensor_data and sensor_data["status"] == "alert":
            for callback in self.alert_callbacks:
                callback(sensor_data)

    def send_ideal_ranges(self, ph_range, ec_range):
        """Send ideal ranges for pH and EC to Arduino."""
        if not self.serial or not self.serial.is_open:
            return
        with self.lock:
            try:
                data = {
                    "ph_min": ph_range.get("min", 5.5),
                    "ph_max": ph_range.get("max", 7.5),
                    "ec_min": ec_range.get("min", 1.2),
                    "ec_max": ec_range.get("max", 2.5)
                }
                self.serial.write(json.dumps(data).encode('utf-8') + b'\n')
                print(f"Sent ideal ranges to Arduino: {data}")
            except Exception as e:
                print(f"Error sending ideal ranges to Arduino: {e}")

    def disconnect(self):
        if self.serial and self.serial.is_open:
            self.serial.close()

