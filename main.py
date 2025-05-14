import customtkinter as ctk
from PIL import Image, ImageTk
import os

# Set appearance mode and default color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Simplified color palette
COLORS = {
    "primary": "#3B82F6",
    "secondary": "#10B981",
    "danger": "#EF4444",
    "background": "#F9FAFB",
    "card": "#FFFFFF",
    "text_dark": "#1F2937",
    "text_light": "#6B7280",
    "border": "#E5E7EB",
}

class Sidebar:
    def __init__(self, master):
        self.frame = ctk.CTkFrame(master, fg_color=COLORS["card"], width=220, corner_radius=0)
        self.frame.pack(side="left", fill="y")
        self.frame.pack_propagate(False)
        
        # App logo/title
        logo_frame = ctk.CTkFrame(self.frame, fg_color="transparent", height=60)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            logo_frame, text="🌊 SmartGrow", font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["primary"]
        ).pack(side="left", padx=20)
        
        # Navigation menu
        self.nav_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.nav_frame.pack(fill="x", pady=20)
        
        self.nav_items = [
            {"icon": "🏠", "text": "Dashboard", "view": "home"},
            {"icon": "📊", "text": "Historial", "view": "history"},
            {"icon": "🔔", "text": "Notificaciones", "view": "notifications"},
            {
                "icon": "⚙️", "text": "Configuración", "view": None,  # view=None indica submenú
                "subitems": [
                    {"text": "Interior", "view": "config_inside"},
                    {"text": "Exterior", "view": "config_outside"}
                ]
            }
        ]

        
        self.nav_buttons = []
        self.submenus = {}
        self.toggle_icons = {}

        for item in self.nav_items:
            if "subitems" in item:
                # Contenedor del botón de configuración con icono a la derecha
                parent_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
                parent_frame.pack(fill="x", padx=20)

                parent_btn = self.create_nav_button(item["icon"], item["text"], view=None, padding=0)
                parent_btn.pack(in_=parent_frame, side="left", fill="x", expand=True)

                toggle_icon = ctk.CTkLabel(parent_frame, text="►", text_color=COLORS["text_light"])
                toggle_icon.pack(side="right", padx=5)

                self.submenus[parent_btn] = []
                self.toggle_icons[parent_btn] = toggle_icon

                for sub in item["subitems"]:
                    sub_btn = self.create_nav_button("↳", sub["text"], sub["view"], padding=40)
                    self.submenus[parent_btn].append(sub_btn)
                    self.nav_buttons.append(sub_btn)  # ✅ Submenús también cuentan como opciones seleccionables

                def toggle_submenu(b=parent_btn):
                    expanded = any(btn.winfo_ismapped() for btn in self.submenus[b])
                    for sub_btn in self.submenus[b]:
                        if expanded:
                            sub_btn.pack_forget()
                        else:
                            sub_btn.pack(pady=3, padx=40)
                    self.toggle_icons[b].configure(text="▼" if not expanded else "►")

                parent_btn.configure(command=toggle_submenu)

            else:
                button = self.create_nav_button(item["icon"], item["text"], item["view"])
                button.pack(pady=5, padx=20)
                self.nav_buttons.append(button)


        
        # Set the first button as active
        self.set_active_button(self.nav_buttons[0])
        
        # User profile at bottom
        profile_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        profile_frame.pack(side="bottom", fill="x", pady=20)
        
        # Divider
        divider = ctk.CTkFrame(profile_frame, fg_color=COLORS["border"], height=1)
        divider.pack(fill="x", padx=20, pady=(0, 15))
        
        # User info
        user_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
        user_frame.pack(fill="x", padx=20)
        
        # User avatar
        avatar_frame = ctk.CTkFrame(user_frame, width=36, height=36, fg_color=COLORS["primary"], corner_radius=18)
        avatar_frame.pack(side="left")
        avatar_frame.pack_propagate(False)
        
        ctk.CTkLabel(avatar_frame, text="JD", font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(expand=True)
        
        # User details
        user_details = ctk.CTkFrame(user_frame, fg_color="transparent")
        user_details.pack(side="left", padx=10)
        
        ctk.CTkLabel(
            user_details, text="Juan Díaz", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_dark"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            user_details, text="Administrador", font=ctk.CTkFont(size=12),
            text_color=COLORS["text_light"]
        ).pack(anchor="w")
        
    def create_nav_button(self, icon, text, view, padding=20):
        button = ctk.CTkButton(
            self.nav_frame,
            text=f"{icon}  {text}",
            anchor="w",
            width=180,
            height=40,
            corner_radius=10,
            fg_color="transparent",
            text_color=COLORS["text_light"],
            hover_color="#F3F4F6",
            font=ctk.CTkFont(size=14),
            command=lambda v=view: self.on_nav_click(v) if v else None
        )
        button.pack(pady=5, padx=padding)
        button.view = view
        return button

    
    def set_active_button(self, active_button):
        # Reset all buttons
        for button in self.nav_buttons:
            button.configure(
                fg_color="transparent",
                text_color=COLORS["text_light"]
            )
        
        # Set active button
        active_button.configure(
            fg_color=COLORS["primary"],
            text_color="white"
        )
    
    def on_nav_click(self, view):
        # Find the button for this view
        for button in self.nav_buttons:
            if button.view == view:
                self.set_active_button(button)
                break
        
        # Show the corresponding view in main content
        if hasattr(self, 'main_content'):
            self.main_content.show_view(view)

class MainContent:
    def __init__(self, master):
        # Main container
        self.frame = ctk.CTkFrame(master=master, fg_color=COLORS["background"])
        self.frame.pack(side="left", fill="both", expand=True)

        # Header
        self.header = ctk.CTkFrame(self.frame, fg_color=COLORS["card"], height=60)
        self.header.pack(fill="x", pady=(0, 15))
        self.header.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.header, 
            text="Dashboard", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["text_dark"]
        )
        self.title_label.pack(side="left", padx=20)
        
        # Content container
        self.content_container = ctk.CTkFrame(master=self.frame, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.views = {}
        self.tk_image = None
        self.original_image = None
        
        self._create_views()
        self.show_view("home")
    
    def _create_card(self, parent, title, value, icon, color):
        """Helper to create a stat card"""
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
        
        # Icon with background
        icon_bg = ctk.CTkFrame(card, width=36, height=36, fg_color=color, corner_radius=18)
        icon_bg.pack(side="left", padx=15, pady=15)
        icon_bg.pack_propagate(False)
        
        ctk.CTkLabel(icon_bg, text=icon, font=ctk.CTkFont(size=16), text_color="white").pack(expand=True)
        
        # Text content
        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=15)
        
        ctk.CTkLabel(
            text_frame, text=value, font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_dark"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame, text=title, font=ctk.CTkFont(size=14),
            text_color=COLORS["text_light"]
        ).pack(anchor="w")
        
        return card
    
    def _create_notification_card(self, parent, title, message):
        """Helper to create a notification card"""
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"], corner_radius=10, 
                        border_width=1, border_color=COLORS["border"])
        
        # Header with icon and title
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        # Icon
        icon_bg = ctk.CTkFrame(header, width=36, height=36, fg_color=COLORS["primary"], corner_radius=18)
        icon_bg.pack(side="left")
        icon_bg.pack_propagate(False)
        ctk.CTkLabel(icon_bg, text="🔔", font=ctk.CTkFont(size=16), text_color="white").pack(expand=True)
        
        # Title and message
        text_frame = ctk.CTkFrame(header, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        ctk.CTkLabel(
            text_frame, text=title, font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLORS["text_dark"], anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame, text=message, font=ctk.CTkFont(size=13),
            text_color=COLORS["text_light"], wraplength=400, anchor="w"
        ).pack(anchor="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkButton(
            button_frame, text="✓ Marcar como leído", width=140, height=30, 
            font=ctk.CTkFont(size=13), fg_color=COLORS["secondary"], text_color="white",
            command=lambda c=card: self.marcar_leido(c)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, text="🗑 Eliminar", width=100, height=30, 
            font=ctk.CTkFont(size=13), fg_color=COLORS["danger"], text_color="white",
            command=lambda c=card: c.destroy()
        ).pack(side="right", padx=5)
        
        return card
        
    def _create_views(self):
        # HOME VIEW
        home_frame = ctk.CTkFrame(self.content_container, fg_color=COLORS["card"], corner_radius=15)
        
        # Stats section
        stats_frame = ctk.CTkFrame(home_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        stats_data = [
            {"title": "Temperatura", "value": "22.5°C", "icon": "🌡️", "color": COLORS["primary"]},
            {"title": "pH", "value": "6.2", "icon": "🧪", "color": COLORS["secondary"]},
            {"title": "Conductividad", "value": "1300 µS/cm", "icon": "⚡", "color": "#F59E0B"},
            {"title": "Water Level", "value": "50%", "icon": "🚰", "color": "#F59E0B"}
        ]
        
        # Create stats cards in a row
        for i, stat in enumerate(stats_data):
            card = self._create_card(stats_frame, stat["title"], stat["value"], stat["icon"], stat["color"])
            card.pack(side="left", fill="x", expand=True, padx=5)
        
        # Image container
        image_container = ctk.CTkFrame(home_frame, fg_color="transparent")
        image_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.image_label = ctk.CTkLabel(image_container, text="")
        self.image_label.pack(fill="both", expand=True)
        home_frame.bind("<Configure>", self._resize_image)
        self.views["home"] = home_frame
        
        # Try to load the background image
        image_path = "./Sources/1.png"
        if os.path.exists(image_path):
            self.original_image = Image.open(image_path)
        else:
            self.image_label.configure(text="Imagen no encontrada", text_color=COLORS["danger"])

        # HISTORY VIEW
        history_frame = ctk.CTkFrame(self.content_container, fg_color=COLORS["card"], corner_radius=15)
        
        # Header
        ctk.CTkLabel(
            history_frame, text="📊 Historial", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_dark"]
        ).pack(pady=20)
        
        # Table container
        table_container = ctk.CTkScrollableFrame(
            history_frame, height=450, fg_color=COLORS["background"], corner_radius=10
        )
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Table headers
        headers = ["📅 Día", "⏰ Hora", "🌡 Temp. (°C)", "🧪 pH", "⚡ Conduct. (µS/cm)"]
        header_frame = ctk.CTkFrame(table_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        for i, header in enumerate(headers):
            header_frame.columnconfigure(i, weight=1)
            ctk.CTkLabel(
                header_frame, text=header, font=ctk.CTkFont(size=14, weight="bold"),
                height=35, fg_color="#DBEAFE", corner_radius=8, text_color=COLORS["primary"]
            ).grid(row=0, column=i, padx=4, pady=6, sticky="nsew")
        
        # Table data
        datos = [
            ["Lunes", "08:00", "22.5", "6.2", "1300"],
            ["Lunes", "12:00", "24.1", "6.3", "1400"],
            ["Martes", "08:00", "21.8", "6.1", "1250"],
        ]
        
        for row_idx, row_data in enumerate(datos):
            row_frame = ctk.CTkFrame(table_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            for i, col_data in enumerate(row_data):
                row_frame.columnconfigure(i, weight=1)
                ctk.CTkLabel(
                    row_frame, text=col_data, font=ctk.CTkFont(size=13),
                    height=30, fg_color=COLORS["card"], corner_radius=8,
                    text_color=COLORS["text_light"]
                ).grid(row=0, column=i, padx=4, pady=4, sticky="nsew")
        
        self.views["history"] = history_frame

        # NOTIFICATIONS VIEW
        notif_frame = ctk.CTkFrame(self.content_container, fg_color=COLORS["card"], corner_radius=15)
        
        # Header
        ctk.CTkLabel(
            notif_frame, text="🔔 Notificaciones", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_dark"]
        ).pack(pady=20)
        
        # Notifications container
        scrollable = ctk.CTkScrollableFrame(
            notif_frame, fg_color=COLORS["background"], height=450, corner_radius=10
        )
        scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        notificaciones = [
            {"titulo": "Actualización disponible", "mensaje": "Hay una nueva versión del sistema."},
            {"titulo": "Recordatorio", "mensaje": "No olvides revisar el módulo de configuración."},
            {"titulo": "Alerta", "mensaje": "Se ha detectado un cambio inusual en los datos."}
        ]
        
        for notif in notificaciones:
            card = self._create_notification_card(scrollable, notif["titulo"], notif["mensaje"])
            card.pack(fill="x", pady=10, padx=5)
        
        self.views["notifications"] = notif_frame

        # CONFIG INSIDE VIEW
        config_inside_frame = ctk.CTkFrame(self.content_container, fg_color=COLORS["card"], corner_radius=15)

        # Header
        ctk.CTkLabel(
            config_inside_frame, text="Configuración Interior", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_dark"]
        ).pack(pady=20)

        # Content area
        custom_content = ctk.CTkFrame(config_inside_frame, fg_color=COLORS["background"], corner_radius=10)
        custom_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Ideal temperature (estilo decorativo)
        temp_box = ctk.CTkFrame(custom_content, fg_color="#DBEAFE", corner_radius=8, height=40)
        temp_box.pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(
            temp_box,
            text="🌡️Temperatura Ideal:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6"
        ).pack(side="left", padx=10)

        temp_entry = ctk.CTkEntry(temp_box, width=100)
        temp_entry.pack(side="right", padx=10)

        #ideal PH (estilo decorativo)
        ph_box = ctk.CTkFrame(custom_content, fg_color="#DBEAFE", corner_radius=8, height=40)
        ph_box.pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(
            ph_box,
            text="🧪 pH apropiado:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6"
        ).pack(side="left", padx=10)

        ph_entry = ctk.CTkEntry(ph_box, width=100)
        ph_entry.pack(side="right", padx=10)

        # ⚡ Conductividad ideal
        conduct_frame = ctk.CTkFrame(custom_content, fg_color="#DBEAFE", corner_radius=8, height=40)
        conduct_frame.pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(
            conduct_frame,
            text="⚡ Conductividad ideal (µS/cm):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6"
        ).pack(side="left", padx=10)

        conduct_entry = ctk.CTkEntry(conduct_frame, width=100)
        conduct_entry.pack(side="right", padx=10)

        # LED lights toggle
        led_frame = ctk.CTkFrame(custom_content, fg_color="transparent")
        led_frame.pack(pady=10)
        ctk.CTkLabel(led_frame, text="Luces Led", text_color=COLORS["text_dark"], font=ctk.CTkFont(size=14)).pack(side="left")
        led_switch = ctk.CTkSwitch(led_frame, text="")
        led_switch.pack(side="left", padx=10)

        # Intensity slider
        intensity_frame = ctk.CTkFrame(custom_content, fg_color="transparent")
        intensity_frame.pack(pady=10)
        ctk.CTkLabel(intensity_frame, text="Intensidad", text_color=COLORS["text_dark"], font=ctk.CTkFont(size=14)).pack(side="left")
        intensity_slider = ctk.CTkSlider(intensity_frame, from_=0, to=100, width=150)
        intensity_slider.set(50)
        intensity_slider.pack(side="left", padx=10)

        # Save button
        save_button = ctk.CTkButton(custom_content, text="Guardar", width=80, fg_color=COLORS["primary"], text_color="white")
        save_button.pack(pady=20)

        self.views["config_inside"] = config_inside_frame

        # CONFIG OUTSIDE VIEW
        config_outside_frame = ctk.CTkFrame(self.content_container, fg_color=COLORS["card"], corner_radius=15)

        # Header
        ctk.CTkLabel(
            config_outside_frame, text="Configuración Exterior", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text_dark"]
        ).pack(pady=20)

        # Content area
        custom_content = ctk.CTkFrame(config_outside_frame, fg_color=COLORS["background"], corner_radius=10)
        custom_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Ideal temperature (estilo decorativo)
        temp_box = ctk.CTkFrame(custom_content, fg_color="#DBEAFE", corner_radius=8, height=40)
        temp_box.pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(
            temp_box,
            text="🌡️Temperatura Ideal:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6"
        ).pack(side="left", padx=10)

        temp_entry = ctk.CTkEntry(temp_box, width=100)
        temp_entry.pack(side="right", padx=10)

        #ideal PH (estilo decorativo)
        ph_box = ctk.CTkFrame(custom_content, fg_color="#DBEAFE", corner_radius=8, height=40)
        ph_box.pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(
            ph_box,
            text="🧪 pH apropiado:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6"
        ).pack(side="left", padx=10)

        ph_entry = ctk.CTkEntry(ph_box, width=100)
        ph_entry.pack(side="right", padx=10)

        # ⚡ Conductividad ideal
        conduct_frame = ctk.CTkFrame(custom_content, fg_color="#DBEAFE", corner_radius=8, height=40)
        conduct_frame.pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(
            conduct_frame,
            text="⚡ Conductividad ideal (µS/cm):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6"
        ).pack(side="left", padx=10)

        conduct_entry = ctk.CTkEntry(conduct_frame, width=100)
        conduct_entry.pack(side="right", padx=10)

        # Save button
        save_button = ctk.CTkButton(custom_content, text="Guardar", width=80, fg_color=COLORS["primary"], text_color="white")
        save_button.pack(pady=20)

        self.views["config_outside"] = config_outside_frame

    #def _resize_image(self, event):
        #if self.original_image:
            #resized = self.original_image.resize((event.width, event.height), Image.LANCZOS)
            #self.tk_image = ImageTk.PhotoImage(resized)
            #self.image_label.configure(image=self.tk_image)
    def _resize_image(self, event):
        if self.original_image:
            # Tamaño del contenedor
            container_width = event.width
            container_height = event.height

            # Tamaño original de la imagen
            img_width, img_height = self.original_image.size

            # Calcular proporción adecuada
            ratio = min(container_width / img_width, container_height / img_height)
            new_size = (int(img_width * ratio), int(img_height * ratio))

            resized = self.original_image.resize(new_size, Image.LANCZOS)
            # Tamaño del contenedor
            container_width = event.width
            container_height = event.height

            # Tamaño original de la imagen
            img_width, img_height = self.original_image.size

            # Calcular proporción adecuada
            ratio = min(container_width / img_width, container_height / img_height)
            new_size = (int(img_width * ratio), int(img_height * ratio))

            resized = self.original_image.resize(new_size, Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized)


            self.image_label.configure(image=self.tk_image)



    def show_view(self, view_name):
        # Update header title
        titles = {
            "home": "Dashboard",
            "history": "Historial",
            "notifications": "Notificaciones",
            "custom": "Vista Personalizada"
        }
        self.title_label.configure(text=titles.get(view_name, "Dashboard"))
        
        # Hide all views and show selected view
        for view in self.views.values():
            view.pack_forget()
            
        if view_name in self.views:
            self.views[view_name].pack(fill="both", expand=True)

    def show_custom_view(self, text):
        self.custom_label.configure(text=text)
        self.show_view("custom")

    def marcar_leido(self, card):
        card.configure(fg_color="#F0FDF4")  # Light green background

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("AquaMonitor - Sistema de Monitoreo")
        self.geometry("1100x700")
        self.minsize(900, 600)
        
        # Create sidebar
        self.sidebar = Sidebar(self)
        
        # Create main content
        self.main_content = MainContent(self)
        
        # Connect sidebar to main content
        self.sidebar.main_content = self.main_content

if __name__ == "__main__":
    app = App()
    app.mainloop()