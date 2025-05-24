import customtkinter as ctk
from VIEWS.colors import COLORS
from VIEWS.dashboard import Dashboard
from VIEWS.history import History
from VIEWS.notifications import Notifications
from VIEWS.settings import CustomView

class MainContent(ctk.CTkFrame):
    def __init__(self, parent, on_settings_saved=None):
        super().__init__(parent)
        # Main container
        self.frame = ctk.CTkFrame(master=parent, fg_color=COLORS.background)
        self.frame.pack(side="left", fill="both", expand=True)

        # Header
        self.header = ctk.CTkFrame(self.frame, fg_color=COLORS.card, height=60)
        self.header.pack(fill="x", pady=(0, 15))
        self.header.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.header, 
            text="Dashboard", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS.text_dark
        )
        self.title_label.pack(side="left", padx=20)
        
        # Content container
        self.content_container = ctk.CTkFrame(master=self.frame, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Initialize views
        self.custom_view = CustomView(self.content_container, on_settings_saved=on_settings_saved)
        self.dashboard = Dashboard(self.content_container)
        self.history = History(self.content_container)
        self.notifications = Notifications(self.content_container, self.custom_view)

        
        # Store views in dictionary for easy access
        self.views = {
            "home": self.dashboard.frame,
            "history": self.history.frame,
            "notifications": self.notifications.frame,
            "custom": self.custom_view.frame
        }
        
        # Show default view
        self.show_view("home")
    
    def show_view(self, view_name):
        # Update header title
        titles = {
            "home": "Dashboard",
            "history": "",
            "notifications": "",
            "custom": ""
        }
        self.title_label.configure(text=titles.get(view_name, "Dashboard"))
        
        # Hide all views and show selected view
        for view in self.views.values():
            view.pack_forget()
            
        if view_name in self.views:
            self.views[view_name].pack(fill="both", expand=True)

    def show_custom_view(self, text):
        self.custom_view.update_content(text)
        self.show_view("custom")

    def update_sensor_display(self, sensor_data):
        # Forward sensor data to dashboard (and other views if needed)
        if hasattr(self.dashboard, "update_sensor_display"):
            self.dashboard.update_sensor_display(sensor_data)
        # Optionally, update other views if needed

    def show_alert(self, alert_data):
        if hasattr(self, "notifications"):
            self.notifications.handle_alert(alert_data)
        # ...puedes agregar lógica para mostrar en otro lado si lo deseas...