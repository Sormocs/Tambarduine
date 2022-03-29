nums = "0123456789"
prim_symbols = ["*", "%", "//", "/"]
sec_symbols = ["+", "-"]

global_vars = []
methods = []

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
        print(op)
        res = 0
    return int(op[0])


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

    print(res)
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
    print(res)
    return res


def Funciones(name,param):

    if name == "Percutor":
        if param == "A":
            print ("Funcion Golpe Arriba")
        elif param == "B":
            print ("Funcion Golpe Abajo")
        elif param == "D":
            print("Funcion Golpe Derecha")
        elif param == "I":
            print ("Funcion Golpe Izquierda")
        elif param == "DI":
            print ("Funcion Golpe Derecha e Izquierda")
        elif param == "AB":
            print ("Funcion Golpe Arriba y Abajo")
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
    else:
        print ("Funcion Incorrecta")




def Metronomo(name,param,speed):
    if (name != "Metronomo"):
        pass
    else:
        print ("Funcion incorrecta llamada")


class statement_set():
    def __init__(self,var,sentence):

        self.type = "set"
        self.var = var
        self.sentence = sentence

    def GetType(self):
        return self.type

    def GetSentence(self):
        return self.sentence

    def Execute(self):

        var = Var(self.var,self.sentence)
#
#
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
        methods.append(self)

    def GetType(self):
        return self.type

    def GetName(self):
        return self.name

    def GetBlock(self):
        return self.block

    def Execute(self):
        print("Executing...")
        temp = self.block
        while (temp != None):
            print(self.block.GetBlock().GetType())
            if (self.block.type == "sentence"):
                print("Sentence Bloque: "+ self.block.GetBlock().GetValue())
            else:
                print("Statement Bloque:"+ self.block.GetBlock().GetType())
            temp = temp.GetNext()

class print():
    def __init__(self, name):
        self.name = name

    def Execute(self):
        pass

class sentence():


    def __init__(self,value, sentype):

        self.value = value
        self.sentype = sentype
        self.next = None

    def __int__(self,value,sentype):
        self.value = value
        self.sentype = sentype

    def SetNext(self,next):
        self.next = next

    def GetNext(self):
        return self.next

    def GetValue(self):
        return self.value

    def GetType(self):
        return self.sentype

    def Execute(self):
        if self.sentype == "operation":
            print("Sentence OP")

class Block():

    def __init__(self,block,block_type):
        self.block = block
        self.type = block_type
        self.next = None

    def SetNext(self,next):
        self.next = next

    def GetNext(self):
        return self.next

    def GetBlock(self):
        return self.block

    def GetType(self):
        return self.type


class Var():

    def __init__(self,name,value):
        self.name = name
        self.value = value

    def SetName(self,name):
        self.name = name

    def GetName(self):
        return self.name

    def SetValue(self,value):
        self.value = value

    def GetValue(self):
        return self.value