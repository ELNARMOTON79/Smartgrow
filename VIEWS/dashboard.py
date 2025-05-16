import customtkinter as ctk
from PIL import Image, ImageTk
import os
import serial
import threading
import time
from VIEWS.colors import COLORS  # Asegúrate de que COLORS esté correctamente definido

class Dashboard:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=15)
        
        # Sección de estadísticas
        stats_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        self.stats_labels = {}
        stats_data = [
            {"title": "Temperatura", "value": "Esperando...", "icon": "🌡️", "color": COLORS.primary},
            {"title": "pH", "value": "6.2", "icon": "🧪", "color": COLORS.secondary},  # Valor estático por ahora
            {"title": "Conductividad", "value": "Esperando...", "icon": "⚡", "color": "#F59E0B"},
            {"title": "Water Level", "value": "100%", "icon": "🚰", "color": "#F59E0B"}  # Valor estático por ahora
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
            # Cambia esto al puerto correcto en tu sistema
            ser = serial.Serial('COM3', 9600, timeout=1)
            time.sleep(2)  # Espera a que el Arduino reinicie

            while True:
                line1 = ser.readline().decode('utf-8').strip()
                line2 = ser.readline().decode('utf-8').strip()

                if line1.startswith("Voltaje") and line2.startswith("Temperatura"):
                    try:
                        ec_part = line1.split("Conductividad:")[1].strip().split(" ")[0]
                        ec_value = f"{ec_part} mS/cm"

                        temp_part = line2.split("=")[1].strip().split(" ")[0]
                        temp_value = f"{temp_part} °C"

                        # Actualizar las etiquetas en el hilo principal
                        self.stats_labels["Temperatura"].after(0, self.stats_labels["Temperatura"].configure, {"text": temp_value})
                        self.stats_labels["Conductividad"].after(0, self.stats_labels["Conductividad"].configure, {"text": ec_value})

                    except Exception as parse_error:
                        print("Error al analizar los datos:", parse_error)
                
                time.sleep(1)

        except Exception as e:
            print("Error abriendo el puerto serial:", e)
