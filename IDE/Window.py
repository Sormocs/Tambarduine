import tkinter.filedialog
from tkinter import *
from IDE import LineNumbers
from COMP import Syntax
from COMP import Lexer
import json

class Window:

    """

    Class window is the main window of the IDE.

    """

    def __init__(self, master):

        """
        init method of the class Window.
        :param master: canva of the IDE
        """

        self.master = master
        self.master.title("IDE")

        self.mainCanvas = Canvas(self.master, width=800, height=800)
        self.mainCanvas.place(x=0, y=0)

        self.objectsCanvas = Canvas(self.mainCanvas, width=800, height=800)
        self.objectsCanvas.place(x=0, y=0)

        self.consoleCanvas = Canvas(self.mainCanvas, width=800, height=200)
        self.consoleCanvas.place(x=0, y=596)

        self.textBox = Text(self.objectsCanvas, width=94, height=37) #, bg = "black",  fg = "white")
        self.textBox.grid(row=0, column=1, columnspan=2)

        self.outputBox = Text(self.consoleCanvas, width=97, height=11)
        self.outputBox.grid(row=1, column=0, columnspan=2)
        self.outputBox.configure(state="disabled")

        self.labelConsole = Label(self.consoleCanvas, text="Console")
        self.labelConsole.grid(row=0, column=0, columnspan=1, sticky=W)

        self.scrollBar = Scrollbar(self.objectsCanvas, orient=VERTICAL)
        self.scrollBar.config(command=self.textBox.yview)
        self.scrollBar.grid(row=0, column=5, sticky=N+S)

        self.scrollBarConsole = Scrollbar(self.consoleCanvas, orient=VERTICAL)
        self.scrollBarConsole.config(command=self.outputBox.yview)
        self.scrollBarConsole.grid(row=1, column=5, sticky=N+S)

        self.lineNumbers = LineNumbers.TextLineNumbers(self.objectsCanvas, width=25)
        self.lineNumbers.attach(self.textBox)
        self.lineNumbers.grid(row=0, column=0, sticky=N+S)

        self.textBox['yscrollcommand'] = self.scrollBar.set
        self.outputBox['yscrollcommand'] = self.scrollBarConsole.set

        self.textBox.tag_configure("orange", foreground="orange")
        self.textBox.tag_configure("blue", foreground="blue")
        self.textBox.tag_configure("green", foreground="green")
        self.textBox.tag_configure("red", foreground="red")
        self.textBox.tag_configure("purple", foreground="purple")

        self.tags = ["orange", "blue", "red", "green", "purple"]
        self.wordList = [["WHILE","FOR","for","while","if","else","to"],["Exec","Def"],["Cuando","EnTons"],["Fin-EnCaso","to","SET"],["EnCaso","Step","type"]]
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p","q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

        self.textBox.bind("<Return>", lambda event: self.Indent(event.widget))
        self.textBox.bind("<Tab>", lambda event: self.IdentAux(event.widget))
        self.textBox.bind("<BackSpace>", lambda event: self.BackSpaceFunction(event.widget))
        self.textBox.bind("<MouseWheel>", lambda event: self.MouseWheel(event.widget))
        self.textBox.bind("<Configure>", lambda event: self.MouseWheel(event.widget))
        self.master.bind("<Button-1>", lambda event: self.MouseWheel(event.widget))

        self.numIdent = 0
        self.ident = "     "

        self.menuBar = Menu(self.master, bg="black", fg="white")

        self.menuBar.add_command(label="Open", command= lambda: self.Open())
        self.menuBar.add_command(label="Save as", command=lambda: self.SaveAs())
        self.menuBar.add_command(label="Save", command=lambda: self.Save())
        self.menuBar.add_command(label="Clear", command=lambda: self.Clear())
        self.menuBar.add_command(label="Clear Console", command=lambda: self.ClearOutput())
        self.menuBar.add_command(label="Compile", command=lambda: self.Compile())
        self.menuBar.add_command(label="Run", command=lambda: self.Run())

        self.pathCode = ""

        self.master.config(menu=self.menuBar)

    def MouseWheel(self, event):

        """
        Method that manages the mouse wheel to update the lines of code
        :param event: event that is triggered when the mouse wheel is moved
        :return: None
        """

        self.lineNumbers.redraw()

    def IdentAux(self, event):

        """
        Method that manages the indentation of the code with the tab key
        :param event: the tab key
        :return: None
        """

        self.numIdent += 1
        self.textBox.insert(INSERT, self.ident)

        return "break"

    def BackSpaceFunction(self, widget):

        """
        Method that manages the backspace key to remove the indentation
        :param widget: the widget that is being modified textbox
        :return: None
        """

        actualLine = self.textBox.get("insert linestart", "insert lineend")

        if len(actualLine) != 0:

            if actualLine[-1] == "{":

                self.numIdent -= 1


    def VerifyIdent(self, prevLine):

        """
        Method that verifies if the line of code is indented or not
        :param prevLine: string that is the previous line of code
        :return: None
        """

        lenLine = len(prevLine)

        if lenLine > 6:
            if prevLine[0:5] == self.ident:
                return True
            else:
                return False


    def Indent(self, widget):

        """
        Method that manages the indentation of the code with the return key
        :param widget: textbox widget that is being modified
        :return: None
        """

        index1 = widget.index("insert")
        index2 = "%s-%sc" % (index1, 1)
        prevIndex = widget.get(index2, index1)
        prevIndex2 = widget.get("%s-%sc" % (index1, 2), index1)

        prevIndentLine = widget.index(index1 + "linestart")
        prevLine = widget.get(prevIndentLine, index1 + "lineend")


        if self.numIdent < 0:
            self.numIdent = 0

        if prevIndex == "{":

            self.numIdent += 1
            widget.insert("insert", "\n" + self.ident*self.numIdent)
            self.lineNumbers.redraw()
            return "break"

        elif prevIndex2 == "};":

            self.numIdent -= 1
            widget.insert("insert", "\n" + self.ident*self.numIdent)
            self.lineNumbers.redraw()
            return "break"

        else:

            if self.VerifyIdent(prevLine) and self.numIdent == 0:

                for i in range(0, len(prevLine), 5):

                    print(len(prevLine[i:i+5]),self.ident)

                    if prevLine[i:i+5] == self.ident:

                        widget.insert("insert", self.ident)
                        self.numIdent += 1

            if prevLine == "":
                self.numIdent = 0

            widget.insert("insert", "\n" + self.ident * self.numIdent)
            self.lineNumbers.redraw()
            return "break"

    def GetIndex(self, index):

        """
        Method that gets the index of the line of code
        :param index: int that is the index of the line of code
        :return: int
        """

        while True:
            if self.textBox.get(index) == " ":
                index = "%s+%sc" % (index, 1)
            else:
                return self.textBox.index(index)

    def tagHighlight(self):

        """
        Method that highlights the code in reserved words
        :return: None
        """

        self.lineNumbers.redraw()

        start = "1.0"
        end = "end"

        for mylist in self.wordList:
            num = int(self.wordList.index(mylist))

            for word in mylist:
                self.textBox.mark_set("matchStart", start)
                self.textBox.mark_set("matchEnd", start)
                self.textBox.mark_set("SearchLimit", end)

                mycount = IntVar()

                while True:
                    index = self.textBox.search(word, "matchEnd", "SearchLimit", count=mycount, regexp=False)

                    if index == "": break
                    if mycount.get() == 0: break

                    self.textBox.mark_set("matchStart", index)
                    self.textBox.mark_set("matchEnd", "%s+%sc" % (index, mycount.get()))

                    preIndex = "%s-%sc" % (index, 1)
                    postIndex = "%s+%sc" % (index, mycount.get())

                    if self.check(index, preIndex, postIndex):
                        self.textBox.tag_add(self.tags[num], "matchStart", "matchEnd")

    def check(self, index, pre, post):

        """
        Method that checks if the word is a reserved word
        :param index: int
        :param pre: int
        :param post: int
        :return: bool
        """

        if self.textBox.get(pre) == self.textBox.get(index):
            pre = index
        else:
            if self.textBox.get(pre) in self.letters:
                return 0

        if self.textBox.get(post) in self.letters:
            return 0

        return 1

    def GetText(self):

        """
        Get the code of the textbox
        :return: string of the code
        """

        return self.textBox.get("1.0", "end")

    def Open(self):

        """
        Method that opens a file
        :return: None
        """

        file = tkinter.filedialog.askopenfilename( filetypes=[("Code File", "*.json")])

        if file != "":
            with open(file, "r") as f:
                dicData = self.JsonToDict(f.read())
                self.LoadCode(dicData["code"],dicData["ident"])
                self.pathCode = file


    def SaveAs(self):

        """
        Method that saves the code as a file
        :return: None
        """

        self.GenerateJson()
        file = tkinter.filedialog.asksaveasfilename(defaultextension=".json")

        if file != "":
            with open(file, 'w') as f:
                toSave = self.GenerateJson()
                f.write(toSave)

    def Save(self):

        """
        Method that saves the code
        :return:
        """

        if self.pathCode == "":
            self.SaveAs()
        else:
            self.GenerateJson()
            with open(self.pathCode, 'w') as f:
                toSave = self.GenerateJson()
                f.write(toSave)

    def Clear(self):

        """
        Method that clears the code in the textbox
        :return: None
        """

        self.numIdent = 0
        self.textBox.delete("1.0", "end")
        self.lineNumbers.redraw()


    def GenerateJson(self):

        """
        Method that generates the json file
        :return: Json object
        """

        dic = {"ident": self.numIdent, "code": self.GetText()}
        json_string = json.dumps(dic)

        return json_string

    def JsonToDict(self, json_string):

        """
        Method that converts a json file to a dictionary
        :param json_string: json object
        :return: dictionary
        """

        dic = json.loads(json_string)

        return dic

    def LoadCode(self, code, ident):

        """
        Method that loads the code
        :param code: string of the code
        :param ident: int of the identation
        :return: none
        """

        self.numIdent = ident
        self.textBox.delete("1.0", "end")
        self.textBox.insert("1.0", code)
        self.lineNumbers.redraw()
        self.tagHighlight()

    def Compile(self):

        """
        Method that compiles the code
        :return:
        """

        code = self.GetText()
        #Lexer.TokenGen(code)
        Syntax.Parsear(code,self.outputBox)


    def Run(self):

        """
        Method that runs the code
        :return:
        """

        pass

    def SendOutput(self, text):

        """
        Method that sends the output to the textbox in the bottom
        :param text: string
        :return: None
        """

        self.outputBox.configure(state="normal")
        self.outputBox.insert("end", text + "\n")
        self.outputBox.configure(state="disabled")

    def ClearOutput(self):

        """
        Method that clears the output
        :return: None
        """

        self.outputBox.configure(state="normal")
        self.outputBox.delete("1.0", "end")
        self.outputBox.configure(state="disabled")

    def GetLinesCode(self):

        """
        Method that gets the lines of the code
        :return: list of strings
        """

        code = self.GetText()
        lines = code.split("\n")

        return lines

    def SearchLine(self, line):

        """
        Search a line in the code
        :param line: string
        :return: int
        """

        lines = self.GetLinesCode()

        for i in range(len(lines)):
            if lines[i] == line:
                return i + 1

        return -1