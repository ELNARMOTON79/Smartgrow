from customtkinter import *

class Configuracion(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Crear un frame principal para contener las métricas
        self.main_frame = CTkFrame(self, fg_color="#E8F5E9")  # Fondo verde claro
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Contenedor centrado
        self.content_frame = CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(expand=True)

        # Título
        self.title_label = CTkLabel(self.content_frame, text="Settings", font=("Arial", 24, "bold"), text_color="#32909C")
        self.title_label.pack(pady=(20, 30))  # Espaciado superior

        # Campo de temperatura ideal
        self.temp_label = CTkLabel(self.content_frame, text="Ideal temperature:", text_color="black", font=("Arial", 16))
        self.temp_label.pack()
        self.temp_entry = CTkEntry(self.content_frame, width=200, height=35)
        self.temp_entry.pack(pady=10)

        # Campo de pH adecuado
        self.ph_label = CTkLabel(self.content_frame, text="pH appropriate:", text_color="black", font=("Arial", 16))
        self.ph_label.pack()
        self.ph_entry = CTkEntry(self.content_frame, width=200, height=35)
        self.ph_entry.pack(pady=10)

        # Interruptor de luces LED
        self.led_label = CTkLabel(self.content_frame, text="Led lights", text_color="black", font=("Arial", 16))
        self.led_label.pack()
        self.led_switch = CTkSwitch(self.content_frame, text="")
        self.led_switch.pack(pady=10)

        # Control de intensidad
        self.intensity_label = CTkLabel(self.content_frame, text="Intensity", text_color="black", font=("Arial", 16))
        self.intensity_label.pack()
        self.intensity_slider = CTkSlider(self.content_frame, from_=0, to=100, width=250)
        self.intensity_slider.pack(pady=20)

if __name__ == "__main__":
    app = CTk()
    app.title("SmartGrow - Hydroponic System")
    app.geometry("900x700")

    config_frame = Configuracion(app)
    config_frame.pack(fill="both", expand=True)

    app.mainloop()