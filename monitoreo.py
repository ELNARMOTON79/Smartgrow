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

        # Crear frames para cada métrica
        self.temperatura_frame = TemperaturaFrame(self.main_frame)
        self.temperatura_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.humedad_frame = HumedadFrame(self.main_frame)
        self.humedad_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.ph_frame = PHFrame(self.main_frame)  # Frame para el pH
        self.ph_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.agua_frame = AguaFrame(self.main_frame)  # Frame para el nivel de agua
        self.agua_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Configurar el grid para que los frames se expandan adecuadamente
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)