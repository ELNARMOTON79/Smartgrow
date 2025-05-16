import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import time

# Configura aquí el puerto y baudrate que usa tu Arduino
PUERTO_SERIAL = 'COM11'  # Cambia esto según tu sistema (ej. '/dev/ttyUSB0' en Linux)
BAUDRATE = 9600

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor EC y Temperatura")

        # Variables de sensores
        self.volt_var = tk.StringVar(value="---")
        self.ec_var = tk.StringVar(value="---")
        self.temp_var = tk.StringVar(value="---")

        # Serial
        self.serial_connected = False
        try:
            self.ser = serial.Serial(PUERTO_SERIAL, BAUDRATE, timeout=1)
            self.serial_connected = True
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar al puerto {PUERTO_SERIAL}\n{e}")
            return

        # UI
        self.create_widgets()

        # Hilo para leer datos
        self.running = True
        threading.Thread(target=self.read_serial, daemon=True).start()

    def create_widgets(self):
        ttk.Label(self.root, text="Voltaje (V):").grid(row=0, column=0, sticky="e")
        ttk.Label(self.root, textvariable=self.volt_var).grid(row=0, column=1)

        ttk.Label(self.root, text="Conductividad (mS/cm):").grid(row=1, column=0, sticky="e")
        ttk.Label(self.root, textvariable=self.ec_var).grid(row=1, column=1)

        ttk.Label(self.root, text="Temperatura (°C):").grid(row=2, column=0, sticky="e")
        ttk.Label(self.root, textvariable=self.temp_var).grid(row=2, column=1)

        ttk.Label(self.root, text="").grid(row=3, column=0)

        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Encender/Apagar (A)", command=lambda: self.send_command('A')).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Cambiar Espectro (B)", command=lambda: self.send_command('B')).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Cambiar Intensidad (C)", command=lambda: self.send_command('C')).grid(row=0, column=2, padx=5)

    def send_command(self, command):
        if self.serial_connected:
            try:
                self.ser.write(command.encode())
            except:
                messagebox.showerror("Error", "Fallo al enviar comando.")

    def read_serial(self):
        buffer = ""
        while self.running and self.serial_connected:
            try:
                if self.ser.in_waiting:
                    char = self.ser.read().decode(errors='ignore')
                    if char == '\n':
                        self.parse_line(buffer.strip())
                        buffer = ""
                    else:
                        buffer += char
            except:
                continue
            time.sleep(0.1)

    def parse_line(self, line):
        # Ejemplo de línea: "Voltaje: 2.56 V Conductividad: 1.23 mS/cm"
        if "Voltaje" in line and "Conductividad" in line:
            try:
                parts = line.split()
                volt = parts[1]
                ec = parts[4]
                self.volt_var.set(volt)
                self.ec_var.set(ec)
            except:
                pass
        elif "Temperatura=" in line:
            try:
                temp = line.split('=')[1].split()[0]
                self.temp_var.set(temp)
            except:
                pass

    def close(self):
        self.running = False
        if self.serial_connected:
            self.ser.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
