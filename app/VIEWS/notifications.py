import customtkinter as ctk
from VIEWS.colors import COLORS
from typing import Dict, List
from datetime import datetime

class Notifications:
    def __init__(self, parent, custom_view=None):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.background, corner_radius=15)
        self.arduino_controller = None
        self.alerts_history = []
        self.custom_view = custom_view  # Store reference if needed
        
        # Title
        title_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            title_frame, text="🔔 Notificaciones y Alertas",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(anchor="w")
        
        # Current alerts section
        current_frame = ctk.CTkFrame(self.frame, fg_color=COLORS.card, corner_radius=10)
        current_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            current_frame, text="⚡ Alertas Activas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.current_alert_label = ctk.CTkLabel(
            current_frame, text="✅ Sin alertas activas",
            font=ctk.CTkFont(size=14),
            text_color=COLORS.primary
        )
        self.current_alert_label.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Alert history
        history_frame = ctk.CTkFrame(self.frame, fg_color=COLORS.card, corner_radius=10)
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        header_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(
            header_frame, text="📝 Historial de Alertas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(side="left")
        
        clear_btn = ctk.CTkButton(
            header_frame, text="🗑️ Limpiar",
            command=self.clear_history,
            width=100, height=30,
            font=ctk.CTkFont(size=12)
        )
        clear_btn.pack(side="right")
        
        # Scrollable alert history
        self.history_scroll = ctk.CTkScrollableFrame(
            history_frame, fg_color="transparent",
            height=300
        )
        self.history_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Initial message
        self.empty_history_label = ctk.CTkLabel(
            self.history_scroll, text="📭 No hay alertas en el historial",
            font=ctk.CTkFont(size=14),
            text_color=COLORS.text_light
        )
        self.empty_history_label.pack(pady=20)

    def set_arduino_controller(self, controller):
        """Set the Arduino controller"""
        self.arduino_controller = controller
        if controller and hasattr(controller, 'add_alert_callback'):
            try:
                controller.add_alert_callback(self.handle_alert)
            except Exception as e:
                print(f"Error setting alert callback: {e}")

    def handle_alert(self, alert_data: Dict):
        """Handle new alert from Arduino controller"""
        # Add to history
        self.alerts_history.insert(0, alert_data)
        
        # Keep only last 50 alerts
        if len(self.alerts_history) > 50:
            self.alerts_history = self.alerts_history[:50]
        
        # Update current alert display using after() for thread safety
        self.frame.after(0, lambda: self.update_current_alert(alert_data))
        
        # Update history display using after() for thread safety
        self.frame.after(0, self.update_history_display)

    def update_current_alert(self, alert_data: Dict):
        """Update current alert display"""
        severity_colors = {
            "low": "#F59E0B",
            "medium": "#EF4444",
            "high": "#DC2626"
        }
        
        severity_icons = {
            "low": "⚠️",
            "medium": "🚨",
            "high": "🔴"
        }
        
        severity = alert_data.get("severity", "medium")
        icon = severity_icons.get(severity, "⚠️")
        color = severity_colors.get(severity, "#EF4444")
        
        self.current_alert_label.configure(
            text=f"{icon} {alert_data['message']}",
            text_color=color
        )
        
        # Clear alert after 15 seconds
        self.frame.after(15000, self.clear_current_alert)

    def clear_current_alert(self):
        """Clear current alert display"""
        self.current_alert_label.configure(
            text="✅ Sin alertas activas",
            text_color=COLORS.primary
        )

    def update_history_display(self):
        """Update alert history display"""
        # Clear existing widgets
        for widget in self.history_scroll.winfo_children():
            widget.destroy()
        
        if not self.alerts_history:
            self.empty_history_label = ctk.CTkLabel(
                self.history_scroll, text="📭 No hay alertas en el historial",
                font=ctk.CTkFont(size=14),
                text_color=COLORS.text_light
            )
            self.empty_history_label.pack(pady=20)
            return
        
        # Display alerts
        for alert in self.alerts_history:
            self.create_alert_item(alert)

    def create_alert_item(self, alert_data: Dict):
        """Create alert item widget"""
        item_frame = ctk.CTkFrame(self.history_scroll, fg_color=COLORS.background, corner_radius=8)
        item_frame.pack(fill="x", padx=5, pady=2)
        
        # Severity color
        severity_colors = {
            "low": "#F59E0B",
            "medium": "#EF4444",
            "high": "#DC2626"
        }
        
        color = severity_colors.get(alert_data.get("severity", "medium"), "#EF4444")
        
        # Alert info with more detail
        sensor_name = alert_data.get("sensor", "").title()
        value = alert_data.get("value", "")
        alert_type = alert_data.get("type", "")
        
        if sensor_name and value:
            info_text = f"⏰ {alert_data['timestamp']} - {sensor_name}: {value} ({alert_type})"
        else:
            info_text = f"⏰ {alert_data['timestamp']} - {alert_data['message']}"
        
        ctk.CTkLabel(
            item_frame, text=info_text,
            font=ctk.CTkFont(size=12),
            text_color=color,
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)

    def clear_history(self):
        """Clear alert history"""
        self.alerts_history.clear()
        self.update_history_display()

    def get_frame(self):
        """Return the main frame"""
        return self.frame