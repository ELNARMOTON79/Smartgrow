import customtkinter as ctk
from VIEWS.colors import COLORS

class History:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=15)

        # Header
        ctk.CTkLabel(
            self.frame, text="\ud83d\udcca Historial", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(pady=20)

        # --- Filtros ---
        filtro_frame = ctk.CTkFrame(self.frame, fg_color=COLORS.background, corner_radius=10)
        filtro_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.dia_opciones = ["Todos", "Lunes", "Martes", "Mi\u00e9rcoles", "Jueves", "Viernes"]
        self.hora_opciones = ["Todos"] + [f"{h:02}:00" for h in range(0, 24)]

        self.dia_filtro = ctk.CTkOptionMenu(filtro_frame, values=self.dia_opciones, fg_color=COLORS.card)
        self.dia_filtro.set("Todos")
        self.dia_filtro.pack(side="left", padx=10, pady=10)

        self.hora_inicio = ctk.CTkOptionMenu(filtro_frame, values=self.hora_opciones, fg_color=COLORS.card)
        self.hora_inicio.set("Todos")
        self.hora_inicio.pack(side="left", padx=10)

        self.hora_fin = ctk.CTkOptionMenu(filtro_frame, values=self.hora_opciones, fg_color=COLORS.card)
        self.hora_fin.set("Todos")
        self.hora_fin.pack(side="left", padx=10)

        ctk.CTkButton(
            filtro_frame, text="Filtrar", fg_color=COLORS.primary, text_color="white",
            command=self.aplicar_filtro
        ).pack(side="left", padx=10)

        # Contenedor tabla
        self.table_container = ctk.CTkScrollableFrame(
            self.frame, height=450, fg_color=COLORS.background, corner_radius=10
        )
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Paginación
        self.filas_por_pagina = 5
        self.pagina_actual = 0

        pag_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        pag_frame.pack(pady=(0, 10))

        self.btn_anterior = ctk.CTkButton(
            pag_frame, text="\u2b05 Anterior", fg_color=COLORS.secondary, text_color="white",
            command=self.ir_anterior
        )
        self.btn_anterior.pack(side="left", padx=10)

        self.pagina_label = ctk.CTkLabel(
            pag_frame, text="Página 1", text_color=COLORS.text_dark
        )
        self.pagina_label.pack(side="left", padx=10)

        self.btn_siguiente = ctk.CTkButton(
            pag_frame, text="Siguiente \u27a1", fg_color=COLORS.primary, text_color="white",
            command=self.ir_siguiente
        )
        self.btn_siguiente.pack(side="left", padx=10)

        # Datos de ejemplo
        self.datos = [
            ["Lunes", "08:00", "22.5", "6.2", "1300"],
            ["Lunes", "12:00", "24.1", "6.3", "1400"],
            ["Martes", "08:00", "21.8", "6.1", "1250"],
            ["Martes", "12:00", "23.0", "6.4", "1350"],
            ["Miércoles", "09:00", "22.0", "6.2", "1320"],
            ["Jueves", "10:00", "22.8", "6.5", "1330"],
            ["Viernes", "11:00", "23.2", "6.3", "1380"],
            ["Viernes", "13:00", "23.6", "6.2", "1420"],
        ]

        self.aplicar_filtro()

    def aplicar_filtro(self):
        dia = self.dia_filtro.get()
        hora_inicio = self.hora_inicio.get()
        hora_fin = self.hora_fin.get()

        self.datos_filtrados = []

        for row in self.datos:
            dia_match = (dia == "Todos" or row[0] == dia)
            hora_match = True

            if hora_inicio != "Todos" and row[1] < hora_inicio:
                hora_match = False
            if hora_fin != "Todos" and row[1] > hora_fin:
                hora_match = False

            if dia_match and hora_match:
                self.datos_filtrados.append(row)

        self.pagina_actual = 0
        self.mostrar_tabla_paginada()

    def mostrar_tabla_paginada(self):
        for widget in self.table_container.winfo_children():
            widget.destroy()

        headers = ["\ud83d\udcc5 Día", "\u23f0 Hora", "\ud83c\udf21 Temp. (\u00b0C)", "\ud83e\uddea pH", "\u26a1 Conduct. (\u00b5S/cm)"]
        header_frame = ctk.CTkFrame(self.table_container, fg_color=COLORS.primary)
        header_frame.pack(fill="x", pady=(0, 8), padx=4)

        for i, header in enumerate(headers):
            header_frame.columnconfigure(i, weight=1)
            ctk.CTkLabel(
                header_frame, text=header, font=ctk.CTkFont(size=14, weight="bold"),
                height=35, text_color="white", fg_color=COLORS.primary, corner_radius=6
            ).grid(row=0, column=i, padx=2, sticky="nsew")

        inicio = self.pagina_actual * self.filas_por_pagina
        fin = inicio + self.filas_por_pagina
        pagina_datos = self.datos_filtrados[inicio:fin]

        for idx, row_data in enumerate(pagina_datos):
            row_frame = ctk.CTkFrame(
                self.table_container,
                fg_color=COLORS.card if idx % 2 == 0 else "#F3F4F6"
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
