import customtkinter as ctk
from PIL import Image, ImageTk
import os
import threading
import time
from VIEWS.sidebar import Sidebar
from VIEWS.maincontent import MainContent
from VIEWS.colors import COLORS
from typing import Dict

# NUEVO: Importa el controlador de Arduino
from sensores.arduino_controller import ArduinoController



# Set appearance mode and default color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Smartgrow - Sistema hidroponía")
        self.geometry("1200x700")
        
        self.minsize(900, 600)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize notification system
        self.alerts = []
        self.max_alerts = 10
        
        self.running = True
        
        # Create sidebar
        self.sidebar = Sidebar(self)
        
        # Create main content
        self.main_content = MainContent(self, on_settings_saved=self.on_settings_saved)
        # Connect sidebar to main content
        self.sidebar.main_content = self.main_content
        
        # NUEVO: Instancia el controlador de Arduino (ajusta el puerto según tu sistema)
        self.arduino_controller = ArduinoController(port="COM12", baudrate=9600)  # Cambia COM3 por el puerto correcto

        # Nuevo: almacena configuración ideal
        self.ideal_settings = {}

        # Start data update thread
        self.start_data_thread()
    
    def handle_sensor_alert(self, alert_data: Dict):
        """Handle sensor alerts from Arduino controller"""
        # Add alert to list
        self.alerts.insert(0, alert_data)
        
        # Keep only recent alerts
        if len(self.alerts) > self.max_alerts:
            self.alerts = self.alerts[:self.max_alerts]
        
        # Update UI with alert
        self.after(0, lambda: self.display_alert(alert_data))
    
    def display_alert(self, alert_data: Dict):
        """Display alert in the UI"""
        if hasattr(self.main_content, 'show_alert'):
            self.main_content.show_alert(alert_data)
        
        # Print to console
        print(f"ALERT: {alert_data['message']}")
    
    def start_data_thread(self):
        """Start background thread for Arduino data updates"""
        self.data_thread = threading.Thread(target=self.update_data_loop, daemon=True)
        self.data_thread.start()
    
    def on_settings_saved(self, settings):
        """Callback para guardar configuración ideal (ahora rangos)"""
        def parse_float(val):
            try:
                return float(val.lstrip("0").replace(",", ".").strip()) if val.strip() != "" else None
            except Exception:
                return None

        try:
            self.ideal_settings = {
                "pH": {
                    "min": parse_float(settings["pH"]["min"]),
                    "max": parse_float(settings["pH"]["max"])
                },
                "Temperatura": {
                    "min": parse_float(settings["Temperatura"]["min"]),
                    "max": parse_float(settings["Temperatura"]["max"])
                },
                "EC": {
                    "min": parse_float(settings["EC"]["min"]),
                    "max": parse_float(settings["EC"]["max"])
                }
            }
            print("Configuración ideal guardada:", self.ideal_settingitgs)
        except Exception as e:
            print(f"Error al guardar configuración ideal: {e}")

    def update_data_loop(self):
        """Background loop for updating sensor data"""
        while self.running:
            try:
                if self.arduino_controller:
                    sensor_data = self.arduino_controller.read_sensors()
                    if sensor_data:
                        print("Datos recibidos del Arduino:", sensor_data)
                        mapped_data = {
                            "temperature": sensor_data.get("temp_C"),
                            "ph": sensor_data.get("pH"),
                            "ec": sensor_data.get("EC_mS_cm"),
                            "water_level": sensor_data.get("nivelAgua_cm"),
                        }
                        self.after(0, lambda data=mapped_data: self.main_content.update_sensor_display(data))
                        # Nuevo: comparar con configuración ideal y generar alerta si corresponde
                        self.check_and_alert(mapped_data)
                time.sleep(2)  # Update every 2 seconds
            except Exception as e:
                print(f"Error in data update loop: {e}")
                time.sleep(5)  # Wait longer on error

    def check_and_alert(self, mapped_data):
        """Compara valores actuales con los rangos ideales y genera alerta si es necesario"""
        if not self.ideal_settings:
            return
        alerts = []
        # pH
        ph_range = self.ideal_settings.get("pH", {})
        actual_ph = mapped_data.get("ph")
        if actual_ph is not None:
            try:
                actual_ph = float(actual_ph)
                if ph_range.get("min") is not None and actual_ph < ph_range["min"]:
                    alerts.append({"message": f"pH bajo: {actual_ph}", "sensor": "pH", "value": actual_ph, "type": "pH bajo", "severity": "medium"})
                elif ph_range.get("max") is not None and actual_ph > ph_range["max"]:
                    alerts.append({"message": f"pH alto: {actual_ph}", "sensor": "pH", "value": actual_ph, "type": "pH alto", "severity": "medium"})
            except Exception:
                pass
        # Temperatura
        temp_range = self.ideal_settings.get("Temperatura", {})
        actual_temp = mapped_data.get("temperature")
        if actual_temp is not None:
            try:
                actual_temp = float(actual_temp)
                if temp_range.get("min") is not None and actual_temp < temp_range["min"]:
                    alerts.append({"message": f"Temperatura baja: {actual_temp}°C", "sensor": "temperatura", "value": f"{actual_temp}°C", "type": "Temperatura baja", "severity": "medium"})
                elif temp_range.get("max") is not None and actual_temp > temp_range["max"]:
                    alerts.append({"message": f"Temperatura alta: {actual_temp}°C", "sensor": "temperatura", "value": f"{actual_temp}°C", "type": "Temperatura alta", "severity": "medium"})
            except Exception:
                pass
        # EC
        ec_range = self.ideal_settings.get("EC", {})
        actual_ec = mapped_data.get("ec")
        if actual_ec is not None:
            try:
                actual_ec = float(actual_ec)
                if ec_range.get("min") is not None and actual_ec < ec_range["min"]:
                    alerts.append({"message": f"EC baja: {actual_ec}", "sensor": "EC", "value": actual_ec, "type": "EC baja", "severity": "medium"})
                elif ec_range.get("max") is not None and actual_ec > ec_range["max"]:
                    alerts.append({"message": f"EC alta: {actual_ec}", "sensor": "EC", "value": actual_ec, "type": "EC alta", "severity": "medium"})
            except Exception:
                pass
        # Enviar alertas a notificaciones
        for alert in alerts:
            alert["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            self.after(0, lambda a=alert: self.main_content.show_alert(a))

    def on_closing(self):
        """Handle application closing"""
        self.running = False
        if hasattr(self, 'arduino_controller') and self.arduino_controller is not None:
            try:
                self.arduino_controller.disconnect()
            except Exception as e:
                print(f"Error disconnecting Arduino: {e}")
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()