import customtkinter as ctk
from PIL import Image, ImageTk
import os

class SmartGrowApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.app = ctk.CTk()
        self.app.geometry("800x600")
        self.app.title("SmartGrow")
        self.app.configure(fg_color="#FFFFFF")
        
        # PRIMERO Sidebar, LUEGO MainContent
        self.sidebar = Sidebar(self.app, None)  # Temporalmente None
        self.main_content = MainContent(self.app)
        self.sidebar.main_content = self.main_content  # Ahora sí, lo enlazamos correctamente
        
    def run(self):
        self.app.mainloop()

class Sidebar:
    def __init__(self, master, main_content):
        self.main_content = main_content
        self.frame = ctk.CTkFrame(master=master, width=200, corner_radius=0, fg_color="#A6E6CF")
        self.frame.pack(side="left", fill="y")
        self._create_widgets()
    
    def _create_widgets(self):
        title_label = ctk.CTkLabel(master=self.frame, 
                                   text="SmartGrow", 
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color="#3CB371")
        title_label.pack(pady=(20, 10))
        
        ctk.CTkLabel(master=self.frame, text="", height=30).pack(pady=(30, 10))
        
        ctk.CTkButton(master=self.frame, text="Home",
                      fg_color="#4A90E2", hover_color="#3CB371", text_color="#FFFFFF",
                      command=lambda: self.main_content.show_view("home")
                      ).pack(pady=10, padx=20, fill="x")
        
        self.graphics_select = ctk.CTkOptionMenu(
            master=self.frame,
            values=["Ph", "Temperature", "Conductivity", "Water Level"],
            anchor="w",
            fg_color="#4A90E2",
            button_color="#4A90E2",
            button_hover_color="#3CB371",
            text_color="#FFFFFF",
            command=self.graphics_selected
        )
        self.graphics_select.set("Graphics")
        self.graphics_select.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(master=self.frame, text="History",
                      fg_color="#4A90E2", hover_color="#3CB371", text_color="#FFFFFF",
                      command=lambda: self.main_content.show_view("history")
                      ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(master=self.frame, text="Notifications",
                      fg_color="#4A90E2", hover_color="#3CB371", text_color="#FFFFFF",
                      command=lambda: self.main_content.show_view("notifications")
                      ).pack(pady=10, padx=20, fill="x")
        
        self.settings_select = ctk.CTkOptionMenu(
            master=self.frame,
            values=["Inside", "Outside"],
            anchor="w",
            fg_color="#4A90E2",
            button_color="#4A90E2",
            button_hover_color="#3CB371",
            text_color="#FFFFFF",
            command=self.settings_selected
        )
        self.settings_select.set("Settings")
        self.settings_select.pack(pady=10, padx=20, fill="x")

    def graphics_selected(self, selection):
        self.main_content.show_view(selection.lower())

    def settings_selected(self, selection):
        self.main_content.show_view(selection.lower())

class MainContent:
    def __init__(self, master):
        self.frame = ctk.CTkFrame(master=master, fg_color="#FFFFFF")
        self.frame.pack(side="left", fill="both", expand=True)

        self.content_container = ctk.CTkFrame(master=self.frame, fg_color="#FFFFFF")
        self.content_container.pack(fill="both", expand=True)

        self.views = {}
        self.tk_image = None
        self.original_image = None

        self._create_views()
        self.show_view("home")

    def _create_views(self):
        # --- Vista Home ---
        home_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        self.image_label = ctk.CTkLabel(home_frame, text="")
        self.image_label.pack(fill="both", expand=True)
        home_frame.bind("<Configure>", self._resize_image)
        self.views["home"] = home_frame

        image_path = "Sources/fondo_light.png"
        if os.path.exists(image_path):
            self.original_image = Image.open(image_path)
        else:
            self.image_label.configure(text="Imagen no encontrada", text_color="red")

        # --- Vista History ---
        history_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        ctk.CTkLabel(history_frame, text="Historial", font=ctk.CTkFont(size=20)).pack(pady=20)
        self.views["history"] = history_frame

        # --- Vista Notifications ---
        notif_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        ctk.CTkLabel(notif_frame, text="Notificaciones", font=ctk.CTkFont(size=20)).pack(pady=20)
        self.views["notifications"] = notif_frame

        # --- Vistas para gráficos ---
        for graph in ["ph", "temperature", "conductivity", "water level"]:
            graph_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
            ctk.CTkLabel(graph_frame, text=f"Gráfico de {graph.title()}",
                         font=ctk.CTkFont(size=20)).pack(pady=20)
            self.views[graph] = graph_frame

        # --- Vistas para Settings ---
        inside_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        ctk.CTkLabel(inside_frame, text="Configuración Interna",
                     font=ctk.CTkFont(size=20)).pack(pady=20)
        self.views["inside"] = inside_frame

        outside_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        ctk.CTkLabel(outside_frame, text="Configuración Externa",
                     font=ctk.CTkFont(size=20)).pack(pady=20)
        self.views["outside"] = outside_frame

    def _resize_image(self, event):
        if self.original_image:
            resized = self.original_image.resize((event.width, event.height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized)
            self.image_label.configure(image=self.tk_image)

    def show_view(self, view_name):
        for view in self.views.values():
            view.pack_forget()
        if view_name in self.views:
            self.views[view_name].pack(fill="both", expand=True)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = SmartGrowApp()
    app.run()
