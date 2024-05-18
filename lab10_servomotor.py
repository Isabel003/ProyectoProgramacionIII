#librerias a utilizar
import serial
from serial.tools.list_ports import comports
from time import sleep
from tkinter import *
from tkinter import Button
import tkinter as tk
import threading

import time
import mysql.connector #SQL

# ---------------------------------------------------------------------
#Funcion comunicacion entre el puerto
def leer_serial(puerto):
    #try except para errores
    try:
        #ciclo de conexcion
        while True:
            #espera a conexion
            if puerto.in_waiting > 0:
                #leer consola y puerto
                consola = puerto.readline().decode('utf-8').rstrip()
                print(consola)                      #ordenar los datos
                guardar(consola) #Guardar mensaje en BD
    except serial.SerialException as e:
        #primer error
        print(f"Error al abrir el puerto: {e}")
        guardar(f"Error al abrir el puerto: {e}") #Guardar mensaje en BD
    except KeyboardInterrupt:
        #segundo error
        print(f"Comunicación interrumpida...")
        guardar(f"Comunicación interrumpida...") #Guardar mensaje en BD
    finally:
        #cierre de conexion
        if puerto.is_open:
            puerto.close()
            print(f"Puerto serial cerrado")
            guardar(f"Puerto serial cerrado") #Guardar mensaje en BD
# ----------------------------------------------------------------------- 

    #Funciones para TK.KINTER e interfaz
def BOTON_IZQUIERDA():
     puerto.write('0'.encode())

def BOTON_DERECHA():
     puerto.write('1'.encode())

# ----------------------------------------------------------------------- 

    #Enlace a la base de datos
conexion = mysql.connector.connect(user = 'root', 
                                password = 'server', 
                                host = 'localhost', 
                                database = 'lab10', 
                                port = '3306')
print(conexion)
''' 

    Variable para el enlace de BD
        funcion connect
                Terminos de la conexion, como el usuario, contraseña, puerto y nombre de la base

'''
#Crear objeto de la conexion a SQL
cursor = conexion.cursor()
#Objeto cursor para crear una tabla
cursor.execute
(
    '''
        CREATE TABLE IF NOT EXISTS datos_serial 
        (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            mensaje VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''     
)
#Guardar datos SERIAL a SQL

def guardar(Mensaje_Serial):
    try:
        #Enlace a la base de datos
        conexion = mysql.connector.connect(user = 'root', 
                                password = 'server', 
                                host = 'localhost', 
                                database = 'lab10', 
                                port = '3306'
        )

        cursor = conexion.cursor()
        #ORDEN DE GUARDAR CADA DATO DESDE EL PRINCIPIO AL FINAL
        cursor.execute('INSERT INTO datos_serial (Mensaje_Serial) VALUES (%s)', (Mensaje_Serial,))
        #funcion commit para guardar cambios
        conexion.commit()
    except mysql.connector.Error as err:
         print(f"Error al conectar a la base de datos: {err}")
    finally:
         cursor.close()
         conexion.close()

# ----------------------------------------------------------------------- 

#INICIO
    #crear el puerto
puerto = None 
try:
    #caracteristicas del puerto
    puerto = serial.Serial('COM7', 9600, timeout=1)
    print(f"Conectado a: {'COM7'}")
    time.sleep(2)

    # Lectura del puerto serial
    lectura = threading.Thread(target=leer_serial, args=(puerto,))
    lectura.daemon = True
    lectura.start()

    # Inicializar Tkinter
    interfaz = tk.Tk()
    interfaz.title("SERVO MOTOR SG90")
    interfaz.config(width=400, height=500, background="lemon chiffon")
        #titulo de la ventana flotante
    title = Label (text= " SERVO MOTOR ", background= "light cyan", foreground="black", font=("Arial", 20))
    title.place(x=100, y=20)
        #Creacion de botones en la interfaz
    Boton_L = tk.Button(text="Izquierda", width="10", height="25", command=BOTON_IZQUIERDA, background="misty rose")
    Boton_L.place(x=110, y=100)

    Boton_L = tk.Button(text="Derecha", width="10", height="25", command=BOTON_DERECHA, background="light blue")
    Boton_L.place(x=210, y=100)

    # Mantener la ventana abierta
    interfaz.mainloop()

#Errores except del usuario al iniciar el programa
except serial.SerialException as e:
        print(f"Error al abrir el puerto: {e}")
except KeyboardInterrupt:
        print("Comunicación interrumpida...")
finally:
    if puerto and puerto.is_open:
        #Fin de la comunicacion serial
        puerto.close()
        print("Puerto serial cerrado")
    cursor.close()#Cerrar cambios en BD
    conexion.close()#Cerrar conexion a BD