from tkinter import *

import platform

class TextLineNumbers(Canvas):
    '''
        Canvas for Linenumbers
    '''
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        self.fontSize = 12



    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(1,y,anchor="nw", text=linenum, fill='black')
            i = self.textwidget.index("%s+1line" % i)