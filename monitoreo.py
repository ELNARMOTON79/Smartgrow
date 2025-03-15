from customtkinter import *
from temperatura import TemperaturaFrame
from humedad import HumedadFrame
from ph import PHFrame
from nivel_agua import AguaFrame

class monitoreo(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Crear un frame principal para contener las métricas
        self.main_frame = CTkFrame(self, fg_color="#CFF4D2")  # Fondo verde claro
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título "Home" con color que combina con la paleta
        self.title_label = CTkLabel(self.main_frame, text="Home", font=("Arial", 20, "bold"), text_color="#32909C")
        self.title_label.pack(pady=(10, 5))  # Espaciado superior

        # Crear un frame contenedor para las métricas
        self.metrics_frame = CTkFrame(self.main_frame, fg_color="transparent")  
        self.metrics_frame.pack(expand=True, fill="both")

        self.temperatura_frame = TemperaturaFrame(self.metrics_frame)
        self.temperatura_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.humedad_frame = HumedadFrame(self.metrics_frame)
        self.humedad_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.ph_frame = PHFrame(self.metrics_frame)  # Frame para el pH
        self.ph_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.agua_frame = AguaFrame(self.metrics_frame)  # Frame para el nivel de agua
        self.agua_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Configurar el grid para que los frames se expandan adecuadamente
        self.metrics_frame.grid_columnconfigure(0, weight=1)
        self.metrics_frame.grid_columnconfigure(1, weight=1)
        self.metrics_frame.grid_rowconfigure(0, weight=1)
        self.metrics_frame.grid_rowconfigure(1, weight=1)