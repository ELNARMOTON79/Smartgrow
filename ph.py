import tkinter as tk
from customtkinter import CTkFrame, CTkLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class PHFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configurar el frame
        self.configure(fg_color="#FFFFFF", border_width=2, border_color="#32909C", height=280, width=580)  # Tamaño ajustado
        self.pack_propagate(False)  # Evitar que el frame cambie de tamaño
        
        # Crear un label para mostrar el valor del pH
        self.ph_label = CTkLabel(self, text="pH: --", font=("Arial", 16), text_color="#000000")
        self.ph_label.pack(pady=10)
        
        # Crear una figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5, 2), facecolor="#F0F0F0")
        self.ax.set_xlabel("Time (s)", color="#000000")
        self.ax.set_ylabel("pH", color="#000000")
        self.ax.tick_params(colors="#000000")
        
        # Crear un canvas para la gráfica
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Inicializar datos de la gráfica
        self.tiempo = list(range(10))
        self.ph_values = [random.uniform(5.5, 7.5) for _ in range(10)]
        
        # Actualizar la gráfica y el valor del pH
        self.actualizar_ph()

    def actualizar_ph(self):
        # Simular un nuevo valor de pH
        nuevo_ph = random.uniform(5.5, 7.5)
        self.ph_values.append(nuevo_ph)
        self.tiempo.append(self.tiempo[-1] + 1)
        
        # Limitar el número de puntos en la gráfica
        if len(self.tiempo) > 20:
            self.tiempo.pop(0)
            self.ph_values.pop(0)
        
        # Actualizar el label con el valor del pH
        self.ph_label.configure(text=f"pH: {nuevo_ph:.2f}")
        
        # Actualizar la gráfica
        self.ax.clear()
        self.ax.bar(self.tiempo, self.ph_values, color='#78E495')
        self.ax.set_xlabel("Time (s)", color="#000000")
        self.ax.set_ylabel("pH", color="#000000")
        self.ax.tick_params(colors="#000000")
        self.canvas.draw()
        
        # Llamar a esta función nuevamente después de 1 segundo
        self.after(10000, self.actualizar_ph)