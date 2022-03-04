import serial, time, sys

ard = serial.Serial('COM4', 9600)

data = ard.readline()

while True:

    print(data.decode('utf-8'))
    time.sleep(3)