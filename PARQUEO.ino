#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <Servo.h> 

LiquidCrystal_I2C lcd(0x27, 16, 2);  // Cambia la dirección I2C si es necesario
Servo myservo;

const int IR1 = 2;  // Sensor de entrada
const int IR2 = 3;  // Sensor de salida
int Slot = 4;       // Número total de espacios de estacionamiento

int flag1 = 0;
int flag2 = 0;

void setup() {
  Serial.begin(9600);
  lcd.init(); // Inicializa el LCD
  lcd.backlight(); // Enciende la retroiluminación

  pinMode(IR1, INPUT);
  pinMode(IR2, INPUT);

  myservo.attach(4); // Cambia el pin del servo si es necesario
  myservo.write(100); // Posición inicial del servomotor

  lcd.setCursor(0, 0);
  lcd.print("     PROYECTO FINAL   ");
  lcd.setCursor(0, 1);
  lcd.print(" SISTEMA DE PARQUEO ");
  delay(2000);
  lcd.clear();
}

void loop() {
  // Lecturas de sensores y actualización de slots
  bool IR1_state = digitalRead(IR1) == LOW;
  bool IR2_state = digitalRead(IR2) == LOW;

  if (IR1_state && flag1 == 0 && flag2 == 0) {
    if (Slot > 0) {
      flag1 = 1;
      delay(2000); // Delay antes de abrir la barrera
      myservo.write(0); // Abre la barrera
      Slot--;
      delay(3000); // Delay para permitir que el coche pase completamente
      myservo.write(100); // Cierra la barrera
      delay(1000); // Pequeño delay después de cerrar la barrera
      flag1 = 0; // Resetea la bandera
    } else {
      lcd.setCursor(0, 0);
      lcd.print("    LO SENTIMOS :(    ");
      lcd.setCursor(0, 1);
      lcd.print("  Parqueo lleno  ");
      delay(3000);
      lcd.clear();
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
  Serial.println("Scanning...");
  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address < 16) Serial.print("0");
      Serial.print(address, HEX);
      Serial.println(" !");
      Devices++;
    } else if (error == 4) {
      Serial.print("Unknown error at address 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
    }
  }
  if (Devices == 0) Serial.println("No I2C devices found\n");
  else Serial.println("done\n");
}