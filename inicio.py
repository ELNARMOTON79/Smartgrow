from customtkinter import *
from theme_manager import ThemeManager
import tkinter as tk
import os
from navbar import Navbar
from PIL import Image
from customtkinter import CTkImage

# Establecer modo por defecto
set_appearance_mode("light")

# Crear ventana principal
app = CTk()
app.geometry("1200x600")
app.title("SmartGrow - Hydroponic System")

# Cargar ícono de la app
base_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(base_dir, "Sources", "logo.png")
if os.path.exists(icon_path):
    app.iconphoto(True, tk.PhotoImage(file=icon_path))

# Navbar
navbar = Navbar(app)
navbar.pack(fill="x", side="top")

# Frame principal con soporte de tema, texto bonito e imagen
class MainFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ThemeManager.subscribe(self)
        self.pack(fill="both", expand=True)

        # Texto bonito
        self.bienvenida_label = CTkLabel(
            self,
            text="Hello, welcome to your hydroponic system!",
            font=("Arial", 32, "bold"),
            text_color=ThemeManager.get_color("text_color")
        )
        self.bienvenida_label.pack(pady=40)

        # Imagen
        image_path = os.path.join(base_dir, "Sources", "inicio.jpg")
        if os.path.exists(image_path):
            self.imagen = CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(200, 200)
            )
            self.imagen_label = CTkLabel(self, image=self.imagen, text="")
            self.imagen_label.pack(pady=20)
            
            self.final_label = CTkLabel(
            self,
            text="No land, no limits. Only growth.",
            font=("Arial", 32, "bold"),
            text_color=ThemeManager.get_color("text_color")
        )
        self.final_label.pack(pady=40)

        self.apply_theme()

    def apply_theme(self):
        self.configure(fg_color=ThemeManager.get_color("bg_color"))
        self.bienvenida_label.configure(text_color=ThemeManager.get_color("text_color"))
        self.final_label.configure(text_color=ThemeManager.get_color("text_color")) 

main_frame = MainFrame(app)

# Ejecutar app
app.mainloop()
