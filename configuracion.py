from customtkinter import *

class Configuracion(CTkFrame ):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Crear un frame principal para contener las métricas
        self.main_frame = CTkFrame(self, fg_color="#CFF4D2")  # Fondo verde claro
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)