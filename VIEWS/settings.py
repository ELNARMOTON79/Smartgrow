import customtkinter as ctk
from VIEWS.colors import COLORS
from CTkMessagebox import CTkMessagebox  # ✅ Importar el mensaje emergente
import re

class CustomView:
    def __init__(self, parent, on_settings_saved=None):
        self.frame = ctk.CTkFrame(parent, fg_color=COLORS.card, corner_radius=15)
        self.settings = {}
        self.on_settings_saved = on_settings_saved  # Nuevo: callback para notificar cambios

        # Validadores
        self.vcmd_ph = self.frame.register(self.validate_ph_format)
        self.vcmd_2digit = self.frame.register(self.validate_two_digits)

        # Header
        ctk.CTkLabel(
            self.frame, text="Settings", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(pady=20)

        content = ctk.CTkFrame(self.frame, fg_color=COLORS.background, corner_radius=10)
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Inputs: ahora son rangos (min y max) para cada parámetro
        self.ph_min_entry, self.ph_max_entry = self._create_labeled_range(content, "pH ideal:", self.vcmd_ph)
        self.temp_min_entry, self.temp_max_entry = self._create_labeled_range(content, "Temperatura ideal (°C):", self.vcmd_2digit)
        self.ec_min_entry, self.ec_max_entry = self._create_labeled_range(content, "Electroconductividad ideal (μS/cm):", self.vcmd_2digit)

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

    def _create_labeled_range(self, parent, label, validate_command):
        container = ctk.CTkFrame(parent, fg_color=COLORS.background)
        container.pack(pady=5)  # quitamos fill="x" para que no se expanda, y quede centrado

        # Etiqueta centrada
        ctk.CTkLabel(container, text=label, text_color=COLORS.text_dark).pack(anchor="center", pady=(0, 2))

        range_frame = ctk.CTkFrame(container, fg_color=COLORS.background)
        range_frame.pack()

        # Entradas min y max centradas con grid
        min_entry = ctk.CTkEntry(
            range_frame,
            fg_color=COLORS.card,
            text_color=COLORS.text_dark,
            border_color=COLORS.border,
            width=60,
            validate="key",
            validatecommand=(validate_command, "%P")
        )
        min_entry.grid(row=0, column=0, padx=(0, 5), pady=2)

        ctk.CTkLabel(range_frame, text="mín", text_color=COLORS.text_dark).grid(row=0, column=1, padx=(0, 15))

        max_entry = ctk.CTkEntry(
            range_frame,
            fg_color=COLORS.card,
            text_color=COLORS.text_dark,
            border_color=COLORS.border,
            width=60,
            validate="key",
            validatecommand=(validate_command, "%P")
        )
        max_entry.grid(row=0, column=2, padx=(0, 5), pady=2)

        ctk.CTkLabel(range_frame, text="máx", text_color=COLORS.text_dark).grid(row=0, column=3)

        return min_entry, max_entry

    def save_settings(self):
        # Mostrar confirmación al usuario
        msg = CTkMessagebox(title="Confirmación", message="¿Estás seguro de guardar los valores?",
                            icon="question", option_1="Sí", option_2="No")

        def clean(val):
            return val.lstrip("0").replace(",", ".").strip()

        def is_float(val):
            try:
                float(clean(val))
                return True
            except Exception:
                return False

        if msg.get() == "Sí":
            # Validar que todos los campos sean numéricos o vacíos
            campos = [
                self.ph_min_entry.get(), self.ph_max_entry.get(),
                self.temp_min_entry.get(), self.temp_max_entry.get(),
                self.ec_min_entry.get(), self.ec_max_entry.get()
            ]
            if not all(is_float(c) or c == "" for c in campos):
                self.status_label.configure(text="❌ Todos los valores deben ser numéricos")
                self.status_label.after(3000, lambda: self.status_label.configure(text=""))
                return

            self.settings = {
                "pH": {
                    "min": clean(self.ph_min_entry.get()),
                    "max": clean(self.ph_max_entry.get())
                },
                "Temperatura": {
                    "min": clean(self.temp_min_entry.get()),
                    "max": clean(self.temp_max_entry.get())
                },
                "EC": {
                    "min": clean(self.ec_min_entry.get()),
                    "max": clean(self.ec_max_entry.get())
                }
            }
            print("Guardado:", self.settings)
            self.status_label.configure(text="Configuración guardada correctamente ✅")
            self.status_label.after(3000, lambda: self.status_label.configure(text=""))
            # Nuevo: notificar a quien corresponda
            if self.on_settings_saved:
                self.on_settings_saved(self.settings)
        else:
            self.status_label.configure(text="Guardado cancelado ❌")
            self.status_label.after(3000, lambda: self.status_label.configure(text=""))

    def toggle_light(self):
        print("Lámpara encendida/apagada")

    def change_spectrum(self):
        print("Espectro de luz cambiado")

    def adjust_intensity(self):
        print("Intensidad ajustada")

    # Validación para formato x.x (como 6.5)
    def validate_ph_format(self, value):
        if value == "":
            return True
        pattern = r"^\d{0,1}(\.\d{0,1})?$"  # un dígito, opcionalmente un punto y un dígito
        return bool(re.fullmatch(pattern, value))

    # Validación para máximo dos dígitos enteros
    def validate_two_digits(self, value):
        if value == "":
            return True
        return value.isdigit() and len(value) <= 2
