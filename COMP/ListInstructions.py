import Hardware.ArduinoSerial as ArduinoSerial
import time

class NodoInstructions:
    def __init__(self, instruction, value):
        self.instruction = instruction
        self.value = value
        self.siguiente = None

    def getInstruction(self):
        return self.instruction

    def getValue(self):
        return self.value

    def getSiguiente(self):
        return self.siguiente

    def setSiguiente(self, siguiente):
        self.siguiente = siguiente


class ListInstructions:

    def __init__(self):
        self.inicio = None
        self.size = 0
        self.arduino = ArduinoSerial.ArduinoSerial()


    def add(self, instruction, value):
        if self.inicio == None:
            self.inicio = NodoInstructions(instruction, value)
        else:
            aux = self.inicio
            while aux.getSiguiente() != None:
                aux = aux.getSiguiente()
            aux.setSiguiente(NodoInstructions(instruction, value))
        self.size += 1

    def getSize(self):
        return self.size

    def deleteAll(self):

        self.inicio = None

    def execute(self):

        aux = self.inicio

        while aux != None:

            action = aux.getInstruction()
            value = aux.getValue()

            if action == "Abanico":

                self.arduino.Abanico(value)

            elif action == "Vertical":

                self.arduino.Vertical(value)

            elif action == "Percutor":

                self.arduino.Percutor(value)

            elif action == "Golpe":

                self.arduino.Golpe()

            elif action == "Vibrato":

                self.arduino.Vibrato(value)

            elif action == "Metronomo":

                self.arduino.Metronomo(value)

            elif action == "Start":

                self.arduino.StartExecite()

            time.sleep(1)
            aux = aux.getSiguiente()


        self.arduino.StartExecute()
        self.deleteAll()

    def metronoOff(self):
        self.arduino.DisableMetronomo()

