from customtkinter import *
import tkinter as tk  # Importar tkinter para usar Canvas
from PIL import Image, ImageTk  # Importar Image y ImageTk de PIL para mostrar imágenes

app = CTk()
app.geometry("800x500")
app.title("SmartGrow")


# Crear un Canvas de tkinter
canvas = tk.Canvas(app, width=200, height=100, bg="white")
canvas.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()
