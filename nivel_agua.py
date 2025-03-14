import tkinter as tk
from customtkinter import CTkFrame, CTkLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class AguaFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configurar el frame
        self.configure(fg_color="#FFFFFF", border_width=2, border_color="#32909C", height=280, width=580)  # Tamaño ajustado
        self.pack_propagate(False)  # Evitar que el frame cambie de tamaño
        
        # Crear un label para mostrar el valor del nivel de agua
        self.agua_label = CTkLabel(self, text="Water Level: --%", font=("Arial", 16), text_color="#000000")
        self.agua_label.pack(pady=10)
        
        # Crear una figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5, 2), facecolor="#F0F0F0")
        self.ax.set_xlabel("Time (s)", color="#000000")
        self.ax.set_ylabel("Water Level (%)", color="#000000")
        self.ax.tick_params(colors="#000000")
        
        # Crear un canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Inicializar datos de la gráfica
        self.tiempo = list(range(10))
        self.agua_values = [random.randint(50, 100) for _ in range(10)]
        
        # Actualizar la gráfica y el valor del nivel de agua
        self.actualizar_agua()

    def actualizar_agua(self):
        # Simular un nuevo valor de nivel de agua
        nuevo_agua = random.randint(50, 100)
        self.agua_values.append(nuevo_agua)
        self.tiempo.append(self.tiempo[-1] + 1)
        
        # Limitar el número de puntos en la gráfica
        if len(self.tiempo) > 20:
            self.tiempo.pop(0)
            self.agua_values.pop(0)
        
        # Actualizar el label con el valor del nivel de agua
        self.agua_label.configure(text=f"Water Level: {nuevo_agua}%")
        
        # Actualizar la gráfica
        self.ax.clear()
        self.ax.bar(self.tiempo, self.agua_values, color='#32909C')  # Verde azulado
        self.ax.set_xlabel("Time (s)", color="#000000")
        self.ax.set_ylabel("Water Level (%)", color="#000000")
        self.ax.tick_params(colors="#000000")
        self.canvas.draw()
        
        # Llamar a esta función nuevamente después de 1 segundo
        self.after(10000, self.actualizar_agua)