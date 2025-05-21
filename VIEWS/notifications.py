import customtkinter as ctk
from VIEWS.colors import COLORS
import serial
import threading
import time
from os import path
from notifypy import Notify
from customtkinter import CTkImage
from PIL import Image


class Notifications:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=15)
        
        # Header
        ctk.CTkLabel(
            self.frame, text="🔔 Notificaciones", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(pady=20)
        
        # Notifications container
        scrollable = ctk.CTkScrollableFrame(
            self.frame, fg_color=COLORS.background, height=450, corner_radius=10
        )
        scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        notificaciones = [
            {"titulo": "Actualización disponible", "mensaje": "Hay una nueva versión del sistema."},
            {"titulo": "Recordatorio", "mensaje": "No olvides revisar el módulo de configuración."},
            {"titulo": "Alerta", "mensaje": "Se ha detectado un cambio inusual en los datos."}
        ]
        
        for notif in notificaciones:
            card = self._create_notification_card(scrollable, notif["titulo"], notif["mensaje"])
            card.pack(fill="x", pady=10, padx=5)

    def _create_notification_card(self, parent, title, message):
        """Helper to create a notification card"""
        card = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=10, 
            border_width=1, border_color=COLORS.border)
        
        # Header with icon and title
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        # Icon
        icon_bg = ctk.CTkFrame(header, width=36, height=36, fg_color=COLORS.primary, corner_radius=18)
        icon_bg.pack(side="left")
        icon_bg.pack_propagate(False)
        ctk.CTkLabel(icon_bg, text="🔔", font=ctk.CTkFont(size=16), text_color="white").pack(expand=True)
        
        # Title and message
        text_frame = ctk.CTkFrame(header, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        ctk.CTkLabel(
            text_frame, text=title, font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLORS.text_dark, anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame, text=message, font=ctk.CTkFont(size=13),
            text_color=COLORS.text_light, wraplength=400, anchor="w"
        ).pack(anchor="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkButton(
            button_frame, text="✓ Marcar como leído", width=140, height=30, 
            font=ctk.CTkFont(size=13), fg_color=COLORS.secondary, text_color="white",
            command=lambda c=card: self.marcar_leido(c)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, text="🗑 Eliminar", width=100, height=30, 
            font=ctk.CTkFont(size=13), fg_color=COLORS.danger, text_color="white",
            command=lambda c=card: c.destroy()
        ).pack(side="right", padx=5)
        
        return card
    
    def marcar_leido(self, card):
        card.configure(fg_color="#F0FDF4")  # Light green background

    



    def read_serial_data(self):
        try:
            ser = serial.Serial('COM11', 9600, timeout=1)
            time.sleep(2)  # Esperar reinicio del Arduino

            buffer = ""
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()

                if line:
                    
                    print(f"📥 Recibido: {line}")  # 👈 Imprime cada línea recibida

                    buffer += line + "\n"

                    if "-----" in line:
                        print("🧩 Bloque detectado, analizando...")
                        self.parse_serial_block(buffer)
                        buffer = ""

                time.sleep(0.2)

        except Exception as e:
            print("❌ Error al abrir el puerto serial:", e)

    def parse_serial_block(self, data_block):
        try:
            lines = data_block.strip().splitlines()
            values = {}

            for line in lines:
                if "Temperatura" in line:
                    temp = ''.join(c for c in line if c.isdigit() or c == '.' or c == ',')
                    values["Temperature"] = f"{temp} °C"

                elif "Conductividad" in line or "EC:" in line:
                    ec = ''.join(c for c in line if c.isdigit() or c == '.' or c == ',')
                    values["Conductivity"] = f"{ec} mS/cm"

                elif "Nivel_agua" in line or "Nivel de agua" in line:
                    nivel = ''.join(c for c in line if c.isdigit() or c == '.' or c == ',')
                    values["Water Level"] = f"{nivel} cm"

                elif "pH" in line:
                    ph = ''.join(c for c in line if c.isdigit() or c == '.' or c == ',')
                    values["pH"] = f"{ph}"

            for key, val in values.items():
                if key in self.stats_labels:
                    self.stats_labels[key].after(0, lambda lbl=self.stats_labels[key], v=val: lbl.configure(text=v))

        except Exception as e:
            print("❌ Error al analizar datos:", e)

    notification = Notify()
    notification.title = "Smartgrow"
    notification.message = "temperature: 25.5°C"

    icono = path.join("../Sources/logonoti.png")
    audio = path.join("../audio/sonidonoti.wav")

    direcion = path.abspath(path.dirname(__file__))

    notification.audio = path.join(direcion, audio)
    notification.icon = path.join(direcion, icono)

    notification.send()

    





    