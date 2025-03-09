from customtkinter import *
import tkinter as tk  # Importar tkinter para usar PhotoImage

class Navbar(CTkFrame):  # Usar CTkFrame en lugar de Frame de tkinter

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="x")

        self.create_widgets()

    def create_widgets(self):
        # Botón Home
        self.home = CTkButton(
            self, 
            text="Home", 
            command=self.home, 
            fg_color="#228B22",
            hover_color="#32CD32"
        )
        self.home.pack(side="left", padx=10, pady=10)

        # Botón History
        self.about = CTkButton(
            self, 
            text="History", 
            command=self.about, 
            fg_color="#228B22",
            hover_color="#32CD32"
        )
        self.about.pack(side="left", padx=10, pady=10)

        # Botón Settings
        self.contact = CTkButton(
            self, 
            text="Settings", 
            command=self.contact, 
            fg_color="#228B22",  
            hover_color="#32CD32"  
        )
        self.contact.pack(side="left", padx=10, pady=10)

        # Espacio flexible para empujar la imagen hacia la derecha
        self.spacer = CTkLabel(self, text="", width=1)
        self.spacer.pack(side="left", fill="x", expand=True)

        # Cargar la imagen .png o .gif usando tkinter.PhotoImage
        self.logo_image = tk.PhotoImage(file="Sources/logo.png")
        self.logo_image = self.logo_image.subsample(2, 2)

        # Mostrar la imagen en un CTkLabel
        self.logo_label = CTkLabel(self, image=self.logo_image, text="")
        self.logo_label.pack(side="right", padx=10, pady=10)