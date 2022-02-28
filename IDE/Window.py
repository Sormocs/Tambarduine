from tkinter import *
from collections import deque

class Window:

    def __init__(self, master):

        self.master = master
        self.master.title("IDE")

        self.mainCanvas = Canvas(self.master, width=800, height=600)
        self.objectsCanvas = Canvas(self.mainCanvas, width=800, height=600)
        self.objectsCanvas.grid(row=0, column=1)

        self.textBox = Text(self.objectsCanvas, width=80, height=20)
        self.textBox.grid(row=0, column=1, columnspan=2)

        self.mainCanvas.pack()



