from customtkinter import *
import tkinter as tk

class Navbar(CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color="#32909C")  # Fondo verde azulado
        self.master = master
        self.pack(fill="x")

        self.create_widgets()

    def create_widgets(self):
        # Cargar imágenes de los iconos
        self.home_icon = tk.PhotoImage(file="Sources/home.png").subsample(18, 18)
        self.history_icon = tk.PhotoImage(file="Sources/history.png").subsample(18, 18)
        self.settings_icon = tk.PhotoImage(file="Sources/setting.png").subsample(18, 18)

        # Botón Home
        self.home = CTkButton(
            self,
            text="Home",
            command=self.home,
            fg_color="#56C596",  # Verde claro
            hover_color="#32909C",  # Verde azulado al pasar el mouse
            font=("Arial", 14, "bold"),
            image=self.home_icon,  # Icono para Home
            compound="left"  # Colocar el icono a la izquierda del texto
        )
        self.home.pack(side="left", padx=10, pady=10)

        # Botón History
        self.about = CTkButton(
            self,
            text="History",
            command=self.about,
            fg_color="#56C596",
            hover_color="#32909C",
            font=("Arial", 14, "bold"),
            image=self.history_icon,  # Icono para History
            compound="left"
        )
        self.about.pack(side="left", padx=10, pady=10)

        # Botón Settings
        self.contact = CTkButton(
            self,
            text="Settings",
            command=self.contact,
            fg_color="#56C596",
            hover_color="#32909C",
            font=("Arial", 14, "bold"),
            image=self.settings_icon,  # Icono para Settings
            compound="left"
        )
        self.contact.pack(side="left", padx=10, pady=10)

        # Espacio flexible para empujar la imagen hacia la derecha
        self.spacer = CTkLabel(self, text="", width=1)
        self.spacer.pack(side="left", fill="x", expand=True)

        # Cargar la imagen del logo
        self.logo_image = tk.PhotoImage(file="Sources/logo.png")
        self.logo_image = self.logo_image.subsample(2, 2)  # Reducir el tamaño a la mitad

        # Mostrar la imagen en un CTkLabel
        self.logo_label = CTkLabel(self, image=self.logo_image, text="")
        self.logo_label.pack(side="right", padx=10, pady=10)

    def home(self):
        print("Home")

    def about(self):
        print("About")

    def contact(self):
        print("Contact")