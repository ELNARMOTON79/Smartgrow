import customtkinter as ctk
from VIEWS.colors import COLORS
import tkinter.ttk as ttk 
import datetime
from base_datos.contacto import obtener_todos, filtrar_por_fecha, filtrar_por_hora

class History:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=15)


        self._crear_header()
        self._crear_filtros()
        self._crear_tabla()
        self._crear_paginacion()

        # Obtiene los datos dinámicamente desde contacto.obtener_todos()
        self.datos = self.obtener_datos()

        self.aplicar_filtro()

    def obtener_datos(self):
        # Llama al método obtener_todos para obtener los datos desde la base de datos
        return obtener_todos()

    def _crear_header(self):
        ctk.CTkLabel(
            self.frame, text="📊 Historial", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(pady=20)

    def _crear_filtros(self):
        try:
            from tkcalendar import DateEntry
            self.tkcalendar_available = True
        except ImportError:
            self.tkcalendar_available = False
        import datetime
        filtro_frame = ctk.CTkFrame(self.frame, fg_color=COLORS.background, corner_radius=10)
        filtro_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Update hour options to 24-hour format
        self.hora_opciones = ["Todo"] + [f"{h:02}:00" for h in range(0, 24)]

        filtros_y_boton = ctk.CTkFrame(filtro_frame, fg_color="transparent")
        filtros_y_boton.pack(padx=10, pady=10, fill="x")

        # Ajusta las columnas: ahora solo hay 4 (fecha, from, to, botón)
        filtros_y_boton.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="filtros")

        # Elimina el filtro de día de la semana
        # def crear_filtro(label_text, opciones, col):
        #     sub_frame = ctk.CTkFrame(filtros_y_boton, fg_color="transparent")
        #     sub_frame.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        #     ctk.CTkLabel(sub_frame, text=label_text, text_color=COLORS.text_dark).pack()
        #     combo = ttk.Combobox(sub_frame, values=opciones, state="readonly", width=18)
        #     combo.set("All")
        #     combo.pack(ipady=6, fill="x",padx=4)
        #     return combo

        # self.dia_filtro = crear_filtro("Day", self.dia_opciones, 0)

        # Calendario para seleccionar fecha (si está disponible)
        cal_frame = ctk.CTkFrame(filtros_y_boton, fg_color="transparent")
        cal_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        ctk.CTkLabel(cal_frame, text="Fecha", text_color=COLORS.text_dark).pack()
        if self.tkcalendar_available:
            self.fecha_filtro = DateEntry(
                cal_frame,
                width=21,  # Ajusta el ancho para que coincida visualmente con los Combobox (por defecto 18)
                background='darkblue',
                foreground='white',
                borderwidth=2,
                date_pattern='yyyy-mm-dd',
                showothermonthdays=True,
                showweeknumbers=True,
            )
            self.fecha_filtro.set_date(datetime.date.today())
            self.fecha_filtro.pack(fill="x", padx=4, ipady=6)  # Usa ipady=6 igual que los Combobox
        else:
            self.fecha_filtro = None
            ctk.CTkLabel(cal_frame, text="tkcalendar\nnot installed", text_color="red").pack()

        def crear_filtro(label_text, opciones, col):
            sub_frame = ctk.CTkFrame(filtros_y_boton, fg_color="transparent")
            sub_frame.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
            ctk.CTkLabel(sub_frame, text=label_text, text_color=COLORS.text_dark).pack()
            combo = ttk.Combobox(sub_frame, values=opciones, state="readonly", width=18)
            combo.set("Todo")
            combo.pack(ipady=6, fill="x",padx=4)
            return combo

        self.hora_inicio = crear_filtro("Desde", self.hora_opciones, 1)
        self.hora_fin = crear_filtro("Hasta", self.hora_opciones, 2)

        # Botón de filtro
        boton_frame = ctk.CTkFrame(filtros_y_boton, fg_color="transparent")
        boton_frame.grid(row=0, column=3, padx=10, pady=(18, 0), sticky="nsew")
        ctk.CTkButton(
            boton_frame, text="🔍 Filtrar", fg_color=COLORS.primary, text_color="white",
            command=self.aplicar_filtro
        ).pack()



    def _crear_tabla(self):
        # Ensure the table container is a proper widget object
        self.table_container = ctk.CTkScrollableFrame(
            self.frame, fg_color=COLORS.background, corner_radius=10
        )
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    def _crear_paginacion(self):
        self.filas_por_pagina = 6
        self.pagina_actual = 0

        pag_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        pag_frame.pack(pady=(0, 20))

        self.btn_anterior = ctk.CTkButton(
            pag_frame, text="⬅ Anterior", fg_color=COLORS.secondary, text_color="white",
            command=self.ir_anterior
        )
        self.btn_anterior.pack(side="left", padx=10)

        self.pagina_label = ctk.CTkLabel(
            pag_frame, text="Página 1", text_color=COLORS.text_dark
        )
        self.pagina_label.pack(side="left", padx=10)

        self.btn_siguiente = ctk.CTkButton(
            pag_frame, text="Siguiente ➡", fg_color=COLORS.primary, text_color="white",
            command=self.ir_siguiente
        )
        self.btn_siguiente.pack(side="left", padx=10)

    def aplicar_filtro(self):
        fecha = self.fecha_filtro.get() if self.fecha_filtro else None
        hora_inicio = self.hora_inicio.get()
        hora_fin = self.hora_fin.get()

        if fecha and fecha != "Todo":
            self.datos_filtrados = filtrar_por_fecha(fecha)
        else:
            self.datos_filtrados = obtener_todos()

        if hora_inicio != "Todo" or hora_fin != "Todo":
            # Parse hora_inicio and hora_fin into datetime.time objects
            hora_inicio = datetime.datetime.strptime(hora_inicio, "%H:%M").time() if hora_inicio != "Todo" else None
            hora_fin = datetime.datetime.strptime(hora_fin, "%H:%M").time() if hora_fin != "Todo" else None

            datos_filtrados_por_hora = []
            for row in self.datos_filtrados:
                if len(row) < 2:  # Verifica que el dato tenga al menos 2 columnas (fecha y hora)
                    continue
                hora = (datetime.datetime.min + row[1]).time()  # Convert timedelta to time
                if hora_inicio and hora < hora_inicio:
                    continue
                if hora_fin and hora > hora_fin:
                    continue
                datos_filtrados_por_hora.append(row)
            self.datos_filtrados = datos_filtrados_por_hora

        # Asegúrate de que cada fila tenga al menos 5 columnas, rellena con valores vacíos si es necesario
        self.datos_filtrados = [
            (row[0], row[1], row[2] if len(row) > 2 else "N/A", row[3] if len(row) > 3 else "N/A", row[4] if len(row) > 4 else "N/A")
            for row in self.datos_filtrados
        ]

        self.pagina_actual = 0
        self.mostrar_tabla_paginada()

    def mostrar_tabla_paginada(self):
        for widget in self.table_container.winfo_children():
            widget.destroy()

        headers = ["📅 Fecha", "⏰ Hora", "🌡️ Temp. (°C)", "🧪 pH", "⚡ Conduct. (µS/cm)"]
        header_frame = ctk.CTkFrame(self.table_container, fg_color=COLORS.primary)
        header_frame.pack(fill="x", pady=(0, 8), padx=4)

        for i, header in enumerate(headers):
            header_frame.columnconfigure(i, weight=1)
            ctk.CTkLabel(
                header_frame, text=header, font=ctk.CTkFont(size=14, weight="bold"),
                height=35, text_color="white"
            ).grid(row=0, column=i, padx=2, sticky="nsew")

        inicio = self.pagina_actual * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina
        pagina_datos = self.datos_filtrados[inicio:fin]

        for idx, row_data in enumerate(pagina_datos):
            row_frame = ctk.CTkFrame(
                self.table_container,
                fg_color=COLORS.card if idx % 2 == 0 else "#ECEFF1"
            )
            row_frame.pack(fill="x", pady=2, padx=4)

            for i, col_data in enumerate(row_data):
                row_frame.columnconfigure(i, weight=1)
                ctk.CTkLabel(
                    row_frame, text=col_data, font=ctk.CTkFont(size=13),
                    height=30, text_color=COLORS.text_dark
                ).grid(row=0, column=i, padx=2, sticky="nsew")

        total_paginas = max(1, (len(self.datos_filtrados) + self.filas_por_pagina - 1) // self.filas_por_pagina)
        self.pagina_label.configure(text=f"Página {self.pagina_actual + 1} de {total_paginas}")
        self.btn_anterior.configure(state="normal" if self.pagina_actual > 0 else "disabled")
        self.btn_siguiente.configure(state="normal" if self.pagina_actual < total_paginas - 1 else "disabled")

    def ir_anterior(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.mostrar_tabla_paginada()

    def ir_siguiente(self):
        total_paginas = (len(self.datos_filtrados) + self.filas_por_pagina - 1) // self.filas_por_pagina
        if self.pagina_actual < total_paginas - 1:
            self.pagina_actual += 1
            self.mostrar_tabla_paginada()