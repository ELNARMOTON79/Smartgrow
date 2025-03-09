import tkinter as tk
from customtkinter import CTkFrame, CTkLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class HumedadFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configurar el frame
        self.configure(fg_color="gray", border_width=0, height=300, width=400)
        
        # Crear un label para mostrar el valor de la humedad
        self.humedad_label = CTkLabel(self, text="Humedad: --%", font=("Arial", 16))
        self.humedad_label.pack(pady=10)
        
        # Crear una figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(4, 2))
        self.ax.set_title("Humedad en el tiempo")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Humedad (%)")
        
        # Crear un canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Inicializar datos de la gráfica
        self.tiempo = list(range(10))
        self.humedades = [random.randint(40, 80) for _ in range(10)]
        
        # Actualizar la gráfica y el valor de la humedad
        self.actualizar_humedad()

    def actualizar_humedad(self):
        # Simular un nuevo valor de humedad
        nueva_humedad = random.randint(40, 80)
        self.humedades.append(nueva_humedad)
        self.tiempo.append(self.tiempo[-1] + 1)
        
        # Limitar el número de puntos en la gráfica
        if len(self.tiempo) > 20:
            self.tiempo.pop(0)
            self.humedades.pop(0)
        
        # Actualizar el label con el valor de la humedad
        self.humedad_label.configure(text=f"Humedad: {nueva_humedad}%")
        
        # Actualizar la gráfica
        self.ax.clear()
        self.ax.bar(self.tiempo, self.humedades, color='green')
        self.ax.set_title("Humedad en el tiempo")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Humedad (%)")
        self.canvas.draw()
        
        self.after(10000, self.actualizar_humedad)