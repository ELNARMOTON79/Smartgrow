import customtkinter as ctk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
import os

class MainContent:
    def __init__(self, master):
        self.frame = ctk.CTkFrame(master=master, fg_color="#FFFFFF")
        self.frame.pack(side="left", fill="both", expand=True)

        self.content_container = ctk.CTkFrame(master=self.frame, fg_color="#FFFFFF")
        self.content_container.pack(fill="both", expand=True)

        self.views = {}
        self.tk_image = None
        self.original_image = None

        self._create_views()
        self.show_view("home")

    def _create_views(self):
        # HOME
        home_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        self.image_label = ctk.CTkLabel(home_frame, text="")
        self.image_label.pack(fill="both", expand=True)
        home_frame.bind("<Configure>", self._resize_image)
        self.views["home"] = home_frame

        image_path = "./Sources/fondo_light.png"
        if os.path.exists(image_path):
            self.original_image = Image.open(image_path)
        else:
            self.image_label.configure(text="Imagen no encontrada", text_color="red")

        # HISTORY - Tabla estética
        history_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        ctk.CTkLabel(history_frame, text="📊 History", font=ctk.CTkFont(size=22, weight="bold"),
                    text_color="#222").pack(pady=15)

        table_container = ctk.CTkScrollableFrame(history_frame, height=450, fg_color="#FAFAFA", corner_radius=10)
        table_container.pack(fill="both", expand=True, padx=30, pady=10)

        headers = ["📅 Día", "⏰ Hora", "🌡 Temp. (°C)", "🧪 pH", "⚡ Conduct. (µS/cm)"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(table_container, text=header, font=ctk.CTkFont(size=14, weight="bold"),
                        width=140, height=35, fg_color="#E0E0E0", corner_radius=8,
                        text_color="#333").grid(row=0, column=i, padx=4, pady=6)

        datos = [
            ["Lunes", "08:00", "22.5", "6.2", "1300"],
            ["Lunes", "12:00", "24.1", "6.3", "1400"],
            ["Martes", "08:00", "21.8", "6.1", "1250"],
        ]

        for fila_idx, fila in enumerate(datos, start=1):
            for col_idx, valor in enumerate(fila):
                ctk.CTkLabel(table_container, text=valor, font=ctk.CTkFont(size=13),
                            width=140, height=30, fg_color="#FFFFFF", corner_radius=8,
                            text_color="#444").grid(row=fila_idx, column=col_idx, padx=4, pady=4)

        self.views["history"] = history_frame

        # NOTIFICATIONS - Estético
        notif_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        ctk.CTkLabel(notif_frame, text="🔔 Notificaciones", font=ctk.CTkFont(size=22, weight="bold"),
                    text_color="#222").pack(pady=15)

        scrollable = ctk.CTkScrollableFrame(notif_frame, fg_color="#F4F4F4", height=450, corner_radius=10)
        scrollable.pack(fill="both", expand=True, padx=30, pady=10)

        notificaciones = [
            {"titulo": "Actualización disponible", "mensaje": "Hay una nueva versión del sistema."},
            {"titulo": "Recordatorio", "mensaje": "No olvides revisar el módulo de configuración."},
            {"titulo": "Alerta", "mensaje": "Se ha detectado un cambio inusual en los datos."}
        ]

        for notif in notificaciones:
            card = ctk.CTkFrame(scrollable, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#DCDCDC")
            card.pack(fill="x", pady=10, padx=5)

            top_frame = ctk.CTkFrame(card, fg_color="transparent")
            top_frame.pack(fill="x", padx=10, pady=5)

            icon_label = ctk.CTkLabel(top_frame, text="🔔", font=ctk.CTkFont(size=22))
            icon_label.pack(side="left")

            text_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=10)

            ctk.CTkLabel(text_frame, text=notif["titulo"], font=ctk.CTkFont(size=15, weight="bold"),
                        text_color="#333", anchor="w").pack(anchor="w")
            ctk.CTkLabel(text_frame, text=notif["mensaje"], font=ctk.CTkFont(size=13),
                        text_color="#666", wraplength=400, anchor="w").pack(anchor="w")

            button_frame = ctk.CTkFrame(card, fg_color="transparent")
            button_frame.pack(fill="x", padx=10, pady=5)

            ctk.CTkButton(button_frame, text="✓ Marcar como leído", width=140, height=30, font=ctk.CTkFont(size=13),
                        fg_color="#C8E6C9", hover_color="#A5D6A7", text_color="#1B5E20",
                        command=lambda c=card: self.marcar_leido(c)).pack(side="left", padx=5)

            ctk.CTkButton(button_frame, text="🗑 Eliminar", width=100, height=30, font=ctk.CTkFont(size=13),
                        fg_color="#FFCDD2", hover_color="#EF9A9A", text_color="#B71C1C",
                        command=lambda c=card: c.destroy()).pack(side="right", padx=5)

        self.views["notifications"] = notif_frame

        # CUSTOM
        custom_frame = ctk.CTkFrame(self.content_container, fg_color="#FFFFFF")
        self.custom_label = ctk.CTkLabel(custom_frame, text="", font=ctk.CTkFont(size=20))
        self.custom_label.pack(pady=20)
        self.views["custom"] = custom_frame


    def _resize_image(self, event):
        if self.original_image:
            resized = self.original_image.resize((event.width, event.height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized)
            self.image_label.configure(image=self.tk_image)

    def show_view(self, view_name):
        for view in self.views.values():
            view.pack_forget()
        if view_name in self.views:
            self.views[view_name].pack(fill="both", expand=True)

    def show_custom_view(self, text):
        self.custom_label.configure(text=text)
        self.show_view("custom")

    def marcar_leido(self, card):
        card.configure(fg_color="#D0EAD7")