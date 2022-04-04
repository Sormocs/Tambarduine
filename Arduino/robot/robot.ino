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

/*
 * @brief Estructura de los nodos de la lista
 */
struct Nodo {
    char movimiento;
    int direccion;
    struct Nodo *sig;
};

/*
 * @brief Lista enlazada de los movimientos
 */
class Acciones {
    struct Nodo *inicio;
    int longitud;

public:
    /*
     * @brief Constructor de la lista
     * @param string, int
     */
    void Agregar(char movimiento, int num){

        struct Nodo *nuevo = new Nodo;
        nuevo->movimiento = movimiento;
        nuevo->direccion = num;
        nuevo->sig = NULL;

        if(inicio == NULL){
            inicio = nuevo;
        } else{
            struct Nodo *aux = inicio;
            while(aux->sig != NULL){
                aux = aux->sig;
            }
            aux->sig = nuevo;
        }
        longitud++;
    }

    /*
     * @brief Devuelve el primer movimiento de la lista
     * @return Nodo
     */
    Nodo* Primero(){
        return inicio;
    }

    /*
     * @brief Devuelve el primer elemento y lo elimina de la lista
     * @return Nodo
     */
    Nodo* PrimeroYEliminar(){

        struct Nodo *aux = inicio;
        inicio = inicio->sig;
        longitud--;
        return aux;
    }

    /*
     * @brief Devuelve la longitud de la lista
     * @return int
     */
    int Longitud(){
        return longitud;
    }

    /*
     * @brief Destructor de la lista
     */
    void Vaciar(){

        struct Nodo *aux = inicio;
        while(aux != NULL){
            struct Nodo *aux2 = aux;
            aux = aux->sig;
            delete aux2;
        }
        inicio = NULL;
        longitud = 0;
    }
};

/*
 * @brief Clase para el robot
 */
class Tambarduine{

private:
    //metrónomo
    int tempoNum = 1;
    int tempo = 2;
    int metrica = 4;

    // pines del ardiuno
    int buzzPin = 8;
    int ledPin = 13;
    int vertServoPin = 10;
    int horiServoPin = 9;
    int pinzaServoPin = 7;
    int ejePinzaServoPin = 6;

    // órdenes
    Acciones acciones;
    bool configurado = false;
    bool metronomo = false;
    struct Nodo *accion = new Nodo;

    //singleton
    static Tambarduine *instance;

    //servos
    Servo vertServo, horiServo, pinzaServo, ejePinzaServo;

    // pyserial
    String option,value1,value2;
    int valueAction;
    char action;

    /*
     * @brief Realiza el movimiento de abanico
     * @param int
     */
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

    /*
     * @brief Realiza el movimiento de abanico vertical
     * @param int
     */
    void Vertical(int direccion){
        MetronomoEspec(0);
        horiServo.write(HORIZONTAL_NEUTRAL+30*pow(-1,direccion-1));
        delay(500);
        horiServo.write(HORIZONTAL_NEUTRAL);
        delay(500);
    }

    /*
     * @brief Golpea el pandero en diferentes lugares
     * @param int
     */
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

        // Hace sonar el metrónomo en el momento adecuado
        if (tempo > 1000) {
            MetronomoEspec(tempo*1000-1000);
        }

    }

    /*
     * @brief Golpea el pandero al centro
     */
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

    /*
     * @brief mueve el pandero a gran velocidad un número de veces
     * @param int: número de veces que se moverá el pandero
     */
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

    /*
     * @brief restablece las posiciones del pandero
     */
    void Restablecer(){
        vertServo.write(VERTICAL_NEUTRAL);
        horiServo.write(HORIZONTAL_NEUTRAL);
        pinzaServo.write(PINZA_NEUTRAL);
        ejePinzaServo.write(EJE_PINZA_NEUTRAL);
    }

    /*
     * @brief establece el tempo del metrónomo
     * @param int: tempo en segundos
     */
    void SetTempo(int nuevoTempo){
        tempo = nuevoTempo;
    }

    /*
     * @brief provoca el sonido del metrónomo con el delay indicado
     * @param int: delay en milisegundos
     */
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

    /*
     * @brief suena el metrónomo con el tempo indicado
     */
    void Metronomo(){
        MetronomoEspec(tempo*1000);
    }

    /*
     * @brief establece la comunicación entre el arduino y el ordenador
     * @param string, char, int
     * @return string
     */
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
    /*
     * @brief inicializa el arduino
     */
    void Setup() {
        Serial.begin(9600);
        pinMode(ledPin,OUTPUT);
        vertServo.attach(vertServoPin);
        horiServo.attach(horiServoPin);
        pinzaServo.attach(pinzaServoPin);
        ejePinzaServo.attach(ejePinzaServoPin);
        pinMode(3 , OUTPUT);
        digitalWrite(3 , LOW); 

    }

    /*
     * @ singleton de la clase
     * @return instancia de la clase
     */
    static Tambarduine* getInstance() {
        if (instance == nullptr) {
            instance = new Tambarduine();
        }
        return instance;
    }

    /*
     * @brief configura los movimientos en la lista
     */
    void Config(){

        while(!configurado) {

            option = Serial.readString();
            value1 = getValue(option,'#',0);
            value2 = getValue(option,'#',1);

            action = value1.charAt(0);
            valueAction = value2.toInt();


            switch (action){

                case 'A':
                    //Llama a abanico con el parámetro valueAction como dirección
                    //Abanico(valueAction);
                    acciones.Agregar('A', valueAction);
                case 'V':
                    //Llama a vertical con el parámetro valueAction como dirección
                    //Vertical(valueAction);
                    acciones.Agregar('V', valueAction);
                    break;
                case 'P':
                    //Llama a Percitor con el parámetro valueAction
                    //Percutor(valueAction);
                    acciones.Agregar('P', valueAction);
                    break;
                case 'G':
                    //Llamada a Golpe
                    //Golpe();
                    acciones.Agregar('G', 0);
                    break;
                case 'T':
                    //Llamada a Vibrato con el parametro valueAction como numero de vibraciones
                    //Vibratto(valueAction);
                    acciones.Agregar('T', valueAction);
                    break;
                case 'M':
                    //Llamada a Metronomo para actualizar el numero con valueAction
                    SetTempo(valueAction);
                    metronomo = true;
                    break;
                case 'S':
                    configurado = true;
                    digitalWrite(3 , HIGH); 
                    break;
            }
        }

    }

    /*
     * @brief ejecuta la lista de acciones
     */
    void Bucle(){
        if (!configurado){
            Restablecer();
            Config();
            //Vibratto(5);
            //Abanico(1);
            //Vertical(1);
            //Golpe();
            //Percutor(1);
            
        } else if (metronomo){
            while (acciones.Longitud() > 0){
                accion = acciones.PrimeroYEliminar();

                switch (accion->movimiento){
                    case 'A':
                        Abanico(accion->direccion);
                        break;
                    case 'V':
                        Vertical(accion->direccion);
                        break;
                    case 'P':
                        Percutor(accion->direccion);
                        break;
                    case 'G':
                        Golpe();
                        break;
                    case 'T':
                        Vibratto(accion->direccion);
                        break;
                }
                configurado = false;
                digitalWrite(3 , LOW); 
            }
        } else {

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
