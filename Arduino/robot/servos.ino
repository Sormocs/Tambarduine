#include <Servo.h>

int tempoNum = 1;
int tempo = 1;
int metrica = 4;

int LEDPin = 9;
int buzzPin = 8;
int vertServoPin = 10;
int horiServoPin = 9;
int pinzaServoPin = 7;
int ejePinzaServoPin = 6;

int buzzFrec1 = 1600;
int buzzFrec2 = 800;

Servo vertServo;
Servo horiServo;
Servo pinzaServo;
Servo ejePinzaServo;

void setup(){
  Serial.begin(9600);
  pinMode(buzzPin, OUTPUT);
  vertServo.attach(vertServoPin);
  horiServo.attach(horiServoPin);
  
  Restablecer();
  Abanico(2);
  Vertical(1);
}

void loop(){
}

void Abanico(int direccion){
  MetronomoEspec();
  vertServo.write(90-15*pow(-1,direccion-1));
  delay(500);
  vertServo.write(90);
  delay(500);
}

void Vertical(int direccion){
  MetronomoEspec();
  horiServo.write(90-15*pow(-1,direccion-1));
  delay(500);
  horiServo.write(90);
  delay(500);
}

void Percutor(int orden){
  switch (orden){
    
  }
}

void Vibratto(int duracion){
  
  for (int i=0; i<duracion*tempo; i++){
    MetronomoEspec();
    horiServo.write(80);
    delay(250);
    horiServo.write(100);
    delay(250);
    horiServo.write(80);
    delay(250);
    if (i == duracion*tempo -1) {
      horiServo.write(90);
    } else {
      horiServo.write(100);
    }
    delay(250);
  }
}

void Restablecer(){
  vertServo.write(90);
  horiServo.write(90);
}

void MetronomoEspec(){
  if (tempoNum == 1){
    tone(buzzPin, buzzFrec1, 30);
    
  } else {
    tone(buzzPin, buzzFrec2, 30);
  }
  tempoNum++;
  if (tempoNum > metrica){
    tempoNum = 1;
  }
}

void Metronomo(){
  MetronomoEspec();
  delay(tempo*500);
}
