from tkinter import *

import platform

class TextLineNumbers(Canvas):

    """
    A canvas widget that displays the line numbers for a text widget.
    """
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)

        self.textwidget = None
        self.fontSize = 12



    def attach(self, text_widget):

        """
        Attach the line number canvas to the text widget
        :param text_widget: text
        :return: None
        """

        self.textwidget = text_widget

    def redraw(self, *args):
        """
        Redraw the line numbers
        :param args:
        :return: None
        """
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(1,y,anchor="nw", text=linenum, fill='black')
            i = self.textwidget.index("%s+1line" % i)