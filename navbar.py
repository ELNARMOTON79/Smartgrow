from customtkinter import *
import tkinter as tk
import os
from PIL import Image
from customtkinter import CTkImage
from theme_manager import ThemeManager

class Navbar(CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        ThemeManager.subscribe(self)
        self.master = master
        self.pack(fill="x")

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Espacio flexible (empuja elementos a la derecha)
        self.spacer = CTkLabel(self, text="", width=1)
        self.spacer.pack(side="left", fill="x", expand=True)

        # Botón para cambiar tema
        self.theme_button = CTkButton(
            self,
            text="🌗 Tema",
            command=ThemeManager.toggle_theme,
            font=("Arial", 14)
        )
        self.theme_button.pack(side="right", padx=10)

        # Logo
        logo_path = os.path.join(base_dir, "Sources", "logo.png")
        if os.path.exists(logo_path):
            self.logo_image = CTkImage(Image.open(logo_path), size=(50, 50))
            self.logo_label = CTkLabel(self, image=self.logo_image, text="")
            self.logo_label.pack(side="right", padx=10, pady=10)

    def apply_theme(self):
        self.configure(fg_color=ThemeManager.get_color("navbar_bg"))
        self.theme_button.configure(
            fg_color=ThemeManager.get_color("accent"),
            hover_color=ThemeManager.get_color("navbar_bg"),
            text_color=ThemeManager.get_color("text_color")
        )
