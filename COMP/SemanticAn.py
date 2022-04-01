from COMP.ply.yacc import YaccSymbol

nums = "0123456789"
prim_symbols = ["*", "%", "//", "/"]
sec_symbols = ["+", "-"]

global_vars = []
methods = []

metronome = False

box = None

def FinalOp(op):
    i = 0
    res = 0
    while (len(op) != 1):
        if op[i + 1] == "+":
            res += float(op[i]) + float(op[i + 2])
        elif op[i + 1] == "-":
            res += float(op[i]) - float(op[i + 2])
        else:
            pass
        op[0] = res
        # op.remove(op[i])
        op.remove(op[i + 1])
        op.remove(op[i + 1])
        res = 0
    return float(op[0])


def Solve(op):
    res1 = []
    symbs = []
    skip = -1

    for i in range(0, len(op)):
        if i + 1 < len(op):
            if op[i + 1] == "**":
                res1 += [str(float(op[i]) ** float(op[i + 2]))]
                skip = i + 2
            elif op[i] == "**" or i == skip:
                pass
            elif op[i] in prim_symbols or op[i] in sec_symbols:
                symbs += [op[i]]
            else:
                res1 += [op[i]]
        else:
            if (i == skip):
                pass
            else:
                res1 += [op[i]]

    new_op = FormOp(res1, symbs)

    res1 = []
    symbs = []
    for i in range(0, len(new_op)):
        if i + 1 != len(new_op):
            if new_op[i + 1] in prim_symbols:
                if new_op[i + 1] == "*":
                    res1 += [str(float(new_op[i]) * float(new_op[i + 2]))]
                elif new_op[i + 1] == "%":
                    res1 += [float(int(new_op[i]) % float(new_op[i + 2]))]
                elif new_op[i + 1] == "//":
                    res1 += [float(int(new_op[i]) // float(new_op[i + 2]))]
                elif new_op[i + 1] == "/":
                    res1 += [float(int(new_op[i]) / float(new_op[i + 2]))]
                skip = i + 2
            elif new_op[i] in prim_symbols or i == skip:
                pass
            elif new_op[i] in sec_symbols:
                symbs += [new_op[i]]
            else:
                res1 += [new_op[i]]
        else:
            if (i == skip):
                pass
            else:
                res1 += [new_op[i]]
    new_op2 = FormOp(res1, symbs)
    res = FinalOp(new_op2)

    return res


def FormOp(nums, symbs):
    i = 0
    res = []
    while i < len(nums):
        if i < len(symbs):
            res += [nums[i]]
            res += [symbs[i]]
        else:
            res += [nums[i]]

        i += 1
    return res


def Funciones(name,param):

    if name == "Percutor":
        if param == "A":
            print ("Funcion percutor Arriba")
        elif param == "B":
            print ("Funcion percutor Abajo")
        elif param == "D":
            print("Funcion percutor Derecha")
        elif param == "I":
            print ("Funcion percutor Izquierda")
        elif param == "DI":
            print ("Funcion percutor Derecha e Izquierda")
        elif param == "AB":
            print ("Funcion percutor Arriba y Abajo")
        else:
            print ("Parametro incorrecto")

    elif name == "Abanico":
        if param == "A":
            print ("Funcion Abanico Arriba")
        elif param == "B":
            print("Funcion Abanico Abajo")
        else:
            print ("Parametro incorrecto")

    elif name == "Vertical":
        if param == "D":
            print ("Funcion Abanico Arriba")
        elif param == "I":
            print("Funcion Abanico Abajo")
        else:
            print ("Parametro incorrecto")
    elif name == "Golpe":
        print ("Funcion Golpe Llamada")
    elif name == "Vibrato":
        print ("Funcion Vibrato Llamada" + str(param))




def Metronomo(param,speed):
    global metronome
    if param == "A":
        if metronome:
            PrintText("Metronomo Ya esta activado")
        else:
            metronome = True
            PrintText("Se ha activado el metronomo")
    else:
        if metronome:
            metronome = False
            PrintText("Se ha desactivado el metronomo")
        else:
            PrintText("Metronomo Ya esta desactivado")

def PrintText(text):
    box.configure(state="normal")
    box.insert("end", text + "\n")
    box.configure(state="disabled")


class statement_set():
    def __init__(self,var,sentence):

        self.type = "set"
        self.var = var
        self.sentence = sentence

    def GetType(self):
        return self.type

    def GetSentence(self):
        return self.sentence

    def Execute(self,vars):
        value = self.sentence.Execute(vars)
        if (value == "Error"):
            pass
        elif (self.sentence.GetType() == "operation"):
            var = Var(self.var, value, "int")
            return var
        elif (value == "Funcion"): #CAMBIAR POR ALGO QUE DETECTE LAS FUNCIONES
            return "Error"
        elif (value == "str"):
            var = Var(self.var, value, "str")
            return var

class statement_for():
    def __init__(self, name):
        self.name = name
        self.type = "state"

    def GetType(self):
        return self.type

    def Execute(self):
        pass


class statement_if():
    def __init__(self, name):
        self.name = name
        self.type = "state"

    def GetType(self):
        return self.type

    def Execute(self):
        pass


class statement_EnCaso():
    def __init__(self, name):
        self.name = name
        self.type = "state"

    def GetType(self):
        return self.type

    def Execute(self):
        pass

class statement_DEF():
    def __init__(self, name,block):
        self.name = name
        self.block = block
        self.type = "def"
        self.vars = []
        methods.append(self)

    def GetType(self):
        return self.type

    def GetName(self):
        return self.name

    def GetBlock(self):
        return self.block

    def Execute(self):
        temp = self.block
        temp2 = None
        while (temp != None):
            if (type(temp) != YaccSymbol):
                if (len(temp) > 1):
                    temp2 = temp[0].value

                else:
                    temp2 = temp[0].value
            else:
                temp2 = temp.value
        #COMIENZA EJECUCION DE BLOQUES SEGUN EL TIPO DE BLOQUES
            if (temp2.GetType() == "set"):

                new_var = temp2.GetAction().Execute(self.vars)
                if (self.name == "@Principal"):
                    global_vars.append(new_var)
                else:
                    self.vars.append(new_var)

            elif (temp2.GetType() == "sentence"):
                if temp2.GetAction().GetType() == "function":
                    res = temp2.GetAction().Execute(self.vars)
                    if (res == "Error"):
                        PrintText("Error en la funcion introducida en linea " + str(temp2.GetAction().GetLine()))
                        break


            elif (temp2.GetType() == "print"):
                temp2.GetAction().Execute(self.vars)
            elif (temp2.GetType() == "def"):
                pass

            if (type(temp) == YaccSymbol): #al final
                temp = None
            else:
                temp = temp[1].value


class PrintConsole():
    def __init__(self, id,sentence):
        self.sentence = sentence
        self.outputBox = box
        self.type = type
        self.text = ""
        self.vars = []
        self.type = "print"

    def Execute(self,vars):
        self.vars = vars
        if(self.sentence.GetType() != "function"):
            self.text = str(self.sentence.Execute(self.vars))
            self.Insert()
            return ("Exito")
        else:
            return ("Error")

    def Insert(self):
        self.outputBox.configure(state="normal")
        self.outputBox.insert("end", self.text + "\n")
        self.outputBox.configure(state="disabled")


class sentence():

    def __init__(self,value,sentype,line):
        self.value = value
        self.sentype = sentype
        self.vars = []
        self.line = line
        

    def GetValue(self):
        return self.value

    def GetType(self):
        return self.sentype

    def GetLine(self):
        return self.line

    def Execute(self,vars):
        self.vars = vars
        #print(global_vars)
        if (self.sentype == "str"):
            new_op = self.SwitchVars(self.value)
            new_op.split(",")
            res = ""
            for i in new_op:
                res += str(i)
            print("FinalRes = " + str(res))
            return res
        elif self.sentype == "operation":

            type = self.VerifyOp(self.value)
            #print(type) 40.42
            if (type == "num_var"):

                new_op = self.SwitchVars(self.value)
                #print("new_op: "+new_op)
                res = self.FormList(new_op)
                return res
            elif (type == "string"):
                new_op = self.SwitchVars(self.value)
                new_op.split(",")
                res = ""
                for i in new_op:
                    res += str(i)
                print("FinalRes = " + str(res))
                return res
            else:
                pass

        elif self.sentype == "function":
            split = self.value.split("$")
            #print("split: ", split)

            if (split[0] == "Golpe"):
                Funciones(split[0],"none")
                return "Exito"
            elif (split[0] == "Percutor" or split[0] == "Abanico" or split[0] == "Vertical" or split[0] == "Vibrato"):
                if split[0] == "Vibrato":
                    try:
                        num = split[1].replace(",","")
                        int(num)
                        Funciones(split[0],int(num))

                        return "Exito"
                    except (ValueError):
                        return "Error"
                elif split[0] == "Vertical":
                    if (split[1] == "D" or split[1] == "I"):
                        Funciones(split[0],split[1])
                        return "Exito"
                    else:
                        return "Error"
                elif split[0] == "Abanico":
                    if (split[1] == "A" or split[1] == "B"):
                        Funciones(split[0],split[1])
                        return "Exito"
                    else:
                        return "Error"
                elif split[0] == "Percutor":
                    if (split[1] == "D" or split[1] == "I" or split[1] == "A" or split[1] == "B" or split[1] == "AB" or split[1] == "DI"):
                        Funciones(split[0],split[1])
                        return "Exito"
                    else:
                        return "Error"
                else:
                    return "Error"
            elif split[0] == "Metronomo":
                if (split[1]=="A" or split[1] == "D"):
                    try:
                        num = split[2].replace(",","")
                        int(num)
                        Metronomo(split[1],int(num))
                        return "Exito"
                    except (ValueError):
                        return "Error"
                else:
                    return "Error"
            else:
                return "Error"


    def SwitchVars(self,op):

        new_op = op.replace("(","")
        new_op = new_op.replace(")","")
        op_split = op.split(",")[0:-1]

        for i in op_split:
            if self.vars != []:
                for j in self.vars:
                    name = j.GetName()
                    if i == name and j.GetType() == "int" or j.GetType() == "str":
                        op = op.replace(name,str(j.GetValue()))
            if global_vars != []:
                for j in global_vars:
                    name = j.GetName()
                    if i == name and j.GetType() == "int" or j.GetType() == "str":
                        op = op.replace(name,str(j.GetValue()))
            for j in global_vars:
                if i == j.GetName() and j.GetType() == "int" or j.GetType() == "str":
                    op = op.replace(j.GetName(), str(j.GetValue()).replace('"', ''))
        return op


    def CheckPar(self,opstr):

        started = False
        another = 0
        parlist = []
        par = ""
        i=0
        while i < len(opstr):
            if not started:
                if opstr[i] == "(":
                    started = True
                    i+=1

            else:
                if opstr[i] == "(":
                    another+=1
                elif (opstr[i] == ")" and another > 0):
                    another -=1
                elif (opstr[i]==")" and another == 0):
                    started = False
                    parlist += [par]
                    par = ""
                    i+=1
                par += opstr[i]
            i+=1

        if parlist != []:
            for i in range (0,len(parlist)):
                if (parlist[i][0]!= ","):
                    parlist[i] = ","+parlist[i]
                lalala = "("+parlist[i]+")"
                laalala = str(self.FormList(parlist[i]))
                opstr = opstr.replace(lalala,laalala)
        return opstr

    def FormList(self,opstr):

        checked_op = self.CheckPar(opstr)

        if (checked_op[0] == ","):
            checked_op = checked_op[1:-1]
        else:
            checked_op = checked_op[0:-1]

        result = Solve(checked_op.split(","))

        return result

    def VerifyOp(self,op):
        string = False
        num_var = False

        op_split = op.split(",")[0:-1]
        for i in op_split:
            if ",#str in " in i:
                string = True
                self.value = self.value.replace(",#str","")
                self.value = self.value.replace('"','')
            elif i == "(" or i in sec_symbols or i in prim_symbols or i == ")":
                pass
            else:
                try:
                    float(i)
                    num_var = True
                except(ValueError):
                    if (i[0] == "@"):
                        num_var = True
                    else:
                        string = True

        if string:
            return "string"
        elif num_var:
            return "num_var"
        else:
            return "Error"


class Block():

    def __init__(self, accion, block_type):
        self.action = accion
        self.type = block_type
        self.next = None

    def SetNext(self,next):
        self.next = next

    def GetNext(self):
        return self.next

    def GetAction(self):
        return self.action

    def GetType(self):
        return self.type

    def Execute(self,vars):
        self.action.Execute(vars)


class Var():

    def __init__(self,name,value,type):
        self.name = name
        self.value = value
        self.type = type

    def SetName(self,name):
        self.name = name

    def GetName(self):
        return self.name

    def SetValue(self,value):
        self.value = value

    def GetValue(self):
        return self.value

    def GetType(self):
        return self.type