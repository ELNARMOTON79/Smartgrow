import customtkinter as ctk
import serial
import threading

# --- CONFIGURACIÓN DEL PUERTO SERIAL ---
SERIAL_PORT = "COM11"  # Cambia esto según tu sistema (ej: '/dev/ttyUSB0' en Linux)
BAUD_RATE = 9600

# --- App GUI ---
class SensorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Monitor de Sensores Hidropónicos")
        self.geometry("400x350")
        ctk.set_appearance_mode("dark")

        # --- Etiquetas ---
        self.nivel_label = ctk.CTkLabel(self, text="💧 Nivel de agua: --- cm", font=("Arial", 16))
        self.nivel_label.pack(pady=10)

        self.distancia_label = ctk.CTkLabel(self, text="📏 Distancia: --- cm", font=("Arial", 16))
        self.distancia_label.pack(pady=10)

        self.temperatura_label = ctk.CTkLabel(self, text="🌡️ Temperatura: --- °C", font=("Arial", 16))
        self.temperatura_label.pack(pady=10)

        self.ec_label = ctk.CTkLabel(self, text="⚡ EC: --- mS/cm", font=("Arial", 16))
        self.ec_label.pack(pady=10)

        self.voltaje_label = ctk.CTkLabel(self, text="🔋 Voltaje: --- V", font=("Arial", 16))
        self.voltaje_label.pack(pady=10)

        self.alert_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 15, "bold"))
        self.alert_label.pack(pady=10)

        # --- Serial ---
        self.serial_connection = None
        self.start_serial_thread()

    def start_serial_thread(self):
        try:
            self.serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            threading.Thread(target=self.read_serial_data, daemon=True).start()
        except Exception as e:
            self.alert_label.configure(text=f"⚠️ Error al conectar: {e}")

    def read_serial_data(self):
        buffer = ""
        while True:
            try:
                line = self.serial_connection.readline().decode("utf-8").strip()
                if not line:
                    continue

                # Acumulamos líneas
                buffer += line + "\n"

                # Esperamos bloque completo (con '-----' al final)
                if "-----" in buffer:
                    self.parse_data(buffer)
                    buffer = ""

            except Exception as e:
                self.alert_label.configure(text=f"⚠️ Error: {e}")

    def parse_data(self, data):
        lines = data.strip().splitlines()
        for line in lines:
            if "Nivel_agua:" in line or "💧 Nivel de agua:" in line:
                nivel = ''.join(c for c in line if c.isdigit() or c == '.' or c == ',')
                self.nivel_label.configure(text=f"💧 Nivel de agua: {nivel} cm")
            elif "Distancia al agua:" in line:
                distancia = ''.join(c for c in line if c.isdigit() or c == '.' or c == ',')
                self.distancia_label.configure(text=f"📏 Distancia: {distancia} cm")
            elif "Temperatura" in line:
                temp = ''.join(c for c in line if c.isdigit() or c == '.' or c == ',')
                self.temperatura_label.configure(text=f"🌡️ Temperatura: {temp} °C")
            elif "EC:" in line or "Conductividad" in line:
                ec = ''.join(c for c in line if c.isdigit() or c == '.' or c == ',')
                self.ec_label.configure(text=f"⚡ EC: {ec} mS/cm")
            elif "Voltaje" in line:
                volt = ''.join(c for c in line if c.isdigit() or c == '.' or c == ',')
                self.voltaje_label.configure(text=f"🔋 Voltaje: {volt} V")
            elif "¡Nivel bajo!" in line or "❌" in line:
                self.alert_label.configure(text="⚠️ ¡Nivel de agua bajo!")
            else:
                self.alert_label.configure(text="")  # Limpia si no hay alerta

if __name__ == "__main__":
    app = SensorApp()
    app.mainloop()
