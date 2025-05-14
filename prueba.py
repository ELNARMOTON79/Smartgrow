import serial
import threading
import tkinter as tk
from tkinter import ttk

SERIAL_PORT = 'COM8'  # Cambia esto a tu puerto
BAUD_RATE = 9600

root = tk.Tk() 
root.title("Sistema Hidropónico")
root.geometry("500x500")

temperature_var = tk.StringVar(value="--")
distance_var = tk.StringVar(value="--")
ec_var = tk.StringVar(value="--")
ph_var = tk.StringVar(value="--")
intensity_var = tk.StringVar(value="--")
water_status = tk.StringVar(value="OFF")
peri_status = tk.StringVar(value="OFF")

# Datos en pantalla
labels = [
    ("Temperatura (°C)", temperature_var),
    ("Distancia (cm)", distance_var),
    ("Conductividad (EC)", ec_var),
    ("pH", ph_var),
    ("Intensidad de Luz", intensity_var),
    ("Bomba Agua", water_status),
    ("Bomba Peristáltica", peri_status)
]

for text, var in labels:
    ttk.Label(root, text=text + ":").pack(pady=(5, 0))
    ttk.Label(root, textvariable=var, font=("Arial", 12)).pack()

ser = None

def send_command(command):
    if ser and ser.is_open:
        ser.write((command + '\n').encode())

# Controles de luz
ttk.Label(root, text="Controles de Luz").pack(pady=10)
btn_frame = ttk.Frame(root)
btn_frame.pack()

ttk.Button(btn_frame, text="Encender/Apagar Luz", command=lambda: send_command("BTN1")).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(btn_frame, text="Cambiar Espectro", command=lambda: send_command("BTN2")).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(btn_frame, text="Cambiar Intensidad", command=lambda: send_command("BTN3")).grid(row=1, column=0, columnspan=2, pady=5)

# Controles de bombas
ttk.Label(root, text="Controles de Bombas").pack(pady=10)
pump_frame = ttk.Frame(root)
pump_frame.pack()

ttk.Button(pump_frame, text="Bomba de Agua", command=lambda: send_command("WATER")).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(pump_frame, text="Bomba Peristáltica", command=lambda: send_command("PERISTALTIC")).grid(row=0, column=1, padx=10, pady=5)

# Lectura del serial en segundo plano
def read_serial():
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    data = dict(item.split(":") for item in line.split(","))
                    temperature_var.set(data.get("TEMP", "--"))
                    distance_var.set(data.get("DIST", "--"))
                    ec_var.set(data.get("EC", "--"))
                    ph_var.set(data.get("PH", "--"))
                    intensity_var.set(data.get("INTENSITY", "--"))
                    water_status.set(data.get("WATER", "--"))
                    peri_status.set(data.get("PERI", "--"))
                except Exception as e:
                    print("Error procesando datos:", e)
    except serial.SerialException as e:
        print("Error abriendo puerto:", e)

threading.Thread(target=read_serial, daemon=True).start()

root.mainloop()
