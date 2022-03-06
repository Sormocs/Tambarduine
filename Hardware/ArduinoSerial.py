import time

import serial

class ArduinoSerial:
    def __init__(self):
        self.tempo = 0
        self.canSend = False
        self.arduino = serial.Serial('COM5', 9600) #Arduino Mega : self.arduino = serial.Serial('COM4', 9600)
        time.sleep(2)

    def send(self, message):

        print(message)

        if self.canSend:
            self.arduino.write(message.encode())

    def receive(self):
        return self.arduino.readline()

    def close(self):
        self.arduino.close()

    def Abanico(self, move):

        if move == "A":
            self.send("A#1") #Abanico#A
        elif move == "B":
            self.send("A#2") #Abanico#B

    def Vertical(self, move):

        if move == "D":
            self.send("V#1") #Vertical#D
        elif move == "I":
            self.send("V#2") #Vertical#I

    def Percutor(self, move):

        if move == "A":
            self.send("P#1") #Percutor#A
        elif move == "B":
            self.send("P#2") #Percutor#B
        elif move == "D":
            self.send("P#4") #Percutor#D
        elif move == "I":
            self.send("P#5") #Percutor#I
        elif move == "AB":
            self.send("P#6") #Percutor#AB
        elif move == "DI":
            self.send("P#7")  #Percutor#DI

    def Golpe(self):

        self.send("G#1") #Golpe#0

    def Vibrato(self, n):

        self.send("T#" + str(n)) #Vibrato#0

    def Metronomo(self, tempo):

        self.canSend = True
        self.tempo = tempo
        self.send("M#" + str(tempo)) #Tempo#0




