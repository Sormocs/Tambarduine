import time

import serial

class ArduinoSerial:

    """
    Class to handle serial communication with Arduino
    """

    def __init__(self):

        self.tempo = 0
        self.canSend = False
        self.arduino = serial.Serial('COM5', 9600) #Arduino Mega : self.arduino = serial.Serial('COM4', 9600)
        time.sleep(2)

    def send(self, message):

        """
        Send a message to the Arduino
        :param message: string
        :return: None
        """

        if self.canSend:
            self.arduino.write(message.encode())

    def receive(self):

        """
        Receive a message from the Arduino
        :return: string
        """

        return self.arduino.readline().decode()

        return self.arduino.readline()

    def close(self):

        """
        close the serial connection
        :return:
        """

        self.arduino.close()

    def Abanico(self, move):

        """
        Send a message to the Arduino to move the abanico
        :param move:
        :return: None
        """

        if move == "A":
            self.send("A#1") #Abanico#A
        elif move == "B":
            self.send("A#2") #Abanico#B

    def Vertical(self, move):

        """
        Send a message to the Arduino to move the vertical
        :param move:
        :return: None
        """

        if move == "D":
            self.send("V#1") #Vertical#D
        elif move == "I":
            self.send("V#2") #Vertical#I

    def Percutor(self, move):

        """
        Send a message to the Arduino to move the percutor
        :param move:
        :return: None
        """

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

        """
        Send a message to the Arduino to make a golpe
        :return: None
        """

        self.send("G#1") #Golpe#0

    def Vibrato(self, n):

        """
        Send a message to the Arduino to make a vibrato
        :param n: int
        :return: None
        """

        self.send("T#" + str(n)) #Vibrato#0

    def Metronomo(self, tempo):

        """
        Send a message to the Arduino to make a metronomo
        :param tempo: int
        :return: None
        """

        self.canSend = True
        self.tempo = tempo
        self.send("M#" + str(tempo)) #Tempo#0