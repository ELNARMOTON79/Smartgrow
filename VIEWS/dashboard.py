import customtkinter as ctk
from PIL import Image, ImageTk
import os
import serial
import threading
import time
from VIEWS.colors import COLORS  # Asegúrate de que este archivo existe y tiene los colores correctos
from base_datos.contacto import guardar_registro  # Asegúrate de que este archivo existe y tiene la clase Contacto

class Dashboard:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=15)
        
        # Sección de estadísticas
        stats_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        self.stats_labels = {}
        stats_data = [
            {"title": "Temperature", "value": "Waiting...", "icon": "🌡️", "color": COLORS.primary},
            {"title": "pH", "value": "Waiting...", "icon": "🧪", "color": COLORS.secondary},
            {"title": "Conductivity", "value": "Waiting...", "icon": "⚡", "color": "#F59E0B"},
            {"title": "Water Level", "value": "Waiting...", "icon": "🚰", "color": "#3B82F6"}
        ]
        
        for stat in stats_data:
            card, value_label = self._create_card(stats_frame, stat["title"], stat["value"], stat["icon"], stat["color"])
            card.pack(side="left", fill="x", expand=True, padx=5)
            self.stats_labels[stat["title"]] = value_label
        
        # Contenedor de imagen
        image_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        image_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.image_label = ctk.CTkLabel(image_container, text="")
        self.image_label.pack(fill="both", expand=True)
        self.frame.bind("<Configure>", self._resize_image)
        
        self.tk_image = None
        self.original_image = None
        image_path = "./Sources/fondo_light.png"
        if os.path.exists(image_path):
            self.original_image = Image.open(image_path)
        else:
            self.image_label.configure(text="Imagen no encontrada", text_color=COLORS.danger)
        
        # Iniciar lectura del puerto serial en segundo plano
        threading.Thread(target=self.read_serial_data, daemon=True).start()

    def _create_card(self, parent, title, value, icon, color):
        card = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=10, border_width=1, border_color=COLORS.border)
        
        icon_bg = ctk.CTkFrame(card, width=36, height=36, fg_color=color, corner_radius=18)
        icon_bg.pack(side="left", padx=15, pady=15)
        icon_bg.pack_propagate(False)
        ctk.CTkLabel(icon_bg, text=icon, font=ctk.CTkFont(size=16), text_color="white").pack(expand=True)
        
        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=15)
        
        value_label = ctk.CTkLabel(
            text_frame, text=value, font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS.text_dark
        )
        value_label.pack(anchor="w")
        
        ctk.CTkLabel(
            text_frame, text=title, font=ctk.CTkFont(size=14),
            text_color=COLORS.text_light
        ).pack(anchor="w")
        
        return card, value_label

    def _resize_image(self, event):
        if self.original_image:
            resized = self.original_image.resize((event.width, event.height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(resized)
            self.image_label.configure(image=self.tk_image)

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

        # Dentro de parse_serial_block al final:
        temperatura = values.get("Temperature", "").replace(" °C", "")
        ph = values.get("pH", "")
        conductividad = values.get("Conductivity", "").replace(" mS/cm", "")
        nivel_agua = values.get("Water Level", "").replace(" cm", "")

        guardar_registro(temperatura, ph, conductividad, nivel_agua)
