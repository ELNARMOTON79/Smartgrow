import customtkinter as ctk
from PIL import Image, ImageTk
import os
from VIEWS.colors import COLORS
from typing import Dict, Optional

# Añadir imports para matplotlib
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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
        
        # Bottom section for chart (expandable)
        chart_section = ctk.CTkFrame(main_container, fg_color="transparent")
        chart_section.pack(fill="both", expand=True)
        
        # Contenedor de gráfica
        self.chart_frame = chart_section
        self._init_chart(chart_section)

        # Si no hay controlador, no cargar datos de simulación
        if self.arduino_controller:
            self.refresh_data()

    def _init_chart(self, parent):
        """Inicializa la gráfica de sensores"""
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.fig.tight_layout()
        self.sensor_history = {
            "Temperature": [],
            "pH": [],
            "Conductivity": [],
            "Water Level": [],
            "x": []
        }
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
        self._update_chart()  # Dibuja la gráfica vacía

    def _update_chart(self):
        """Actualiza la gráfica con los datos actuales"""
        self.ax.clear()
        x = self.sensor_history["x"]
        if len(x) == 0:
            self.ax.set_title("Esperando datos de sensores...")
            self.canvas.draw()
            return
        
        # Variables para calcular los límites dinámicos del eje Y
        all_values = []

        # Graficar cada sensor si hay datos
        for key, label, color, lw in [
            ("Temperature", "Temperatura (°C)", "tab:red", 2),
            ("pH", "pH", "#8B5CF6", 3),  # Morado brillante y línea más gruesa
            ("Conductivity", "Conductividad (mS/cm)", "#F59E0B", 3),  # Amarillo fuerte y línea más gruesa
            ("Water Level", "Nivel Agua (cm)", "tab:cyan", 2),
        ]:
            if len(self.sensor_history[key]) > 0:
                self.ax.plot(x, self.sensor_history[key], label=label, color=color, linewidth=lw, marker='o')
                all_values.extend(self.sensor_history[key])  # Agregar valores para calcular límites

        # Ajustar límites del eje Y dinámicamente
        if all_values:
            min_y = min(all_values) - 1  # Margen inferior
            max_y = max(all_values) + 1  # Margen superior
            self.ax.set_ylim(min_y, max_y)

        self.ax.legend(loc="upper left")
        self.ax.set_xlabel("Tiempo (min)")
        self.ax.set_ylabel("Valor")
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlim(left=max(0, len(x) - 20), right=len(x))  # Avanzar conforme llegan datos
        
        # Cambiar etiqueta del eje X dinámicamente entre segundos y minutos
        if len(x) * 5 < 60:  # Si el rango total es menor a 1 minuto
            self.ax.set_xlabel("Tiempo (s)")
            self.ax.set_xticks([i for i in range(len(x))])  # Ajustar ticks del eje X
            self.ax.set_xticklabels([f"{i * 5}" for i in range(len(x))])  # Mostrar en segundos
        else:  # Si el rango total es mayor o igual a 1 minuto
            self.ax.set_xlabel("Tiempo (min)")
            self.ax.set_xticks([i for i in range(len(x))])  # Ajustar ticks del eje X
            self.ax.set_xticklabels([f"{i * 5 / 60:.1f}" for i in range(len(x))])  # Mostrar en minutos
        
        self.fig.tight_layout()
        self.canvas.draw()

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
                    formatted_value = f"{display_key}: {value:.2f} {unit}" if unit else f"{display_key}: {value:.2f}"
                else:
                    formatted_value = f"{display_key}: {str(value)}"
                
                self.stats_labels[display_key].configure(text=formatted_value)
        
        # Actualizar historial de sensores para la gráfica
        # Se asume que cada llamada es una nueva medición
        self.sensor_history["x"].append(len(self.sensor_history["x"]))
        for key, display_key in [
            ("temperature", "Temperature"),
            ("ph", "pH"),
            ("ec", "Conductivity"),
            ("water_level", "Water Level"),
        ]:
            value = sensor_data.get(key)
            if isinstance(value, (int, float)):
                self.sensor_history[display_key].append(value)
            else:
                self.sensor_history[display_key].append(float("nan"))
        # Limitar historial a 20 puntos
        for k in self.sensor_history:
            self.sensor_history[k] = self.sensor_history[k][-20:]
        self._update_chart()
        
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

    def get_frame(self):
        """Return the main frame for embedding in other components"""
        return self.frame

    def refresh_data(self):
        """Manually refresh sensor data"""
        if self.arduino_controller:
            sensor_data = self.arduino_controller.read_sensors()
            if sensor_data:
                self.update_sensor_display(sensor_data)

