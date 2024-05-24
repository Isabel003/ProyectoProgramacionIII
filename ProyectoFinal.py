# Librerias para la conexion a Azure
import pypyodbc as odbc #pip install pypyobdc
import pandas as pd #pip install pandas
# Librerias para la interfaz
import tkinter as tk
from tkinter import messagebox
import serial
from serial.tools.list_ports import comports
from tkinter import *
from tkinter import Button
# Lectura del puerto en tiempo real
import threading
import time
# Librerias para conexion SQL

import mysql.connector #SQL

def leer_serial(puerto):
    # Configurar la conexión serial
    try:
        # ciclo de conexion
        while True:
            # esperar a conexion
            if puerto.in_waiting > 0:
                # leer consola y puerto
                consola = puerto.readline().decode('utf-8').rstrip()
                # Impresion de consola
                print(consola)
                # Guardar consola
                guardar(consola)
    # Errores del usuario, IDE Arduino o SQL
    except serial.SerialException as e:
        print(f"Error abriendo el puerto serial: {e}")
        guardar(f"Error abriendo el puerto serial: {e}")
    except KeyboardInterrupt:
        print(f"Comunicación interrumpida...")
        guardar(f"Comunicación interrumpida...")
    finally:
        if puerto.is_open:
            puerto.close()
            print(f"Puerto serial cerrado")
            guardar(f"Puerto serial cerrado")

# Conexion a SQL local
conexion = mysql.connector.connect(user = 'root', 
                                   password = 'server', 
                                   host ='localhost', 
                                   database = 'proyecto', 
                                   port = '3306')
print(conexion)
# Lectura de cada linea de la terminal
cursor = conexion.cursor()
# Comunicacion del terminal hacia SQL
cursor.execute
(
    '''
        CREATE TABLE IF NOT EXISTS datos_serial
        (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Mensaje_Serial LONGTEXT,
            Tiempo TIMESTAMP DEFAULT CURRENT TIMESTAMP
        )
    '''
)
# Funcion guardar en SQL
def guardar(Mensaje_Serial):
    try:
        conexion = mysql.connector.connect(user = 'root', 
                                   password = 'server', 
                                   host ='localhost', 
                                   database = 'proyecto', 
                                   port = '3306'
        )
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO datos_serial (Mensaje_Serial) VALUES (%s)', (Mensaje_Serial,))
        conexion.commit()    
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
    finally:
        cursor.close()
        conexion.close()

# Número inicial de parqueos disponibles
parking_slots = 4
max_slots = 4  # Máximo número de parqueos disponibles

# Función para leer desde el puerto serial
def read_from_serial():
    global parking_slots
    while True:
        try:
            if puerto.in_waiting > 0:
                line = puerto.readline().decode().strip()
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
            break

# Función para actualizar el texto de la etiqueta en la interfaz gráfica
def update_label(text):
    label.config(text=text)

# Función para mostrar mensaje de no hay parqueos
def show_no_parking_message():
    messagebox.showwarning("Parqueo lleno", "No hay parqueos disponibles.")

# Función para cerrar correctamente el puerto serial al cerrar la ventana
def on_closing():
    if puerto.is_open:
        puerto.close()
    root.destroy()

# Función para abrir la talanquera
def open_talanquera():
    global parking_slots
    if puerto.is_open:
        if parking_slots > 0:
            puerto.write(b'8\n')  # Enviar el comando para abrir la talanquera
            parking_slots -= 1
            update_label(f"Parqueos disponibles: {parking_slots}")
        else:
            show_no_parking_message()

# Función para cerrar la talanquera
def close_talanquera():
    global parking_slots
    if puerto.is_open:
        puerto.write(b'9\n')  # Enviar el comando para cerrar la talanquera
        if parking_slots < max_slots:
            parking_slots += 1
            update_label(f"Parqueos disponibles: {parking_slots}")

puerto = None
try:
    puerto = serial.Serial('COM7', 9600, timeout=1)
    print(f"Conectado a: {'COM7'}")
    time.sleep(2)

    lectura = threading.Thread(target= leer_serial, args=(puerto,))
    lectura.daemon = True
    lectura.start()
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

        # Manejar el cierre de la ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)

        # Iniciar el loop de tkinter
    root.mainloop()

except serial.SerialException as e:
    print(f"Error al abrir el puerto: {e}")
except KeyboardInterrupt:
    print("Comunicación interrumpida...")
finally:
    if puerto and puerto.is_open:
        puerto.close()
        print("Puerto serial cerrado")
    cursor.close()
    conexion.close()