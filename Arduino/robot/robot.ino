int ledPin = 13;
String option,value1,value2;
int valueAction;
char action;

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

void setup(){
  Serial.begin(9600);
  pinMode(ledPin,OUTPUT);
}

void loop(){

  option = Serial.readString();
  value1 = getValue(option,'#',0);
  value2 = getValue(option,'#',1);

  action = value1.charAt(0);
  valueAction = value2.toInt();


  switch (action){

      case 'A':
          if (valueAction == 1){
            //Llamada a Abanico A
          }
          else{
            //Llamada a Abanico B
          }
          break;
      case 'V':
          if (valueAction == 1){
            //Llamada a Vertical A
          }
          else{
            //Llamada a Vertical B
          }
          break;
      case 'P':
          if (valueAction == 1){
            //Llamada a Percutor A
          }
          else if(valueAction == 2){
            //Llamada a Percutor B
          }
          else if(valueAction == 3){
            //Llamada a Percutor D
          }
          else if(valueAction == 4){
            //Llamada a Percutor I
          }
          else if(valueAction == 5){
            //Llamada a Percutor AB
          }
          else{
            //Llamada a Vertical DI
          }
          break;
      case 'G':
          //Llamada a Golpe
          break;
      case 'T':
          //Llamada a Vibrato con el parametro valueAction como numero de vibraciones
          break;
      case 'M':
          //Llamada a Metriono para actualizar el numero con valueAction
          break;
    
  }

  
}
