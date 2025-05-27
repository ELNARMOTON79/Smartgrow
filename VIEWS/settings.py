import customtkinter as ctk
from VIEWS.colors import COLORS
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
            self.frame, text="⚙️ Settings", font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS.text_dark
        ).pack(pady=20)

        content = ctk.CTkFrame(self.frame, fg_color=COLORS.background, corner_radius=10)
        content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # --- Etiquetas con signo de interrogación y ayuda ---
        label_frame_ph = ctk.CTkFrame(content, fg_color=COLORS.background)
        label_frame_ph.pack(pady=(10, 0))
        ctk.CTkLabel(
            label_frame_ph,
            text="🧪 pH ideal:",
            text_color=COLORS.text_dark,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        ctk.CTkButton(
            label_frame_ph, text="❓", width=28, height=28, fg_color=COLORS.primary, text_color="white",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda: self.show_help("ph")
        ).pack(side="left", padx=(5, 0))

        self.ph_min_entry, self.ph_max_entry = self._create_labeled_range(content, "", self.vcmd_ph)

        label_frame_temp = ctk.CTkFrame(content, fg_color=COLORS.background)
        label_frame_temp.pack(pady=(10, 0))
        ctk.CTkLabel(
            label_frame_temp,
            text="🌡️ Temperatura ideal (°C):",
            text_color=COLORS.text_dark,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        ctk.CTkButton(
            label_frame_temp, text="❓", width=28, height=28, fg_color=COLORS.primary, text_color="white",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda: self.show_help("temperatura")
        ).pack(side="left", padx=(5, 0))

        self.temp_min_entry, self.temp_max_entry = self._create_labeled_range(content, "", self.vcmd_2digit)

        label_frame_ec = ctk.CTkFrame(content, fg_color=COLORS.background)
        label_frame_ec.pack(pady=(10, 0))
        ctk.CTkLabel(
            label_frame_ec,
            text="⚡ Electroconductividad ideal (μS/cm):",
            text_color=COLORS.text_dark,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        ctk.CTkButton(
            label_frame_ec, text="❓", width=28, height=28, fg_color=COLORS.primary, text_color="white",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda: self.show_help("ec")
        ).pack(side="left", padx=(5, 0))

        self.ec_min_entry, self.ec_max_entry = self._create_labeled_range(content, "", self.vcmd_2digit)

        # Botón de guardar
        save_btn = ctk.CTkButton(
            content, text="Guardar", fg_color=COLORS.primary, hover_color=COLORS.secondary,
            text_color="white", command=self.save_settings, font=ctk.CTkFont(size=18, weight="bold"), height=40
        )
        save_btn.pack(pady=10)

        # Etiqueta para mostrar confirmación
        self.status_label = ctk.CTkLabel(content, text="", text_color=COLORS.text_dark, font=ctk.CTkFont(size=16, weight="bold"))
        self.status_label.pack()

        # Botones de control
        btn_frame = ctk.CTkFrame(content, fg_color=COLORS.background)
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="Encender Lámpara", fg_color=COLORS.secondary,
            text_color="white", command=self.toggle_light, font=ctk.CTkFont(size=16, weight="bold"), height=38
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame, text="Cambiar Espectro", fg_color=COLORS.primary,
            text_color="white", command=self.change_spectrum, font=ctk.CTkFont(size=16, weight="bold"), height=38
        ).pack(side="left", padx=5)

        ctk.CTkButton(
                btn_frame, text="Ajustar Intensidad", fg_color=COLORS.button_intensity,  # Cambiado a azul claro
                text_color="white", command=self.adjust_intensity
        ).pack(side="left", padx=5)

    def _create_labeled_range(self, parent, label, validate_command):
        container = ctk.CTkFrame(parent, fg_color=COLORS.background)
        container.pack(pady=5)

        ctk.CTkLabel(container, text=label, text_color=COLORS.text_dark, font=ctk.CTkFont(size=16)).pack(anchor="center", pady=(0, 2))

        range_frame = ctk.CTkFrame(container, fg_color=COLORS.background)
        range_frame.pack()

        min_entry = ctk.CTkEntry(
            range_frame,
            fg_color=COLORS.card,
            text_color=COLORS.text_dark,
            border_color=COLORS.border,
            width=70,
            font=ctk.CTkFont(size=16),
            validate="key",
            validatecommand=(validate_command, "%P")
        )
        min_entry.grid(row=0, column=0, padx=(0, 5), pady=2)

        ctk.CTkLabel(range_frame, text="mín", text_color=COLORS.text_dark, font=ctk.CTkFont(size=14)).grid(row=0, column=1, padx=(0, 15))

        max_entry = ctk.CTkEntry(
            range_frame,
            fg_color=COLORS.card,
            text_color=COLORS.text_dark,
            border_color=COLORS.border,
            width=70,
            font=ctk.CTkFont(size=16),
            validate="key",
            validatecommand=(validate_command, "%P")
        )
        max_entry.grid(row=0, column=2, padx=(0, 5), pady=2)

        ctk.CTkLabel(range_frame, text="máx", text_color=COLORS.text_dark, font=ctk.CTkFont(size=14)).grid(row=0, column=3)

        return min_entry, max_entry

    def save_settings(self):
        # Mostrar confirmación al usuario con un modal personalizado
        response = self.show_modal(
            title="Confirmación",
            message="¿Estás seguro de guardar los valores?",
            icon="question",
            buttons=["Sí", "No"]
        )

        def clean(val):
            return val.lstrip("0").replace(",", ".").strip()

        def is_float(val):
            try:
                float(clean(val))
                return True
            except Exception:
                return False

        if response == "Sí":
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

    def show_help(self, key):
        help_texts = {
            "ph": "Un pH entre 6.0 y 6.5 es ideal para la absorción de nutrientes. Valores menores a 5.5 pueden causar deficiencias de calcio, magnesio y fósforo",
            "temperatura": "Día: entre 20°C y 25°C\nNoche: entre 15°C y 18°C.",
            "ec": "Entre 1.0 y 2.5 mS/cm (milisiemens por centímetro)",
        }

        help_icons = {
            "ph": "🧪",
            "temperatura": "🌡️",
            "ec": "⚡",
        }
        # Ajusta el tamaño de letra solo para temperatura
        font_size = 16 if key == "temperatura" else 20
        self.show_modal(
            title="Valores ideales",
            message=help_texts.get(key, "Sin información disponible."),
            icon=help_icons.get(key, "info"),
            buttons=["Cerrar"],
            msg_font_size=font_size
        )

    def show_modal(self, title, message, icon=None, buttons=["Cerrar"], msg_font_size=20):
        """Muestra un modal personalizado y retorna el texto del botón presionado."""
        modal = ctk.CTkToplevel(self.frame)
        modal.title(title)
        modal.geometry("440x200")
        modal.resizable(False, False)
        modal.grab_set()

        # Centrar modal respecto al padre
        modal.update_idletasks()
        x = self.frame.winfo_rootx() + (self.frame.winfo_width() // 2) - (modal.winfo_width() // 2)
        y = self.frame.winfo_rooty() + (self.frame.winfo_height() // 2) - (modal.winfo_height() // 2)
        modal.geometry(f"+{x}+{y}")

        content = ctk.CTkFrame(modal, fg_color=COLORS.background, corner_radius=10)
        content.pack(fill="both", expand=True, padx=10, pady=10)

        row = ctk.CTkFrame(content, fg_color="transparent")
        row.pack(fill="x", pady=(10, 0), padx=10)

        # Icono
        icon_map = {
            "🧪": ("🧪", "#10b981"),
            "🌡️": ("🌡️", "#f59e42"),
            "⚡": ("⚡", "#6366f1"),
            "info": ("🛈", "#2563eb"),
            "question": ("❓", "#f59e0b"),
        }
        icon_char, icon_color = icon_map.get(icon, ("🧪", "#10b981"))
        icon_label = ctk.CTkLabel(row, text=icon_char, font=ctk.CTkFont(size=48, weight="bold"), text_color=icon_color)
        icon_label.pack(side="left", padx=(0, 18))

        msg = ctk.CTkLabel(
            row, text=message,
            font=ctk.CTkFont(size=msg_font_size, weight="bold"),
            text_color=COLORS.text_dark,
            wraplength=320,
            justify="left"
        )
        msg.pack(side="left", fill="x", expand=True)

        # Botones
        result = {"value": None}
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=(20, 10))
        def set_result(val):
            result["value"] = val
            modal.destroy()
        for b in buttons:
            ctk.CTkButton(
                btn_frame, text=b, command=lambda v=b: set_result(v),
                width=140, height=44, font=ctk.CTkFont(size=18, weight="bold")
            ).pack(side="left", padx=12)
        btn_frame.focus_set()
        modal.transient(self.frame)
        modal.wait_window()
        return result["value"]
