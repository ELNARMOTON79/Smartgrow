from customtkinter import *
from tkinter import ttk

class historial(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Crear un frame principal para contener las métricas
        self.main_frame = CTkFrame(self, fg_color="#CFF4D2")  # Fondo verde claro
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear la tabla con Treeview
        self.tree = ttk.Treeview(
            self.main_frame,
            columns=("Día", "Hora", "Temperatura", "PH", "Conductividad Eléctrica", "Bomba peristáltica"),
            show="headings",
            style="Custom.Treeview"
        )

        # Configurar el estilo de la tabla
        style = ttk.Style()
        style.theme_use("default")  # Usar el tema por defecto para poder personalizarlo

        # Estilo general de la tabla
        style.configure("Custom.Treeview",
                        background="#FFFFFF",  # Fondo blanco para las filas
                        foreground="black",  # Color del texto
                        rowheight=30,  # Altura de las filas
                        font=("Arial", 12),  # Fuente y tamaño
                        fieldbackground="#FFFFFF",  # Fondo blanco para el área de la tabla
                        bordercolor="#CFF4D2",  # Color del borde
                        borderwidth=1)  # Ancho del borde

        # Estilo de los encabezados
        style.configure("Custom.Treeview.Heading",
                        background="#56C596",  # Fondo verde claro para los encabezados
                        foreground="black",  # Color del texto de los encabezados
                        font=("Arial", 14, "bold"),  # Fuente y tamaño de los encabezados
                        padding=10,  # Espaciado interno
                        relief="flat")  # Sin relieve para un aspecto más moderno

        # Estilo de las filas alternas
        style.map("Custom.Treeview",
                  background=[("selected", "#32909C"), ("!selected", "#E8F5E9")],  # Fondo verde claro alterno
                  foreground=[("selected", "white")])  # Texto blanco cuando está seleccionado

        # Configurar las columnas
        self.tree.heading("Día", text="Día")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Temperatura", text="Temperatura")
        self.tree.heading("PH", text="PH")
        self.tree.heading("Conductividad Eléctrica", text="Conductividad Eléctrica")
        self.tree.heading("Bomba peristáltica", text="Bomba peristáltica")

        # Ajustar el ancho de las columnas
        self.tree.column("Día", width=120, anchor="center")
        self.tree.column("Hora", width=120, anchor="center")
        self.tree.column("Temperatura", width=120, anchor="center")
        self.tree.column("PH", width=120, anchor="center")
        self.tree.column("Conductividad Eléctrica", width=180, anchor="center")
        self.tree.column("Bomba peristáltica", width=180, anchor="center")

        # Insertar datos de ejemplo
        self.tree.insert("", "end", values=("2023-10-01", "12:00", "25°C", "7.0", "500 µS/cm", "ON"))
        self.tree.insert("", "end", values=("2023-10-01", "13:00", "26°C", "7.1", "510 µS/cm", "OFF"))
        self.tree.insert("", "end", values=("2023-10-01", "14:00", "27°C", "7.2", "520 µS/cm", "ON"))
        self.tree.insert("", "end", values=("2023-10-01", "15:00", "26.5°C", "7.1", "515 µS/cm", "OFF"))

        # Mostrar la tabla
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)