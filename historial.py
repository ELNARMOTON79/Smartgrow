from customtkinter import *
from CTkTable import *

class historial(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Crear un frame principal para contener las métricas
        self.main_frame = CTkFrame(self, fg_color="#CFF4D2")  # Fondo verde claro
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título "History"
        self.title_label = CTkLabel(self.main_frame, text="History", font=("Arial", 20, "bold"), text_color="#32909C")
        self.title_label.pack(pady=(10, 5))  # Espaciado superior

        # Crear un frame con bordes redondeados para la tabla
        self.table_frame = CTkFrame(self.main_frame, fg_color="#FFFFFF", corner_radius=15)  # Fondo blanco con bordes redondeados
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Datos de la tabla
        value = [
            ["Día", "Hora", "Temperatura", "PH", "Conductividad Eléctrica", "Bomba peristáltica"],
            ["2023-10-01", "12:00", "25°C", "7.0", "500 µS/cm", "ON"],
            ["2023-10-01", "13:00", "26°C", "7.1", "510 µS/cm", "OFF"],
            ["2023-10-01", "14:00", "27°C", "7.2", "520 µS/cm", "ON"],
            ["2023-10-01", "15:00", "26.5°C", "7.1", "515 µS/cm", "OFF"]
        ]

        # Crear la tabla usando CTkTable
        self.table = CTkTable(
            master=self.table_frame,
            row=5,  # Número de filas (incluyendo el encabezado)
            column=6,  # Número de columnas
            values=value,  # Datos de la tabla
            header_color="#56C596",  # Color de fondo del encabezado
            colors=["#E8F5E9", "#FFFFFF"],  # Colores alternos para las filas
            hover_color="#32909C",  # Color al pasar el mouse
            font=("Arial", 14),  # Fuente y tamaño del texto
            text_color="black",  # Color del texto
            corner_radius=10  # Bordes redondeados para las celdas
        )

        # Mostrar la tabla
        self.table.pack(expand=True, fill="both", padx=10, pady=10)
