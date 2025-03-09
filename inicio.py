from customtkinter import *
from navbar import Navbar
from temperatura import TemperaturaFrame
from humedad import HumedadFrame
from ph import PHFrame
from nivel_agua import AguaFrame

app = CTk()
app.geometry("1200x600")  # Tamaño fijo para la pantalla
app.title("SmartGrow - Monitoreo Hidropónico")

# Crear el Navbar
navbar = Navbar(app)
navbar.pack(fill="x", side="top")

# Crear un frame principal para contener las métricas
main_frame = CTkFrame(app, fg_color="#CFF4D2")  # Fondo verde claro
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Crear frames para cada métrica
temperatura_frame = TemperaturaFrame(main_frame)
temperatura_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

humedad_frame = HumedadFrame(main_frame)
humedad_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

ph_frame = PHFrame(main_frame)  # Frame para el pH
ph_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

agua_frame = AguaFrame(main_frame)  # Frame para el nivel de agua
agua_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Configurar el grid para que los frames se expandan adecuadamente
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)

app.mainloop()