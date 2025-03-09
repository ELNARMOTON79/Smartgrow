from customtkinter import *
from navbar import Navbar
from monitoreo import monitoreo
from historial import historial
from configuracion import Configuracion

app = CTk()
app.geometry("1200x600")  # Tamaño fijo para la pantalla
app.title("SmartGrow - Monitoreo Hidropónico")

# Crear el Navbar
navbar = Navbar(app)
navbar.pack(fill="x", side="top")

# Frame principal donde se mostrarán las diferentes vistas
main_frame = CTkFrame(app)
main_frame.pack(fill="both", expand=True)

# Diccionario para almacenar las vistas creadas
vistas = {}

# Función para cambiar la vista
def cambiar_vista(vista):
    # Limpiar el frame principal
    for widget in main_frame.winfo_children():
        widget.pack_forget()  # Ocultar en lugar de destruir

    # Si la vista no ha sido creada, crearla y almacenarla en el diccionario
    if vista not in vistas:
        if vista == "monitoreo":
            vistas[vista] = monitoreo(main_frame)
        elif vista == "historial":
            vistas[vista] = historial(main_frame)
        elif vista == "configuracion":
            vistas[vista] = Configuracion(main_frame)

    # Mostrar la vista correspondiente
    vistas[vista].pack(fill="both", expand=True)

# Configurar los botones del Navbar para cambiar la vista
navbar.home.configure(command=lambda: cambiar_vista("monitoreo"))
navbar.about.configure(command=lambda: cambiar_vista("historial"))
navbar.contact.configure(command=lambda: cambiar_vista("configuracion"))

# Mostrar la vista de monitoreo por defecto
cambiar_vista("monitoreo")

app.mainloop()