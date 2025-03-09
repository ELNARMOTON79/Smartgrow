from customtkinter import *
from navbar import Navbar  # Importar la clase Navbar de navbar.py
from temperatura import TemperaturaFrame  # Importar la clase TemperaturaFrame de temperatura.py
from humedad import HumedadFrame  # Importar la clase HumedadFrame de humedad.py

app = CTk()
app.geometry("1200x600")  # Tamaño más grande para acomodar 5 gráficas
app.title("SmartGrow")

# Crear el Navbar
navbar = Navbar(app)
navbar.pack(fill="x", side="top")  # Colocar el Navbar en la parte superior

# Crear un frame para contener el canvas
frame = CTkFrame(app)
frame.pack(fill="both", expand=True)

# Crear un frame de temperatura
temperatura_frame = TemperaturaFrame(frame)
temperatura_frame.grid(row=0, column=0, padx=5, pady=5)

# Crear un frame para la humedad
humedad_frame = HumedadFrame(frame)
humedad_frame.grid(row=0, column=1, padx=5, pady=5)

frame.grid_columnconfigure(0, weight=0)  # No expandir la columna
frame.grid_rowconfigure(0, weight=0)  # No expandir la fila

app.mainloop()