import tkinter as tk
from customtkinter import CTkFrame, CTkLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class TemperaturaFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configurar el frame
        self.configure(fg_color="gray", border_width=0, height=300, width=400)
        
        # Crear un label para mostrar el valor de la temperatura
        self.temperatura_label = CTkLabel(self, text="Temperatura: --°C", font=("Arial", 16))
        self.temperatura_label.pack(pady=10)
        
        # Crear una figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(4, 2))
        self.ax.set_title("Temperatura en el tiempo")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Temperatura (°C)")
        
        # Crear un canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Inicializar datos de la gráfica
        self.tiempo = list(range(10))
        self.temperaturas = [random.randint(20, 30) for _ in range(10)]
        
        # Actualizar la gráfica y el valor de la temperatura
        self.actualizar_temperatura()

    def actualizar_temperatura(self):
        # Simular un nuevo valor de temperatura
        nueva_temperatura = random.randint(20, 30)
        self.temperaturas.append(nueva_temperatura)
        self.tiempo.append(self.tiempo[-1] + 1)
        
        # Limitar el número de puntos en la gráfica
        if len(self.tiempo) > 20:
            self.tiempo.pop(0)
            self.temperaturas.pop(0)
        
        # Actualizar el label con el valor de la temperatura
        self.temperatura_label.configure(text=f"Temperatura: {nueva_temperatura}°C")
        
        # Actualizar la gráfica
        self.ax.clear()
        self.ax.bar(self.tiempo, self.temperaturas, color='blue')  # Cambiar a gráfica de barras
        self.ax.set_title("Temperatura en el tiempo")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Temperatura (°C)")
        self.canvas.draw()
        
        # Llamar a esta función nuevamente después de 1 segundo
        self.after(10000, self.actualizar_temperatura)
