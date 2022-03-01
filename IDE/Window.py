from tkinter import *
from collections import deque

class Window:

    def __init__(self, master):

        self.master = master
        self.master.title("IDE")

        self.mainCanvas = Canvas(self.master, width=800, height=600)
        self.mainCanvas.place(x=0, y=0)

        self.objectsCanvas = Canvas(self.mainCanvas, width=800, height=600)
        self.objectsCanvas.place(x=100, y=100)

        self.textBox = Text(self.objectsCanvas, width=80, height=20)
        self.textBox.grid(row=0, column=1, columnspan=2)

        self.textBox.tag_configure("orange", foreground="orange")
        self.textBox.tag_configure("blue", foreground="blue")
        self.textBox.tag_configure("green", foreground="green")
        self.textBox.tag_configure("red", foreground="red")
        self.textBox.tag_configure("purple", foreground="purple")

        self.textBox.bind("<Return>", lambda event: self.Indent(event.widget))
        self.numIdent = 0
        self.ident = "     "

        self.menuBar = Menu(self.master)

        self.menuBar.add_command(label="Open", command= lambda: self.Open())
        self.menuBar.add_command(label="Save as", command=lambda: self.SaveAs())
        self.menuBar.add_command(label="Save", command=lambda: self.Save())
        self.menuBar.add_command(label="Clear", command=lambda: self.Clear())

        self.master.config(menu=self.menuBar)

    def Indent(self, widget):

        index1 = widget.index("insert")
        index2 = "%s-%sc" % (index1, 1)
        prevIndex = widget.get(index2, index1)

        if self.numIdent < 0:
            self.numIdent = 0

        if prevIndex == "{":

            self.numIdent += 1
            widget.insert("insert", "\n" + self.ident*self.numIdent)
            return "break"

        elif prevIndex == "}":

            self.numIdent -= 1
            widget.insert("insert", "\n" + self.ident*self.numIdent)
            return "break"

        else:

            widget.insert("insert", "\n" + self.ident * self.numIdent)
            return "break"

    def GetIndex(self, index):
        while True:
            if self.textBox.get(index) == " ":
                index = "%s+%sc" % (index, 1)
            else:
                return self.textBox.index(index)

