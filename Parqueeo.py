import tkinter as tk
from tkinter import messagebox
import serial
import threading

# Configurar la conexión serial
try:
    ser = serial.Serial('COM3', 9600)  # Asegúrate de que el puerto COM sea correcto
except serial.SerialException as e:
    print(f"Error abriendo el puerto serial: {e}")
    exit()

# Número inicial de parqueos disponibles
parking_slots = 4
max_slots = 4  # Máximo número de parqueos disponibles

# Función para leer desde el puerto serial
def read_from_serial():
    global parking_slots
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line == '1':
                    if parking_slots > 0:
                        parking_slots -= 1
                        update_label(f"Parqueos disponibles: {parking_slots}")
                    else:
                        show_no_parking_message()
                elif line == '2':
                    if parking_slots < max_slots:
                        parking_slots += 1
                        update_label(f"Parqueos disponibles: {parking_slots}")
        except serial.SerialException as e:
            print(f"Error leyendo desde el puerto serial: {e}")
            break

# Función para actualizar el texto de la etiqueta en la interfaz gráfica
def update_label(text):
    label.config(text=text)

# Función para mostrar mensaje de no hay parqueos
def show_no_parking_message():
    messagebox.showwarning("Parqueo lleno", "No hay parqueos disponibles.")

# Función para cerrar correctamente el puerto serial al cerrar la ventana
def on_closing():
    if ser.is_open:
        ser.close()
    root.destroy()

# Función para abrir la talanquera
def open_talanquera():
    global parking_slots
    if ser.is_open:
        if parking_slots > 0:
            ser.write(b'8\n')  # Enviar el comando para abrir la talanquera
            parking_slots -= 1
            update_label(f"Parqueos disponibles: {parking_slots}")
        else:
            show_no_parking_message()

# Función para cerrar la talanquera
def close_talanquera():
    global parking_slots
    if ser.is_open:
        ser.write(b'9\n')  # Enviar el comando para cerrar la talanquera
        if parking_slots < max_slots:
            parking_slots += 1
            update_label(f"Parqueos disponibles: {parking_slots}")

# Configurar la ventana de tkinter
root = tk.Tk()
root.title("Sistema de Parqueos")


title_label = tk.Label(root, text="Sistema de Gestión de Parqueos", font=("Helvetica", 18, "bold"))
title_label.pack(pady=30)
title_label = tk.Label(root, text="Grupo #6 , Programación III", font=("Helvetica", 14))
title_label.pack(pady=0)

label = tk.Label(root, text=f"Parqueos disponibles: {parking_slots}", font=("Helvetica", 16))
label.pack(pady=30)

title_label = tk.Label(root, text="Control Manual", font=("Helvetica", 14, "bold"))
title_label.pack(pady=0)


# Añadir botones para abrir y cerrar la talanquera
open_button = tk.Button(root, text="Entrada", command=open_talanquera, font=("Helvetica", 14))
open_button.pack(pady=10)

close_button = tk.Button(root, text="Salida", command=close_talanquera, font=("Helvetica", 14))
close_button.pack(pady=10)

# Crear un hilo para leer desde el puerto serial
thread = threading.Thread(target=read_from_serial)
thread.daemon = True
thread.start()

# Manejar el cierre de la ventana
root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar el loop de tkinter
root.mainloop()
