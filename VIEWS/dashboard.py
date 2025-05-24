import customtkinter as ctk
from PIL import Image, ImageTk
import os
from VIEWS.colors import COLORS
from typing import Dict, Optional

class Dashboard:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=15)
        self.arduino_controller = None
        
        # Main container with proper layout
        main_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top section for stats (fixed height)
        top_section = ctk.CTkFrame(main_container, fg_color="transparent", height=120)
        top_section.pack(fill="x", pady=(0, 10))
        top_section.pack_propagate(False)  # Maintain fixed height
        
        # Sección de estadísticas
        stats_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.stats_labels = {}
        stats_data = [
            {"title": "Temperature", "value": "Waiting...", "icon": "🌡️", "color": COLORS.primary},
            {"title": "pH", "value": "Waiting...", "icon": "🧪", "color": COLORS.secondary},
            {"title": "Conductivity", "value": "Waiting...", "icon": "⚡", "color": "#F59E0B"},
            {"title": "Water Level", "value": "Waiting...", "icon": "🚰", "color": "#3B82F6"}
        ]
        
        for stat in stats_data:
            card, value_label = self._create_card(stats_frame, stat["title"], stat["value"], stat["icon"], stat["color"])
            card.pack(side="left", fill="both", expand=True, padx=3)
            self.stats_labels[stat["title"]] = value_label
        
        # Middle section for status and alerts (fixed height)
        middle_section = ctk.CTkFrame(main_container, fg_color="transparent", height=60)
        middle_section.pack(fill="x", pady=(0, 10))
        middle_section.pack_propagate(False)  # Maintain fixed height
        
        # Connection status and alerts in horizontal layout
        status_container = ctk.CTkFrame(middle_section, fg_color="transparent")
        status_container.pack(fill="both", expand=True, padx=10)
        
        # Connection status indicator
        self.connection_status = ctk.CTkLabel(
            status_container, text="🔴 Disconnected", font=ctk.CTkFont(size=12),
            text_color=COLORS.text_light
        )
        self.connection_status.pack(side="left", anchor="w", pady=5)
        
        # Alert label (takes remaining space)
        self.alert_label = ctk.CTkLabel(
            status_container, text="", font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS.danger
        )
        self.alert_label.pack(side="right", anchor="e", pady=5)
        
        # Bottom section for image (expandable)
        image_section = ctk.CTkFrame(main_container, fg_color="transparent")
        image_section.pack(fill="both", expand=True)
        
        # Contenedor de imagen
        self.image_label = ctk.CTkLabel(image_section, text="")
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bind resize event to the image section instead of frame
        image_section.bind("<Configure>", self._resize_image)
        
        self.tk_image = None
        self.original_image = None
        image_path = "./Sources/fondo_light.png"
        if os.path.exists(image_path):
            try:
                self.original_image = Image.open(image_path)
                # Initial image size
                self.ctk_image = ctk.CTkImage(
                    light_image=self.original_image,
                    dark_image=self.original_image,
                    size=(600, 400)
                )
                self.image_label.configure(image=self.ctk_image)
            except Exception as e:
                print(f"Error loading image: {e}")
                self.image_label.configure(text="Error cargando imagen", text_color=COLORS.danger)
        else:
            self.image_label.configure(text="Imagen no encontrada", text_color=COLORS.danger)

    def set_arduino_controller(self, controller):
        """Set the Arduino controller for this dashboard"""
        self.arduino_controller = controller
        if controller:
            # Add this dashboard as an alert callback
            controller.add_alert_callback(self.handle_alert)
            self.update_connection_status()

    def update_sensor_display(self, sensor_data: Dict):
        """Update dashboard with new sensor data from Arduino controller"""
        if not sensor_data:
            return
        
        # Map sensor data to display labels
        display_mapping = {
            "temperature": ("Temperature", "°C"),
            "ph": ("pH", ""),
            "ec": ("Conductivity", "mS/cm"),
            "water_level": ("Water Level", "cm"),
            "humidity": ("Humidity", "%"),
            "voltage": ("Voltage", "V")
        }
        
        for sensor_key, (display_key, unit) in display_mapping.items():
            if sensor_key in sensor_data and display_key in self.stats_labels:
                value = sensor_data[sensor_key]
                if isinstance(value, (int, float)):
                    formatted_value = f"{value:.1f} {unit}" if unit else f"{value:.1f}"
                else:
                    formatted_value = str(value)
                
                self.stats_labels[display_key].configure(text=formatted_value)
        
        # Update connection status
        self.update_connection_status()
        
        # Clear any previous alerts if data is normal
        if sensor_data.get("status") != "alert":
            self.clear_alert()

    def handle_alert(self, alert_data: Dict):
        """Handle alerts from Arduino controller"""
        self.show_alert(alert_data["message"], alert_data.get("severity", "medium"))

    def show_alert(self, message: str, severity: str = "medium"):
        """Display alert message on dashboard"""
        colors = {
            "low": "#F59E0B",
            "medium": "#EF4444", 
            "high": "#DC2626"
        }
        
        self.alert_label.configure(
            text=f"⚠️ {message}",
            text_color=colors.get(severity, "#EF4444")
        )
        
        # Auto-hide alert after 10 seconds
        self.frame.after(10000, self.clear_alert)

    def clear_alert(self):
        """Clear alert message"""
        self.alert_label.configure(text="")

    def update_connection_status(self):
        """Update connection status indicator"""
        if not self.arduino_controller:
            self.connection_status.configure(text="🔴 No Controller", text_color=COLORS.danger)
            return
        
        if self.arduino_controller.is_connected():
            status_text = f"🟢 Connected ({self.arduino_controller.port})"
            text_color = COLORS.primary
        else:
            status_text = "🟡 Simulated Mode"
            text_color = "#F59E0B"
        
        self.connection_status.configure(text=status_text, text_color=text_color)

    def _create_card(self, parent, title, value, icon, color):
        card = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=8, border_width=1, border_color=COLORS.border)
        
        # Compact card layout
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Icon and text in vertical layout for compact design
        icon_label = ctk.CTkLabel(content_frame, text=icon, font=ctk.CTkFont(size=20), text_color=color)
        icon_label.pack(pady=(0, 5))
        
        value_label = ctk.CTkLabel(
            content_frame, text=value, font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS.text_dark
        )
        value_label.pack()
        
        title_label = ctk.CTkLabel(
            content_frame, text=title, font=ctk.CTkFont(size=11),
            text_color=COLORS.text_light
        )
        title_label.pack()
        
        return card, value_label

    def _resize_image(self, event):
        """Resize image when container size changes"""
        if self.original_image and event.width > 50 and event.height > 50:
            try:
                # Calculate image size maintaining aspect ratio
                available_width = event.width - 20  # Account for padding
                available_height = event.height - 20
                
                # Calculate aspect ratio
                img_width, img_height = self.original_image.size
                aspect_ratio = img_width / img_height
                
                # Calculate new size maintaining aspect ratio
                if available_width / aspect_ratio <= available_height:
                    new_width = available_width
                    new_height = int(available_width / aspect_ratio)
                else:
                    new_height = available_height
                    new_width = int(available_height * aspect_ratio)
                
                # Update CTkImage size
                self.ctk_image = ctk.CTkImage(
                    light_image=self.original_image,
                    dark_image=self.original_image,
                    size=(new_width, new_height)
                )
                self.image_label.configure(image=self.ctk_image)
            except Exception as e:
                print(f"Error resizing image: {e}")

    def get_frame(self):
        """Return the main frame for embedding in other components"""
        return self.frame

    def refresh_data(self):
        """Manually refresh sensor data"""
        if self.arduino_controller:
            sensor_data = self.arduino_controller.read_sensors()
            if sensor_data:
                self.update_sensor_display(sensor_data)

