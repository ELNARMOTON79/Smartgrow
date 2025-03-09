from customtkinter import *

class Configuracion(CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        label = CTkLabel(self, text="Configuración", font=("Arial", 24))
        label.pack(pady=20)