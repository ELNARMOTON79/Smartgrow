import customtkinter as ctk
from VIEWS.colors import COLORS

class CustomView:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=15)
        
        # Header
        ctk.CTkLabel(
            self.frame, text="Settings", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(pady=20)
        
        # Content container
        content = ctk.CTkFrame(self.frame, fg_color=COLORS.background, corner_radius=10)
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Inputs
        self.ph_entry = self._create_labeled_entry(content, "Ideal pH:")
        self.temp_entry = self._create_labeled_entry(content, "Ideal Temperature (°C):")
        self.ec_entry = self._create_labeled_entry(content, "Ideal Electroconductivity (μS/cm):")

        # Botón de guardar
        save_btn = ctk.CTkButton(
            content, text="Save", fg_color=COLORS.primary, hover_color=COLORS.secondary,
            text_color="white", command=self.save_settings
        )
        save_btn.pack(pady=10)

        # Botones para control de la lámpara
        btn_frame = ctk.CTkFrame(content, fg_color=COLORS.background)
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="Turn on Lamp", fg_color=COLORS.secondary,
            text_color="white", command=self.toggle_light
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="Change Spectrum", fg_color=COLORS.primary,
            text_color="white", command=self.change_spectrum
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="Adjust Intensity", fg_color=COLORS.danger,
            text_color="white", command=self.adjust_intensity
        ).pack(side="left", padx=5)

    def _create_labeled_entry(self, parent, label):
        container = ctk.CTkFrame(parent, fg_color=COLORS.background)
        container.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(container, text=label, text_color=COLORS.text_dark).pack(anchor="w")
        entry = ctk.CTkEntry(container, fg_color=COLORS.card, text_color=COLORS.text_dark, border_color=COLORS.border)
        entry.pack(fill="x", pady=2)
        return entry

    def save_settings(self):
        ph = self.ph_entry.get()
        temp = self.temp_entry.get()
        ec = self.ec_entry.get()
        print(f"Guardado: pH={ph}, Temp={temp}, EC={ec}")
        # Aquí puedes conectar lógica de base de datos o enviar a hardware

    def toggle_light(self):
        print("Lámpara encendida/apagada")

    def change_spectrum(self):
        print("Espectro de luz cambiado")

    def adjust_intensity(self):
        print("Intensidad ajustada")
