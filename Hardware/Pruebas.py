import serial
import time

arduino = serial.Serial('COM5', 9600)

def OnOffLed():

    command = input("Type something..: (R/ B / W / G)")
    if command =="R":
        onoff = input("Type something..: (on/off)")
        if onoff == "on":
            arduino.write('R'.encode())
        else:
            arduino.write('2'.encode())
    elif command =="B":
        onoff = input("Type something..: (on/off)")
        if onoff == "on":
            arduino.write('B'.encode())
        else:
            arduino.write('3'.encode())
    elif command =="W":
        onoff = input("Type something..: (on/off)")
        if onoff == "on":
            arduino.write('W'.encode())
        else:
            arduino.write('1'.encode())
    elif command =="G":
        onoff = input("Type something..: (on/off)")
        if onoff == "on":
            arduino.write('G'.encode())
        else:
            arduino.write('4'.encode())
    else:
        print("nothing to do")

    OnOffLed()

time.sleep(2) #waiting the initialization...

OnOffLed()