import serial
import serial.tools.list_ports
import json
import time
import threading
from typing import Dict, Optional, List

class ArduinoController:
    def __init__(self, auto_connect=True):
        self.serial_connection = None
        self.port = None
        self.baudrate = 9600
        self.timeout = 2
        self.connected = False
        self.last_data = {}
        self.connection_lock = threading.Lock()
        
        # Auto-connect on initialization (optional)
        if auto_connect:
            try:
                self.auto_connect()
            except Exception as e:
                print(f"Failed to auto-connect: {e}")
                self.connected = False
    
    def find_arduino_ports(self) -> List[str]:
        """Find available Arduino ports"""
        arduino_ports = []
        try:
            ports = serial.tools.list_ports.comports()
            
            for port in ports:
                # Look for common Arduino identifiers
                if any(keyword in port.description.lower() for keyword in 
                       ['arduino', 'ch340', 'cp210', 'ftdi', 'usb serial']):
                    arduino_ports.append(port.device)
        except Exception as e:
            print(f"Error finding ports: {e}")
        
        return arduino_ports
    
    def auto_connect(self):
        """Automatically connect to Arduino"""
        arduino_ports = self.find_arduino_ports()
        
        if not arduino_ports:
            print("No Arduino ports found. App will run in simulation mode.")
            return False
        
        for port in arduino_ports:
            if self.connect(port):
                print(f"Successfully connected to Arduino on {port}")
                return True
        
        print("Arduino found but connection failed. App will run in simulation mode.")
        return False
    
    def connect(self, port: str = None) -> bool:
        """Connect to Arduino on specified port"""
        with self.connection_lock:
            try:
                if port:
                    self.port = port
                
                if not self.port:
                    return False
                
                self.serial_connection = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=self.timeout
                )
                
                # Wait for Arduino to initialize
                time.sleep(2)
                
                # Test connection
                if self.test_connection():
                    self.connected = True
                    return True
                else:
                    self.disconnect()
                    return False
                    
            except Exception as e:
                print(f"Error connecting to Arduino: {e}")
                self.connected = False
                return False
    
    def test_connection(self) -> bool:
        """Test if Arduino is responding"""
        try:
            # Send test command
            self.serial_connection.write(b"TEST\n")
            self.serial_connection.flush()
            
            # Wait for response
            response = self.serial_connection.readline().decode().strip()
            return "OK" in response or len(response) > 0
            
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Arduino"""
        with self.connection_lock:
            self.connected = False
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
            self.serial_connection = None
    
    def is_connected(self) -> bool:
        """Check if Arduino is connected"""
        return self.connected and self.serial_connection and self.serial_connection.is_open
    
    def read_sensors(self) -> Optional[Dict]:
        """Read sensor data from Arduino or return simulated data"""
        if not self.is_connected():
            # Return simulated data when not connected
            return self.get_simulated_data()
        
        try:
            with self.connection_lock:
                # Request sensor data
                self.serial_connection.write(b"READ_SENSORS\n")
                self.serial_connection.flush()
                
                # Read response
                response = self.serial_connection.readline().decode().strip()
                
                if response:
                    # Try to parse JSON response
                    try:
                        data = json.loads(response)
                        self.last_data = data
                        return data
                    except json.JSONDecodeError:
                        # If not JSON, parse simple format
                        return self.parse_simple_format(response)
                        
        except Exception as e:
            print(f"Error reading sensors: {e}")
            self.connected = False
            # Return simulated data on error
            return self.get_simulated_data()
        
        return self.last_data if self.last_data else self.get_simulated_data()
    
    def parse_simple_format(self, response: str) -> Dict:
        """Parse simple sensor data format"""
        data = {}
        try:
            # Expected format: "temp:25.5,humidity:60.2,ph:6.8,tds:850"
            pairs = response.split(',')
            for pair in pairs:
                key, value = pair.split(':')
                data[key.strip()] = float(value.strip())
        except Exception as e:
            print(f"Error parsing sensor data: {e}")
        
        return data
    
    def get_simulated_data(self) -> Dict:
        """Generate simulated sensor data for testing"""
        import random
        return {
            "temperature": round(20 + random.uniform(-5, 10), 1),
            "humidity": round(50 + random.uniform(-20, 30), 1),
            "ph": round(6.5 + random.uniform(-1, 1), 1),
            "tds": round(800 + random.uniform(-200, 400)),
            "water_level": round(random.uniform(20, 100), 1),
            "light_intensity": round(random.uniform(300, 1000)),
            "status": "simulated"
        }
    
    def send_command(self, command: str) -> bool:
        """Send command to Arduino"""
        if not self.is_connected():
            print(f"Simulated command sent: {command}")
            return True  # Return True for simulation mode
        
        try:
            with self.connection_lock:
                self.serial_connection.write(f"{command}\n".encode())
                self.serial_connection.flush()
                return True
        except Exception as e:
            print(f"Error sending command: {e}")
            return False
    
    def get_last_data(self) -> Dict:
        """Get last received sensor data"""
        return self.last_data.copy() if self.last_data else {}
    
    def reconnect(self) -> bool:
        """Attempt to reconnect to Arduino"""
        self.disconnect()
        time.sleep(1)
        return self.auto_connect()
