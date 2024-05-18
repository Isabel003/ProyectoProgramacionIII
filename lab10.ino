#include <Servo.h> //Libreria del servomotor

//Pines digitales
int boton_izquierda = 3;
int boton_derecha = 4;

//Objeto del servomotor
Servo motor;

//Variable del monitor serial
int monitor;

//Variable del servomotor
int posicion =0;

void setup() 
{
  //Pines de entrada
  pinMode(boton_izquierda, INPUT_PULLUP);//Resistencia PULL-UP del arduino
  pinMode(boton_derecha, INPUT_PULLUP);
  //Pin del servomotor
  motor.attach(2);
  //Iniciar baudios
  Serial.begin(9600);
}

void loop() 
{
  Serial.println(" ");
  delay(1000);
    //Programar botones
    int valor_izquierda = 0;
    valor_izquierda = digitalRead(boton_izquierda);
    int valor_derecha = 0;
    valor_derecha = digitalRead(boton_derecha);
  
  //Mostrar valores de los push botons
    Serial.print("PUSH IZQUIERDO: ");
    if(valor_izquierda == 0)
    {
      Serial.println("Presionado");
    }
    else
    {
      Serial.println("Apagado");
    }
    Serial.print("PUSH DERECHO: ");
    if(valor_derecha == 0)
    {
      Serial.println("Presionado");
    }
    else
    {
      Serial.println("Apagado");
    }
        /*
          1 = LOW
          0 = HIGH
        */  

    // Mover hacia izquierda
  if (valor_izquierda == LOW) // Botón presionado
  {
    Serial.println("GIRAR IZQUIERDA");
    for (posicion = 90; posicion <= 180; posicion += 45)
    {
      motor.write(posicion);
      delay(500);
    }
    posicion = 90;
    motor.write(posicion);
  }

  // Mover hacia derecha
  if (valor_derecha == LOW) // Botón presionado
  {
    Serial.println("GIRAR DERECHA");
    for (posicion = 90; posicion >= 0; posicion -= 45)
    {
      motor.write(posicion);
      delay(500);
    }
    posicion = 90;
    motor.write(posicion);
  }

  // BOTONES APAGADOS
  if (valor_derecha == HIGH && valor_izquierda == HIGH)
  {
    posicion = 90;
    motor.write(posicion);
    Serial.println(" ");
    delay(100);
  }


  //Lectura del monitor serial
  if(Serial.available()>0)
  {
    //Leer el monitor serial
    monitor = Serial.read();
    //Mover hacia izquierda
    if((monitor == '0'))
    {
      Serial.println("GIRAR IZQUIERDA");
      for(posicion=90; posicion<=180; posicion+=45)
      {
        motor.write(posicion);
        delay(500);
      }
      posicion = 90;
      motor.write(posicion);
    }
    //Mover hacia derecha
    if((monitor == '1'))
    {
      Serial.println("GIRAR DERECHA");
      for(posicion =90; posicion>=0; posicion-=45)
      {
        motor.write(posicion);
        delay(500);
      }
      posicion = 90;
      motor.write(posicion);
    }
  }
}