import customtkinter as ctk
from VIEWS.colors import COLORS
import json
import os
from typing import Dict

class Configuration:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.background, corner_radius=15)
        self.arduino_controller = None
        self.notifications_view = None  # Reference to notifications view
        self.config_file = "sensor_config.json"
        
        # Title
        title_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            title_frame, text="⚙️ Configuración del Sistema",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(anchor="w")
        
        # Create main content
        main_content = ctk.CTkScrollableFrame(self.frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Sensor thresholds section
        self.create_sensor_thresholds_section(main_content)
        
        # System settings section
        self.create_system_settings_section(main_content)
        
        # Control buttons
        self.create_control_buttons(main_content)
        
        # Load saved configuration
        self.load_configuration()

    def create_sensor_thresholds_section(self, parent):
        """Create sensor thresholds configuration section"""
        thresholds_frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=10)
        thresholds_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            thresholds_frame, text="📊 Rangos Ideales de Sensores",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        # Sensor configurations
        self.sensor_entries = {}
        sensors_config = [
            {
                "key": "temperature",
                "name": "🌡️ Temperatura (°C)",
                "default_min": 18,
                "default_max": 30,
                "description": "Rango ideal para crecimiento de plantas"
            },
            {
                "key": "ph",
                "name": "🧪 pH",
                "default_min": 5.5,
                "default_max": 7.5,
                "description": "Acidez ideal para absorción de nutrientes"
            },
            {
                "key": "ec",
                "name": "⚡ Conductividad (mS/cm)",
                "default_min": 1.2,
                "default_max": 2.5,
                "description": "Concentración de nutrientes en solución"
            },
            {
                "key": "water_level",
                "name": "🚰 Nivel de Agua (%)",
                "default_min": 20,
                "default_max": 100,
                "description": "Nivel mínimo de agua en el tanque"
            },
            {
                "key": "humidity",
                "name": "💧 Humedad (%)",
                "default_min": 40,
                "default_max": 80,
                "description": "Humedad relativa del ambiente"
            }
        ]
        
        for sensor in sensors_config:
            self.create_sensor_config_widget(thresholds_frame, sensor)

    def create_sensor_config_widget(self, parent, sensor_config):
        """Create configuration widget for a sensor"""
        sensor_frame = ctk.CTkFrame(parent, fg_color=COLORS.background, corner_radius=8)
        sensor_frame.pack(fill="x", padx=20, pady=10)
        
        # Sensor name and description
        info_frame = ctk.CTkFrame(sensor_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(
            info_frame, text=sensor_config["name"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame, text=sensor_config["description"],
            font=ctk.CTkFont(size=12),
            text_color=COLORS.text_light
        ).pack(anchor="w")
        
        # Min/Max entries
        values_frame = ctk.CTkFrame(sensor_frame, fg_color="transparent")
        values_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Minimum value
        min_frame = ctk.CTkFrame(values_frame, fg_color="transparent")
        min_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(min_frame, text="Mínimo:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        min_entry = ctk.CTkEntry(min_frame, width=100, height=32)
        min_entry.pack(anchor="w", pady=(2, 0))
        min_entry.insert(0, str(sensor_config["default_min"]))
        
        # Maximum value
        max_frame = ctk.CTkFrame(values_frame, fg_color="transparent")
        max_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(max_frame, text="Máximo:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        max_entry = ctk.CTkEntry(max_frame, width=100, height=32)
        max_entry.pack(anchor="w", pady=(2, 0))
        max_entry.insert(0, str(sensor_config["default_max"]))
        
        # Store references
        self.sensor_entries[sensor_config["key"]] = {
            "min": min_entry,
            "max": max_entry
        }

    def create_system_settings_section(self, parent):
        """Create system settings section"""
        settings_frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=10)
        settings_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            settings_frame, text="🔧 Configuraciones del Sistema",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        # Alert settings
        alert_frame = ctk.CTkFrame(settings_frame, fg_color=COLORS.background, corner_radius=8)
        alert_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            alert_frame, text="🔔 Configuración de Alertas",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Alert frequency
        freq_frame = ctk.CTkFrame(alert_frame, fg_color="transparent")
        freq_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(freq_frame, text="Frecuencia de alertas (segundos):", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.alert_frequency = ctk.CTkEntry(freq_frame, width=100, height=32)
        self.alert_frequency.pack(anchor="w", pady=(2, 0))
        self.alert_frequency.insert(0, "30")
        
        # Data update rate
        update_frame = ctk.CTkFrame(settings_frame, fg_color=COLORS.background, corner_radius=8)
        update_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            update_frame, text="📊 Frecuencia de Actualización",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        rate_frame = ctk.CTkFrame(update_frame, fg_color="transparent")
        rate_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(rate_frame, text="Actualización de datos (segundos):", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.update_rate = ctk.CTkEntry(rate_frame, width=100, height=32)
        self.update_rate.pack(anchor="w", pady=(2, 0))
        self.update_rate.insert(0, "2")

    def create_control_buttons(self, parent):
        """Create control buttons"""
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)
        
        # Save button
        save_btn = ctk.CTkButton(
            buttons_frame, text="💾 Guardar Configuración",
            command=self.save_configuration,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        # Reset button
        reset_btn = ctk.CTkButton(
            buttons_frame, text="🔄 Restaurar Valores",
            command=self.reset_to_defaults,
            font=ctk.CTkFont(size=14),
            fg_color="#6B7280",
            hover_color="#4B5563",
            height=40
        )
        reset_btn.pack(side="left", padx=10)
        
        # Test alerts button
        test_btn = ctk.CTkButton(
            buttons_frame, text="🧪 Probar Alertas",
            command=self.test_alerts,
            font=ctk.CTkFont(size=14),
            fg_color="#F59E0B",
            hover_color="#D97706",
            height=40
        )
        test_btn.pack(side="right")

    def set_arduino_controller(self, controller):
        """Set the Arduino controller"""
        self.arduino_controller = controller

    def set_notifications_view(self, notifications_view):
        """Set reference to notifications view for updates"""
        self.notifications_view = notifications_view

    def save_configuration(self):
        """Save current configuration to file and update Arduino controller"""
        try:
            config = {
                "sensor_thresholds": {},
                "system_settings": {
                    "alert_frequency": float(self.alert_frequency.get()),
                    "update_rate": float(self.update_rate.get())
                }
            }
            
            # Get sensor thresholds with validation
            for sensor_key, entries in self.sensor_entries.items():
                try:
                    min_val = float(entries["min"].get())
                    max_val = float(entries["max"].get())
                    
                    # Validate min < max
                    if min_val >= max_val:
                        raise ValueError(f"El valor mínimo debe ser menor que el máximo para {sensor_key}")
                    
                    config["sensor_thresholds"][sensor_key] = {
                        "min": min_val,
                        "max": max_val
                    }
                except ValueError as e:
                    self.show_message(f"❌ Error en {sensor_key}: {str(e)}", COLORS.danger)
                    return
            
            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Update Arduino controller
            if self.arduino_controller:
                self.arduino_controller.update_thresholds(config["sensor_thresholds"])
                print(f"Updated thresholds in Arduino controller: {config['sensor_thresholds']}")
                
                # Send ideal ranges for pH and EC to Arduino
                ph_range = config["sensor_thresholds"].get("ph", {})
                ec_range = config["sensor_thresholds"].get("ec", {})
                self.arduino_controller.send_ideal_ranges(ph_range, ec_range)
            
            # Update notifications view to refresh with new thresholds
            if self.notifications_view:
                self.notifications_view.refresh_thresholds()
            
            # Show success message
            self.show_message("✅ Configuración guardada exitosamente", COLORS.primary)
            
        except Exception as e:
            self.show_message(f"❌ Error al guardar: {str(e)}", COLORS.danger)

    def load_configuration(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                # Load sensor thresholds
                for sensor_key, thresholds in config.get("sensor_thresholds", {}).items():
                    if sensor_key in self.sensor_entries:
                        self.sensor_entries[sensor_key]["min"].delete(0, "end")
                        self.sensor_entries[sensor_key]["min"].insert(0, str(thresholds["min"]))
                        self.sensor_entries[sensor_key]["max"].delete(0, "end")
                        self.sensor_entries[sensor_key]["max"].insert(0, str(thresholds["max"]))
                
                # Load system settings
                settings = config.get("system_settings", {})
                if "alert_frequency" in settings:
                    self.alert_frequency.delete(0, "end")
                    self.alert_frequency.insert(0, str(settings["alert_frequency"]))
                if "update_rate" in settings:
                    self.update_rate.delete(0, "end")
                    self.update_rate.insert(0, str(settings["update_rate"]))
                
        except Exception as e:
            print(f"Error loading configuration: {e}")

    def reset_to_defaults(self):
        """Reset all values to defaults"""
        defaults = {
            "temperature": {"min": 18, "max": 30},
            "ph": {"min": 5.5, "max": 7.5},
            "ec": {"min": 1.2, "max": 2.5},
            "water_level": {"min": 20, "max": 100},
            "humidity": {"min": 40, "max": 80}
        }
        
        for sensor_key, values in defaults.items():
            if sensor_key in self.sensor_entries:
                self.sensor_entries[sensor_key]["min"].delete(0, "end")
                self.sensor_entries[sensor_key]["min"].insert(0, str(values["min"]))
                self.sensor_entries[sensor_key]["max"].delete(0, "end")
                self.sensor_entries[sensor_key]["max"].insert(0, str(values["max"]))
        
        self.alert_frequency.delete(0, "end")
        self.alert_frequency.insert(0, "30")
        self.update_rate.delete(0, "end")
        self.update_rate.insert(0, "2")
        
        # Auto-save the defaults
        self.save_configuration()
        
        self.show_message("🔄 Valores restaurados a configuración por defecto", "#F59E0B")

    def test_alerts(self):
        """Test alert system"""
        if self.arduino_controller:
            # Trigger a test alert
            test_alert = {
                "sensor": "test",
                "value": 99.9,
                "type": "test",
                "message": "🧪 Prueba del sistema de alertas - Todo funciona correctamente",
                "timestamp": "TEST",
                "severity": "medium"
            }
            
            # Trigger alert through Arduino controller
            for callback in self.arduino_controller.alert_callbacks:
                callback(test_alert)
            
            self.show_message("🧪 Alerta de prueba enviada", "#F59E0B")
        else:
            self.show_message("❌ No hay controlador Arduino disponible", COLORS.danger)

    def show_message(self, message: str, color: str):
        """Show a modal dialog with the message"""
        modal = ctk.CTkToplevel(self.frame)
        modal.title("Mensaje")
        modal.geometry("400x150")
        modal.resizable(False, False)
        modal.grab_set()  # Modal

        # Center modal relative to parent
        modal.update_idletasks()
        x = self.frame.winfo_rootx() + (self.frame.winfo_width() // 2) - (modal.winfo_width() // 2)
        y = self.frame.winfo_rooty() + (self.frame.winfo_height() // 2) - (modal.winfo_height() // 2)
        modal.geometry(f"+{x}+{y}")

        # Content frame
        content = ctk.CTkFrame(modal, fg_color=COLORS.background, corner_radius=10)
        content.pack(fill="both", expand=True, padx=10, pady=10)

        # Icon and message
        row = ctk.CTkFrame(content, fg_color="transparent")
        row.pack(fill="x", pady=(10, 0), padx=10)

        # Info icon (blue circle with "i")
        icon = ctk.CTkLabel(
            row, text="🛈",  # Unicode info icon, or use "ℹ️"
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#2563eb"  # blue-600
        )
        icon.pack(side="left", padx=(0, 15))

        msg = ctk.CTkLabel(
            row, text=message,
            font=ctk.CTkFont(size=14),
            text_color=color,
            wraplength=260,
            justify="left"
        )
        msg.pack(side="left", fill="x", expand=True)

        # Close button
        btn = ctk.CTkButton(
            content, text="Cerrar",
            command=modal.destroy,
            width=120,
            height=36
        )
        btn.pack(side="bottom", pady=(15, 10))

        btn.focus_set()
        modal.transient(self.frame)
        modal.wait_window()

    def get_frame(self):
        """Return the main frame"""
        return self.frame
