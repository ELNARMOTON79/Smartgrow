import serial
import json
import threading

class ArduinoController:
    def __init__(self, port="COM12", baudrate=9600, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.lock = threading.Lock()
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
                    return json.loads(line)
            except Exception as e:
                print(f"Error reading from Arduino: {e}")
        return None

    def disconnect(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
