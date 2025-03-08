from customtkinter import *
from navbar import Navbar  # Importar la clase Navbar de navbar.py

app = CTk()
app.geometry("1200x600")  # Tamaño más grande para acomodar 5 gráficas
app.title("SmartGrow")

# Crear el Navbar
navbar = Navbar(app)
navbar.pack(fill="x", side="top")  # Colocar el Navbar en la parte superior

# Crear un frame para contener el canvas
frame = CTkFrame(app)
frame.pack(fill="both", expand=True)

# Crear un "canvas" usando CTkFrame
canvas1 = CTkFrame(frame, fg_color="gray", border_width=0, height=300, width=200)
canvas1.grid(row=0, column=0, padx=5, pady=5)


frame.grid_columnconfigure(0, weight=0)  # No expandir la columna
frame.grid_rowconfigure(0, weight=0)  # No expandir la fila

app.mainloop()