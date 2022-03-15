#include <Servo.h>

#define PINZA_ABIERTA 110
#define PINZA_CERRADA 7
#define PINZA_CENTRAL 60

#define PINZA_HORIZONTAL 80
#define PINZA_VERTICAL 180
#define PINZA_NEUTRAL 125

#define HORIZONTAL_NEUTRAL 95
#define VERTICAL_NEUTRAL 147

#define buzzFrec1 1600
#define buzzFrec2 800

class Tambarduine{
private:
    int tempoNum = 1;
    int tempo = 2;
    int metrica = 4;

    int buzzPin = 8;
    int vertServoPin = 10;
    int horiServoPin = 9;
    int pinzaServoPin = 7;
    int ejePinzaServoPin = 6;

    static Tambarduine *instance;


    Servo vertServo, horiServo, pinzaServo, ejePinzaServo;

    int ledPin = 13;
    String option,value1,value2;
    int valueAction;
    char action;

    void Abanico(int direccion){
        MetronomoEspec(0);
        vertServo.write(VERTICAL_NEUTRAL+15*pow(-1,direccion-1));
        delay(500);
        vertServo.write(VERTICAL_NEUTRAL);
        delay(500);
        if (tempo > 1){
            MetronomoEspec(tempo*1000-1000);
        }
    }
    void Vertical(int direccion){
        MetronomoEspec(0);
        horiServo.write(HORIZONTAL_NEUTRAL+30*pow(-1,direccion-1));
        delay(500);
        horiServo.write(HORIZONTAL_NEUTRAL);
        delay(500);
    }

    void Percutor(int orden){
        switch (orden){
            case 1:
                ejePinzaServo.write(PINZA_HORIZONTAL);
                delay(300);
                horiServo.write(HORIZONTAL_NEUTRAL-30);
                delay(200);
                ejePinzaServo.write(PINZA_NEUTRAL);
                horiServo.write(HORIZONTAL_NEUTRAL);
                delay(500);
                break;

            case 2:
                horiServo.write(115);
                delay(300);
                horiServo.write(90);
                delay(700);
                break;

            case 3:
                vertServo.write(115);
                delay(300);
                vertServo.write(90);
                delay(700);
                break;

            case 4:
                vertServo.write(65);
                delay(300);
                vertServo.write(90);
                delay(700);
                break;

            case 5:
                pinzaServo.write(90); // apertura
                delay(200);
                vertServo.write(135);
                delay(500);
                vertServo.write(90);
                pinzaServo.write(90);
                delay(300);
                break;
            case 6:
                ejePinzaServo.write(45); // giro servo
                pinzaServo.write(90); // apertura pinza
                delay(250);
                horiServo.write(45);
                delay(500);
                horiServo.write(90);
                ejePinzaServo.write(90);
                pinzaServo.write(90);
                break;
            default:
                return;
        }

        if (tempo > 1000) {
            MetronomoEspec(tempo*1000-1000);
        }

    }

    void Golpe(){
        pinzaServo.write(PINZA_CERRADA);
        ejePinzaServo.write(PINZA_HORIZONTAL);
        delay(500);
        vertServo.write(VERTICAL_NEUTRAL+30);
        delay(300);
        pinzaServo.write(PINZA_CENTRAL);
        vertServo.write(VERTICAL_NEUTRAL);
        ejePinzaServo.write(PINZA_NEUTRAL);
        delay(200);
        if (tempo > 1) {
            MetronomoEspec(tempo*1000-1000);
        }
    }

    void Vibratto(int duracion){

        for (int i=0; i<duracion; i++){
            horiServo.write(HORIZONTAL_NEUTRAL-10);
            delay(100);
            if (i == duracion*tempo -1) {
                horiServo.write(HORIZONTAL_NEUTRAL);

            } else {
                horiServo.write(HORIZONTAL_NEUTRAL+10);
            }
            delay(100);
            if (duracion * 200 == tempo) {
                MetronomoEspec(0);
            }
        }
    }

    void Restablecer(){
        vertServo.write(VERTICAL_NEUTRAL);
        horiServo.write(HORIZONTAL_NEUTRAL);
        pinzaServo.write(PINZA_CENTRAL);
        ejePinzaServo.write(PINZA_NEUTRAL+15);
    }

    void SetTempo(int nuevoTempo){
        tempo = nuevoTempo;
    }

    void MetronomoEspec(int delayTime){
        delay(delayTime);
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
        MetronomoEspec(tempo*1000);
    }

    String getValue(String data, char separator, int index)
    {
        int found = 0;
        int strIndex[] = { 0, -1 };
        int maxIndex = data.length() - 1;

        for (int i = 0; i <= maxIndex && found <= index; i++) {
            if (data.charAt(i) == separator || i == maxIndex) {
                found++;
                strIndex[0] = strIndex[1] + 1;
                strIndex[1] = (i == maxIndex) ? i+1 : i;
            }
        }
        return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
    }

    public:
    void Setup() {
        Serial.begin(9600);
        pinMode(ledPin,OUTPUT);
        vertServo.attach(vertServoPin);
        horiServo.attach(horiServoPin);
        pinzaServo.attach(pinzaServoPin);
        ejePinzaServo.attach(ejePinzaServoPin);
        Restablecer();
        Percutor(2);
    }

    //singleton Tambarduine
    static Tambarduine* getInstance() {
        if (instance == nullptr) {
            instance = new Tambarduine();
        }
        return instance;
    }

    void Bucle(){
        option = Serial.readString();
        value1 = getValue(option,'#',0);
        value2 = getValue(option,'#',1);

        action = value1.charAt(0);
        valueAction = value2.toInt();


        switch (action){

            case 'A':
                //Llama a abanico con el parámetro valueAction como dirección
                Abanico(valueAction);
            case 'V':
                //Llama a vertical con el parámetro valueAction como dirección
                Vertical(valueAction);
                break;
            case 'P':
                //Llama a Percitor con el parámetro valueAction
                Percutor(valueAction);
                break;
            case 'G':
                //Llamada a Golpe
                Golpe();
                break;
            case 'T':
                //Llamada a Vibrato con el parametro valueAction como numero de vibraciones
                Vibratto(valueAction);
                break;
            case 'M':
                //Llamada a Metronomo para actualizar el numero con valueAction
                SetTempo(valueAction);

                break;
        }
    }

};


Tambarduine tambarduine;

void setup(){
    tambarduine = Tambarduine();
    tambarduine.Setup();

}

void loop(){
    tambarduine.Bucle();
}
