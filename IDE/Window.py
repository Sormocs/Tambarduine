import tkinter.filedialog
from tkinter import *
from IDE import LineNumbers
from tkinter import filedialog
import json

class Window:

    def __init__(self, master):

        self.master = master
        self.master.title("IDE")

        self.mainCanvas = Canvas(self.master, width=800, height=600)
        self.mainCanvas.place(x=0, y=0)

        self.objectsCanvas = Canvas(self.mainCanvas, width=800, height=600)
        self.objectsCanvas.place(x=0, y=0)

        self.textBox = Text(self.objectsCanvas, width=94, height=37) #, bg = "black",  fg = "white")

        self.textBox.grid(row=0, column=1, columnspan=2)

        self.scrollBar = Scrollbar(self.objectsCanvas, orient=VERTICAL)
        self.scrollBar.config(command=self.textBox.yview)
        self.scrollBar.grid(row=0, column=5, sticky=N+S)

        self.lineNumbers = LineNumbers.TextLineNumbers(self.objectsCanvas, width=25)
        self.lineNumbers.attach(self.textBox)
        self.lineNumbers.grid(row=0, column=0, sticky=N+S)

        self.textBox['yscrollcommand'] = self.scrollBar.set

        self.textBox.tag_configure("orange", foreground="orange")
        self.textBox.tag_configure("blue", foreground="blue")
        self.textBox.tag_configure("green", foreground="green")
        self.textBox.tag_configure("red", foreground="red")
        self.textBox.tag_configure("purple", foreground="purple")

        self.tags = ["orange", "blue", "red", "green", "purple"]
        self.wordList = [["for","while","if","else","to"],["Exec","Def"],["Cuando","EnTons"],["Fin-EnCaso","to","SET"],["EnCaso","Step","type"]]
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p","q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

        self.textBox.bind("<Return>", lambda event: self.Indent(event.widget))
        self.textBox.bind("<MouseWheel>", lambda event: self.MouseWheel(event.widget))

        self.numIdent = 0
        self.ident = "     "

        self.menuBar = Menu(self.master, bg="black", fg="white")

        self.menuBar.add_command(label="Open", command= lambda: self.Open())
        self.menuBar.add_command(label="Save as", command=lambda: self.SaveAs())
        self.menuBar.add_command(label="Save", command=lambda: self.Save())
        self.menuBar.add_command(label="Clear", command=lambda: self.Clear())
        self.menuBar.add_command(label="Compilar", command=lambda: self.Compile())
        self.menuBar.add_command(label="Ejecutar", command=lambda: self.Run())

        self.pathCode = ""

        self.master.config(menu=self.menuBar)

    def MouseWheel(self, event):

        self.lineNumbers.redraw()

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

    def tagHighlight(self):

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

        if self.textBox.get(pre) == self.textBox.get(index):
            pre = index
        else:
            if self.textBox.get(pre) in self.letters:
                return 0

        if self.textBox.get(post) in self.letters:
            return 0

        return 1

    def GetText(self):

        return self.textBox.get("1.0", "end")

    def Open(self):

        file = tkinter.filedialog.askopenfilename( filetypes=[("Code File", "*.json")])

        if file != "":
            with open(file, "r") as f:
                dicData = self.JsonToDict(f.read())
                print(dicData)
                self.LoadCode(dicData["code"],dicData["ident"])
                self.pathCode = file


    def SaveAs(self):

        self.GenerateJson()
        file = tkinter.filedialog.asksaveasfilename(defaultextension=".json")
        with open(file, 'w') as f:
            toSave = self.GenerateJson()
            f.write(toSave)

    def Save(self):

        if self.pathCode == "":
            self.SaveAs()
        else:
            self.GenerateJson()
            with open(self.pathCode, 'w') as f:
                toSave = self.GenerateJson()
                f.write(toSave)

    def Clear(self):

        self.textBox.delete("1.0", "end")
        self.lineNumbers.redraw()


    def GenerateJson(self):

        dic = {"ident": self.numIdent, "code": self.GetText()}
        json_string = json.dumps(dic)

        return json_string

    def JsonToDict(self, json_string):

        dic = json.loads(json_string)

        return dic

    def LoadCode(self, code, ident):

        self.numIdent = ident
        self.textBox.delete("1.0", "end")
        self.textBox.insert("1.0", code)
        self.lineNumbers.redraw()
        self.tagHighlight()

    def Compile(self):

        code = self.GetText()

        pass

    def Run(self):

        pass