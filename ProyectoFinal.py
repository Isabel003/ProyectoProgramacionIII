# Librerias para la conexion a Azure
import pypyodbc as odbc #pip install pypyobdc
import pyodbc as py
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

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------


# Librerias para conexion SQL
import mysql.connector #SQL
"""
server = 'progra3.database.windows.net' #conexion a servidor
database = 'PARQUEO' #conexion a base de datos
connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:progra3.database.windows.net,1433;Database=PARQUEO;Uid=jona1;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;' 
#link a la conexion
conn = odbc.connect(connection_string)
#objeto de conexion a azure

"""
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
    interfaz.destroy()

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
    interfaz = tk.Tk()
    interfaz.config(width=1000, height=1000, background= "dim gray")
    interfaz.title("Proyecto Programación III")


    title_label = tk.Label(interfaz, text="Sistema de Gestión de Parqueos", font=("Helvetica", 20, "bold"), background="dim gray")
    title_label.place(x=100, y= 50)
    title_label = tk.Label(interfaz, text="Grupo #6", font=("Helvetica", 18))
    title_label.place(x=100, y=100)

    if(parking_slots>0):
        label = tk.Label(interfaz, text=f"Parqueos disponibles: {parking_slots}", font=("Helvetica", 18), background="spring green")
        label.place(x=600, y=200)
    if(parking_slots <1):
        label = tk.Label(interfaz, text=f"Parqueos disponibles: {parking_slots}", font=("Helvetica", 18), background="red")
        label.place(x=600, y=200)

    title_label = tk.Label(interfaz, text="Control Manual", font=("Helvetica", 16, "bold"), background="khaki")
    title_label.place(x=100, y=400)


        # Añadir botones para abrir y cerrar la talanquera
    open_button = tk.Button(interfaz, text="", command=open_talanquera, font=("Helvetica", 14), background="lawn green")
    open_button.place(x=100, y=450)
    entrada_label = tk.Label(interfaz, text = f"Entrada", font=("Helvetica", 14), background="dim gray")
    entrada_label.place(x=75, y=475)

    close_button = tk.Button(interfaz, text="", command=close_talanquera, font=("Helvetica", 14), background="red")
    close_button.place(x=200, y=450)
    salida_label = tk.Label(interfaz, text = f"Salida", font=("Helvetica", 14), background="dim gray")
    salida_label.place(x=200, y=475)
    #Diseño de parqueo animado
    
    canvas = tk.Canvas(interfaz, width=500, height=500, bg='dim gray')
    canvas.pack()
    canvas.place(x=400, y= 300)
   
    # Dibujar un rectángulo
    
    # Dibujar un cuadrado
    canvas.create_rectangle(50, 50, 150, 150, fill='green', outline='dim gray')
    canvas.create_rectangle(200, 50, 300, 150, fill='green', outline='dim gray')
    canvas.create_rectangle(350, 50, 450, 150, fill='green', outline='dim gray')
    canvas.create_rectangle(350, 200, 450, 300, fill='green', outline='dim gray')
    canvas.create_rectangle(450, 200, 200, 200, fill='orange', outline='dim gray')

     # Dibujar flechas
    canvas.create_line(50, 200, 200, 200, arrow=tk.LAST, fill='yellow', width=3)
    canvas.create_line(50, 250, 200, 250, arrow=tk.LAST, fill='yellow', width=3)
        # Manejar el cierre de la ventana
    interfaz.protocol("WM_DELETE_WINDOW", on_closing)

        # Iniciar el loop de tkinter
    interfaz.mainloop()

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