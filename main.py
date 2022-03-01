from tkinter import *
from IDE import Window

def Main():

    root = Tk()
    root.title("IDE")
    root.geometry("800x600")
    root.resizable(False, False)

    win = Window.Window(root)
    root.mainloop()


if __name__ == "__main__":

    Main()


