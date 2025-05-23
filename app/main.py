import customtkinter as ctk
from PIL import Image, ImageTk
import os
import threading
import time
from VIEWS.sidebar import Sidebar
from VIEWS.maincontent import MainContent
from VIEWS.colors import COLORS
from CONTROLLERS.arduino_controller import ArduinoController
from typing import Dict



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
        
        # Initialize Arduino controller with notifications
        self.arduino_controller = None
        try:
            self.arduino_controller = ArduinoController()
            if hasattr(self.arduino_controller, 'add_alert_callback'):
                self.arduino_controller.add_alert_callback(self.handle_sensor_alert)
            print("Arduino controller initialized with notification system")
        except Exception as e:
            print(f"Arduino not available: {e}")
            self.arduino_controller = None
        
        self.running = True
        
        # Create sidebar
        self.sidebar = Sidebar(self)
        
        # Create main content
        self.main_content = MainContent(self)
        
        # Pass Arduino controller to components
        if hasattr(self.sidebar, 'set_arduino_controller'):
            self.sidebar.set_arduino_controller(self.arduino_controller)
        if hasattr(self.main_content, 'set_arduino_controller'):
            self.main_content.set_arduino_controller(self.arduino_controller)
            
            # Also connect configuration and notifications views if they exist
            if hasattr(self.main_content, 'configuration_view') and hasattr(self.main_content, 'notifications_view'):
                # Set cross-references between views
                self.main_content.configuration_view.set_notifications_view(self.main_content.notifications_view)
        
        # Connect sidebar to main content
        self.sidebar.main_content = self.main_content
        
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
    
    def update_data_loop(self):
        """Background loop for updating sensor data"""
        while self.running:
            try:
                if self.arduino_controller:
                    sensor_data = self.arduino_controller.read_sensors()
                    if sensor_data:
                        # Update main content with new data (now optimized)
                        self.after(0, lambda data=sensor_data: self.main_content.update_sensor_display(data))
                            
                time.sleep(2)  # Update every 2 seconds
            except Exception as e:
                print(f"Error in data update loop: {e}")
                time.sleep(5)  # Wait longer on error
    
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