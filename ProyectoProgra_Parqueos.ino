//Librerias a usar
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

//Direccion del display lcd
LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo myservo;

const int IR1 = 2; // Sensor de entrada
const int IR2 = 3; // Sensor de salida
int Slot = 4;      // Número total de espacios de estacionamiento

int flag1 = 0;// Posicion del servo motor
int flag2 = 0;//Posicion del servo motor

int monitor; //Monitor serial
void setup() 
{
  Serial.begin(9600);
  lcd.init(); // Inicializar el LCD
  lcd.backlight(); // Enciende la retroiluminación
  
  pinMode(IR1, INPUT); // Pin del sensor de entrada
  pinMode(IR2, INPUT); // Pin del sensor de salida

  myservo.attach(4); // Cambia el pin del servo si es necesario
  myservo.write(100); // Posición inicial del servomotor

  lcd.setCursor(0, 0); // Coordenadas iniciales del LCD
  lcd.print("     PROYECTO FINAL   "); // Mensaje inicial
  lcd.setCursor(0, 1); //Posición
  lcd.print(" SISTEMA DE PARQUEO "); // Mensaje
  delay(2000); //Delay
  lcd.clear(); //Limpiar pantalla
}

void loop() 
{
  // Lecturas de sensores y actualización de slots
  bool IR1_state = digitalRead(IR1) == LOW;
  bool IR2_state = digitalRead(IR2) == LOW;
  
  // Comparar estado del servomotor (abierto/cerrado)
  if (IR1_state && flag1 == 0 && flag2 == 0) {//Ambos sensores detectados
    if (Slot > 0) {//Cantidad de parqueos
      flag1 = 1;//Estados del sensor de entrada
      delay(2000); // Delay antes de abrir la barrera
      myservo.write(0); // Abre la barrera
      Slot--;//Disminuir parqueos disponibles
      delay(3000); // Delay para permitir que el coche pase completamente
      myservo.write(100); // Cierra la barrera
      delay(1000); // Pequeño delay después de cerrar la barrera
      flag1 = 0; // Resetea la bandera
      
    } else {
      lcd.setCursor(0, 0);
      lcd.print("    LO SENTIMOS     ");
      lcd.setCursor(0, 1);
      lcd.print("  Parqueo lleno  ");
      delay(3000);
      lcd.clear();
      Serial.println("Parqueo lleno");
    }
  }

  if (IR2_state && flag2 == 0 && flag1 == 0) {
    flag2 = 1;
    delay(2000); // Delay antes de abrir la barrera
    myservo.write(0); // Abre la barrera
    Slot++;
    delay(3000); // Delay para permitir que el coche pase completamente
    myservo.write(100); // Cierra la barrera
    delay(1000); // Pequeño delay después de cerrar la barrera
    flag2 = 0; // Resetea la bandera
  }

  // Verificar si se ha recibido un número a través de la comunicación serial
  if (Serial.available() > 0) {
    int receivedNumber = Serial.parseInt();
    if (receivedNumber == 8) {
      if (Slot > 0) {
        // Abre la barrera cuando se recibe el número 8
        myservo.write(0); // Abre la barrera
        Slot--; // Decrementa el número de espacios disponibles
        delay(3000); // Delay para permitir que el coche pase completamente
        myservo.write(100); // Cierra la barrera
        delay(1000); // Pequeño delay después de cerrar la barrera
      } else {
        lcd.setCursor(0, 0);
        lcd.print("    LO SENTIMOS :(    ");
        lcd.setCursor(0, 1);
        lcd.print("  Parqueo lleno  ");
        delay(3000);
        lcd.clear();
        Serial.println("Parqueo lleno");
        delay(3000);
      }
    } else if (receivedNumber == 9) {
      flag2 = 1;
      delay(2000); // Delay antes de abrir la barrera
      myservo.write(0); // Abre la barrera
      Slot++;
      delay(3000); // Delay para permitir que el coche pase completamente
      myservo.write(100); // Cierra la barrera
      delay(1000); // Pequeño delay después de cerrar la barrera
      flag2 = 0; // Resetea la bandera
    }
  }
//Impresion a SQL
Serial.println("Parqueo abierto");
Serial.print("Espacios disponibles");
Serial.println(Slot);
delay(3000);

  // Actualiza la pantalla LCD
  lcd.setCursor(0, 0);
  lcd.print("    BIENVENIDO   ");
  lcd.setCursor(0, 1);
  lcd.print(" DISPONIBLES: ");
  lcd.print(Slot);
  lcd.print("   ");

}

// Función para escanear dispositivos I2C
void scanI2C() {
  byte error, address;
  int Devices = 0;
  //Serial.println("Buscando...");
  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      //Serial.print("I2C dispositivo no encontrado 0x");
      if (address < 16) Serial.print("0");
      //Serial.print(address, HEX);
      //Serial.println(" !");
      Devices++;
    } else if (error == 4) {
      Serial.print("Error desconocido en direccion 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
    }
  }
  if (Devices == 0) Serial.println("Dispositivo I2C no encontrado\n");
  else Serial.println("Hecho\n");
}