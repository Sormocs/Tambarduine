from tkinter import *
from IDE import Window
import customtkinter

def Main():

    root = Tk()
    root.title("IDE")
    root.geometry("800x800")
    root.resizable(False, False)
    win = Window.Window(root)
    root.bind("<Key>", lambda event: win.tagHighlight())
    root.mainloop()



if __name__ == "__main__":

    Main()


