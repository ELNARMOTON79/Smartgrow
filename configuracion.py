from customtkinter import *

class Configuracion(CTkFrame ):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Crear un frame principal para contener las métricas
        self.main_frame = CTkFrame(self, fg_color="#CFF4D2")  # Fondo verde claro
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.title_label = CTkLabel(self.main_frame, text="Settings", font=("Arial", 20, "bold"), text_color="#32909C")
        self.title_label.pack(pady=(10, 5))  # Espaciado superior