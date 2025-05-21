import customtkinter as ctk
from VIEWS.colors import COLORS
from CTkMessagebox import CTkMessagebox  # ✅ Importar el mensaje emergente

class CustomView:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=15)
        self.settings = {}

        # Header
        ctk.CTkLabel(
            self.frame, text="Settings", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(pady=20)

        content = ctk.CTkFrame(self.frame, fg_color=COLORS.background, corner_radius=10)
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Inputs
        self.ph_entry = self._create_labeled_entry(content, "pH ideal:")
        self.temp_entry = self._create_labeled_entry(content, "Temperatura ideal (°C):")
        self.ec_entry = self._create_labeled_entry(content, "Electroconductividad ideal (μS/cm):")

        # Botón de guardar
        save_btn = ctk.CTkButton(
            content, text="Guardar", fg_color=COLORS.primary, hover_color=COLORS.secondary,
            text_color="white", command=self.save_settings
        )
        save_btn.pack(pady=10)

        # Etiqueta para mostrar confirmación
        self.status_label = ctk.CTkLabel(content, text="", text_color=COLORS.text_dark)
        self.status_label.pack()

        # Botones de control
        btn_frame = ctk.CTkFrame(content, fg_color=COLORS.background)
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="Encender Lámpara", fg_color=COLORS.secondary,
            text_color="white", command=self.toggle_light
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="Cambiar Espectro", fg_color=COLORS.primary,
            text_color="white", command=self.change_spectrum
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="Ajustar Intensidad", fg_color=COLORS.danger,
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
        # Mostrar confirmación al usuario
        msg = CTkMessagebox(title="Confirmación", message="¿Estás seguro de guardar los valores?",
                            icon="question", option_1="Sí", option_2="No")

        if msg.get() == "Sí":
            self.settings = {
                "pH": self.ph_entry.get(),
                "Temperatura": self.temp_entry.get(),
                "EC": self.ec_entry.get()
            }
            print("Guardado:", self.settings)
            self.status_label.configure(text="Configuración guardada correctamente ✅")
            self.status_label.after(3000, lambda: self.status_label.configure(text=""))
        else:
            self.status_label.configure(text="Guardado cancelado ❌")
            self.status_label.after(3000, lambda: self.status_label.configure(text=""))

    def toggle_light(self):
        print("Lámpara encendida/apagada")

    def change_spectrum(self):
        print("Espectro de luz cambiado")

    def adjust_intensity(self):
        print("Intensidad ajustada")
