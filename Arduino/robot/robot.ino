#include <Servo.h>

#define PINZA_ABIERTA 110
#define PINZA_CERRADA 7
#define PINZA_NEUTRAL 60

#define EJE_PINZA_HORIZONTAL 80
#define EJE_PINZA_VERTICAL 180
#define EJE_PINZA_NEUTRAL 125

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
                //Golpea el pandero por la derecha
                ejePinzaServo.write(EJE_PINZA_HORIZONTAL);  //Coloca la pinza en horizontal
                delay(300);
                horiServo.write(HORIZONTAL_NEUTRAL-30); //Gira el pandero hacia la derecha
                delay(200);
                ejePinzaServo.write(EJE_PINZA_NEUTRAL); //Coloca la pinza en diagonal
                horiServo.write(HORIZONTAL_NEUTRAL);    //Gira el pandero hacia la posición neutral
                delay(500);
                break;

            case 2:
                //Golpea el pandero por la izquierda
                ejePinzaServo.write(EJE_PINZA_HORIZONTAL);  //Coloca la pinza en horizontal
                delay(300);
                horiServo.write(HORIZONTAL_NEUTRAL+30); //Gira el pandero hacia la izquierda
                delay(200);
                ejePinzaServo.write(EJE_PINZA_NEUTRAL);     //Coloca la pinza en diagonal
                horiServo.write(HORIZONTAL_NEUTRAL);    //Gira el pandero hacia la posición neutral
                delay(500);
                break;

            case 3:
                //Golpea el pandero por arriba
                ejePinzaServo.write(EJE_PINZA_VERTICAL);//Coloca la pinza en vertical
                pinzaServo.write(PINZA_ABIERTA);        //Abre la pinza
                delay(300);
                vertServo.write(VERTICAL_NEUTRAL-30);   //Inclina el pandero hacia abajo
                delay(200);
                ejePinzaServo.write(EJE_PINZA_NEUTRAL); //Coloca la pinza en diagonal
                pinzaServo.write(PINZA_NEUTRAL);        //Coloca la pinza en posición neutral
                vertServo.write(VERTICAL_NEUTRAL);      //Inclina el pandero a la posición neutral
                break;

            case 4:
                //Golpea el pandero por abajo
                ejePinzaServo.write(EJE_PINZA_VERTICAL);    //Coloca la pinza en vertical
                pinzaServo.write(PINZA_ABIERTA);        //Abre la pinza
                delay(300);
                vertServo.write(VERTICAL_NEUTRAL+30);   //Inclina el pandero hacia arriba
                delay(200);
                ejePinzaServo.write(EJE_PINZA_NEUTRAL);     //Coloca la pinza en diagonal
                vertServo.write(VERTICAL_NEUTRAL);      //inclina el pandero a la posición neutral
                pinzaServo.write(PINZA_NEUTRAL);        //Coloca la pinza en posición neutral
                delay(500);
                break;

            case 5:
                //Golpea el pandero por la izquierda y la derecha a la vez
                pinzaServo.write(PINZA_ABIERTA);        //Abre la pinza
                ejePinzaServo.write(EJE_PINZA_HORIZONTAL);  //Coloca la pinza en horizontal
                delay(300);
                vertServo.write(VERTICAL_NEUTRAL-45);   //Inclina el pandero hacia abajo
                delay(200);
                vertServo.write(VERTICAL_NEUTRAL);      //Inclina el pandero a la posición neutral
                ejePinzaServo.write(EJE_PINZA_NEUTRAL);     //Coloca la pinza en diagonal
                pinzaServo.write(PINZA_NEUTRAL);        //Coloca la pinza en posición neutral

                break;

            case 6:
                //Golpea el pandero por arriba y abajo a la vez
                ejePinzaServo.write(EJE_PINZA_VERTICAL);//Coloca la pinza en vertical
                pinzaServo.write(PINZA_ABIERTA);        //Abre la pinza
                delay(300);
                horiServo.write(HORIZONTAL_NEUTRAL-45); //Gira el pandero hacia la derecha
                delay(200);
                horiServo.write(HORIZONTAL_NEUTRAL);    //Gira el pandero hacia la posición neutral
                ejePinzaServo.write(EJE_PINZA_NEUTRAL);     //Coloca la pinza en diagonal
                pinzaServo.write(PINZA_NEUTRAL);        //Coloca la pinza en posición neutral
                break;

            default:
                return;
        }

        if (tempo > 1000) {
            MetronomoEspec(tempo*1000-1000);
        }

    }

    void Golpe(){
        pinzaServo.write(PINZA_CERRADA);                //Cierra la pinza
        ejePinzaServo.write(EJE_PINZA_HORIZONTAL);      //Coloca la pinza en horizontal
        delay(300);
        vertServo.write(VERTICAL_NEUTRAL-50);           //Inclina el pandero hacia abajo
        delay(200);
        vertServo.write(VERTICAL_NEUTRAL);              //Inclina el pandero a la posición neutral
        pinzaServo.write(PINZA_NEUTRAL);                //Coloca la pinza en posición neutral
        ejePinzaServo.write(EJE_PINZA_NEUTRAL);         //Coloca la pinza en diagonal
        delay(500);
        if (tempo > 1) {
            MetronomoEspec(tempo*1000-1000);
        }
    }

    void Vibratto(int movimientos){

        for (int i = 1; i < movimientos; i++) {
            if (i % 2 == 0) {
                horiServo.write(HORIZONTAL_NEUTRAL-10);
            } else {
                horiServo.write(HORIZONTAL_NEUTRAL+10);
            }
            delay(100);
            if (i % 10 == 0) {
                MetronomoEspec(0);
            }
        }

        horiServo.write(HORIZONTAL_NEUTRAL);

        if (movimientos % 10 != 0) {
            MetronomoEspec(movimientos % 10 * 100);
        }


    }

    void Restablecer(){
        vertServo.write(VERTICAL_NEUTRAL);
        horiServo.write(HORIZONTAL_NEUTRAL);
        pinzaServo.write(PINZA_NEUTRAL);
        ejePinzaServo.write(EJE_PINZA_NEUTRAL);
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
