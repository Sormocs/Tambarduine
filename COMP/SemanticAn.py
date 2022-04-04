from COMP.ply.yacc import YaccSymbol
from COMP import ListInstructions

nums = "0123456789"
prim_symbols = ["*", "%", "//", "/"]
sec_symbols = ["+", "-"]

global_vars = []
methods = []

metronome = False

box = None

instruccions = None

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
                    res1 += [float(new_op[i]) * float(new_op[i + 2])]
                elif new_op[i + 1] == "%":
                    res1 += [float(new_op[i]) % float(new_op[i + 2])]
                elif new_op[i + 1] == "//":
                    res1 += [float(new_op[i]) // float(new_op[i + 2])]
                elif new_op[i + 1] == "/":
                    res1 += [float(new_op[i]) / float(new_op[i + 2])]
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

def CreateListInstruccions():
    global instruccions, metronome

    metronome = False

    if instruccions == None:

        instruccions = ListInstructions.ListInstructions()

def StartArduinoExecution():

    instruccions.execute()

def Funciones(name, param):
    if name == "Percutor":

        print("Se agrego una funcion de Percutor", param)
        instruccions.add("Percutor", param)

    elif name == "Abanico":

        print("Se agrego una funcion de Abanico", param)
        instruccions.add("Abanico", param)

    elif name == "Vertical":

        print("Se agrego una funcion de Vertical", param)
        instruccions.add("Vertical", param)

    elif name == "Golpe":

        print("Se agrego una funcion de Golpe", param)
        instruccions.add("Golpe", param)

    elif name == "Vibrato":

        print("Se agrego una funcion de Vibrato", param)
        instruccions.add("Vibrato", param)


def Metronomo(param, speed):
    global metronome
    if param == "A":
        if metronome:
            PrintText("Metronomo Ya esta activado")
            instruccions.add("Metronomo", speed)
        else:
            metronome = True
            instruccions.add("Metronomo", speed)
            PrintText("Se ha activado el metronomo")
    else:
        if metronome:
            metronome = False
            PrintText("Se ha desactivado el metronomo")
            instruccions.metronoOff()
        else:
            PrintText("Metronomo Ya esta desactivado")
            instruccions.metronoOff()


def PrintText(text):
    box.configure(state="normal")
    box.insert("end", text + "\n")
    box.configure(state="disabled")


class statement_set():
    def __init__(self, var, sentence):

        self.type = "set"
        self.var = var
        self.sentence = sentence

    def GetType(self):
        return self.type

    def GetSentence(self):
        return self.sentence

    def Execute(self, vars,location):
        self.location = location
        value = self.sentence.Execute(vars,location)
        if (value == "Error"):
            return "Error"
        elif (self.sentence.GetType() == "operation"):
            var = Var(self.var, value, "int")
            return var
        elif (self.sentence.GetType() == "function"):
            return "Error"
        elif (self.sentence.GetType() == "str"):
            var = Var(self.var, value, "str")
            return var
        elif (value == "true" or value == "false"):
            var = Var(self.var, value, "bool")
            return var
        else:
            return "Error"


class statement_for():
    def __init__(self, var, max, step_num, block):
        self.var = var
        self.max = max
        self.step_num = step_num
        self.block = block
        self.type = "statement_for"
        self.vars = []
        self.location = None

    def GetType(self):
        return self.type

    def Execute(self, vars, location):
        self.vars = vars
        self.location = location
        temp_var = Var(self.var, 0, "int")
        skip = 0
        if self.location.GetName == "@Principal":
            global_vars.append(temp_var)
        else:
            self.location.GetVars().append(temp_var)
        for i in range(0, self.max, self.step_num):
            temp_var.SetValue(i)
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
                # COMIENZA EJECUCION DE BLOQUES SEGUN EL TIPO DE BLOQUES
                if (temp2.GetType() == "set"):

                    new_var = temp2.GetAction().Execute(self.location.GetVars())
                    if new_var != "Error":

                        if (self.location.GetName() == "@Principal"):
                            global_vars.append(new_var)
                        else:
                            self.vars.append(new_var)

                    else:
                        PrintText("Error en set de la funcion principal " + self.location.GetName())
                        break

                elif (temp2.GetType() == "sentence"):
                    if temp2.GetAction().GetType() == "function":
                        res = temp2.GetAction().Execute(self.vars,self.location)
                        if (res == "Error"):
                            PrintText("Error en la funcion introducida en linea " + str(temp2.GetAction().GetLine()))
                            break

                elif (temp2.GetType() == "statement_if"):
                    res = temp2.GetAction().Execute(self.vars, self.location)
                    if (res == "Error"):
                        PrintText("Error en statement if en " + str(temp2.GetAction().GetLine()))
                        break

                elif (temp2.GetType() == "statement_for"):
                    res = res = temp2.GetAction().Execute(self.vars, self)
                    if(res == "Error"):
                        PrintText("Error en statement for en linea" + str(temp2.GetAction().GetLine()))

                elif (temp2.GetType() == "encaso"):
                    pass

                elif (temp2.GetType() == "print"):
                    res = temp2.GetAction().Execute(self.vars, self.location)
                    if res == "Error":
                        PrintText("Error en print en " + str(temp2.GetAction().GetLine()))
                        break

                elif (temp2.GetType() == "def"):
                    PrintText("Error: def dentro de for")
                    return "Error"

                elif (temp2.GetType() == "special_set"):
                    res = temp2.Execute(self.vars, self.location)
                    if (res == "Error"):
                        PrintText("Error en statement set en " + self.location.GetName())
                        return "Error"

                if (type(temp) == YaccSymbol):  # al final
                    temp = None
                else:
                    temp = temp[1].value


class statement_if():

    def __init__(self, relation, block, else_block, isElse):
        self.type = "if"
        self.relation = relation
        self.block = block
        self.else_block = else_block
        self.isElse = isElse
        self.location = None
        self.vars = []

    def GetType(self):
        return self.type

    def Execute(self, vars, location):
        self.location = location
        self.vars = vars
        if self.relation.GetType() == "relation":

            flag = self.relation.Execute(self.vars,location)
            print(flag)
            if flag == "Error":
                PrintText("Error en la condicion del if " + self.block.GetAction().GetLine())
                return "Error"
            else:
                if not self.isElse:
                    # CODIGO SIN ELSE
                    if self.relation.Execute(vars,location):
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
                            # COMIENZA EJECUCION DE BLOQUES SEGUN EL TIPO DE BLOQUES
                            if (temp2.GetType() == "set"):

                                new_var = temp2.GetAction().Execute(self.vars,self.location)
                                if new_var != "Error":

                                    if (self.location.GetName() == "@Principal"):
                                        global_vars.append(new_var)
                                    else:
                                        self.location.GetVars().append(new_var)

                                else:
                                    PrintText("Error en la ejecucion de la funcion " + self.location.GetName() + " en un set")
                                    break

                            elif (temp2.GetType() == "sentence"):
                                if temp2.GetAction().GetType() == "function":
                                    res = temp2.GetAction().Execute(self.location.GetVars(), self.location)
                                    if (res == "Error"):
                                        PrintText(
                                            "Error en la funcion introducida en linea " + str(temp2.GetAction().GetLine()))
                                        return "Error"

                            elif (temp2.GetType() == "statement_if"):
                                res = temp2.GetAction().Execute(self.location.GetVars(), self.location)
                                if (res == "Error"):
                                    PrintText("Error en statement if en rutina" + self.location.GetName())
                                    return "Error"


                            elif (temp2.GetType() == "statement_for"):
                                res = res = temp2.GetAction().Execute(self.vars, self)
                                if (res == "Error"):
                                    PrintText("Error en statement if en linea" + str(temp2.GetAction().GetLine()))

                            elif (temp2.GetType() == "encaso"):
                                pass

                            elif (temp2.GetType() == "print"):
                                res = temp2.GetAction().Execute(self.vars,self.location)
                                if (res == "Error"):
                                    PrintText("Error en la impresion de linea " + str(temp2.GetAction().GetLine()))

                            elif (temp2.GetType() == "def"):
                                PrintText("Error en la definicion de funcion en linea " + str(temp2.GetAction().GetLine()))
                                return "Error"

                            elif (temp2.GetType() == "special_set"):
                                res = temp2.Execute(self.vars, self.location)
                                if (res == "Error"):
                                    PrintText("Error en statement set en " + self.location.GetName())
                                    return "Error"

                            if (type(temp) == YaccSymbol):  # al final
                                temp = None
                            else:
                                temp = temp[1].value

                    else:
                        pass
                else:
                    # CODIGO CON ELSE PRESENTE
                    if self.relation.Execute():
                        temp = self.block
                    else:
                        temp = self.else_block
                    temp2 = None
                    while (temp != None):
                        if (type(temp) != YaccSymbol):
                            if (len(temp) > 1):
                                temp2 = temp[0].value

                            else:
                                temp2 = temp[0].value
                        else:
                            temp2 = temp.value
                        # COMIENZA EJECUCION DE BLOQUES SEGUN EL TIPO DE BLOQUES
                        if (temp2.GetType() == "set"):

                            new_var = temp2.GetAction().Execute(self.vars,self.location)
                            if new_var != "Error":

                                if (self.location.GetName() == "@Principal"):
                                    global_vars.append(new_var)
                                else:
                                    self.vars.append(new_var)

                            else:
                                PrintText("Error en la ejecucion de la funcion " + self.location.GetName() + " en un set")
                                break

                        elif (temp2.GetType() == "sentence"):
                            if temp2.GetAction().GetType() == "function":
                                res = temp2.GetAction().Execute(self.vars)
                                if (res == "Error"):
                                    PrintText("Error en la funcion introducida en linea " + str(temp2.GetAction().GetLine()))
                                    break

                        elif (temp2.GetType() == "statement_if"):
                            res = temp2.GetAction().Execute(self.vars, self)
                            if (res == "Error"):
                                PrintText("Error en statement if en " + str(temp2.GetAction().GetLine()))
                                break

                        elif (temp2.GetType() == "statement_for"):
                            res = temp2.GetAction().Execute(self.vars, self)
                            if (res == "Error"):
                                PrintText("Error en statement for en " + self.name)
                                break

                        elif (temp2.GetType() == "encaso"):
                            pass

                        elif (temp2.GetType() == "print"):
                            temp2.GetAction().Execute(self.vars,self.location)

                        elif (temp2.GetType() == "def"):
                            PrintText("Error: funcion dentro de funcion")
                            break

                        elif (temp2.GetType() == "special_set"):
                            res = temp2.Execute(self.vars, self.location)
                            if (res == "Error"):
                                PrintText("Error en statement set en " + self.location.GetName())
                                return "Error"

                        if (type(temp) == YaccSymbol):  # al final
                            temp = None
                        else:
                            temp = temp[1].value

        else:
            return "Error"


class statement_DEF():
    def __init__(self, name, block):
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

    def GetVars(self):
        return self.vars

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
            # COMIENZA EJECUCION DE BLOQUES SEGUN EL TIPO DE BLOQUES
            if (temp2.GetType() == "set"):

                new_var = temp2.GetAction().Execute(self.vars,self)
                if new_var != "Error":

                    if (self.name == "@Principal"):
                        global_vars.append(new_var)
                    else:
                        self.vars.append(new_var)

                else:
                    PrintText("Error en set de la funcion principal " + self.name)
                    break

            elif (temp2.GetType() == "sentence"):
                if temp2.GetAction().GetType() == "function":
                    res = temp2.GetAction().Execute(self.vars,self)
                    if (res == "Error"):
                        PrintText("Error en la funcion introducida en linea " + str(temp2.GetAction().GetLine()))
                        break

            elif (temp2.GetType() == "statement_if"):
                print("llama a statement if")
                res = temp2.GetAction().Execute(self.vars, self)
                if (res == "Error"):
                    PrintText("Error en statement if en "+self.name)
                    break

            elif (temp2.GetType() == "statement_for"):
                res = temp2.GetAction().Execute(self.vars, self)
                if (res == "Error"):
                    PrintText("Error en statement for en "+self.name)
                    break


            elif (temp2.GetType() == "encaso"):

                res = temp2.Execute(self.vars, self)
                if (res == "Error"):
                    PrintText("Error en statement encaso en " + self.name)
                    break


            elif (temp2.GetType() == "print"):

                res = temp2.GetAction().Execute(self.vars, self)
                if res == "Error":
                    print("Error en print en " + str(temp2.GetAction().GetLine()))
                    return "Error"

            elif (temp2.GetType() == "def"):
                PrintText("Error: funcion dentro de funcion")
                return "Error"

            elif (temp2.GetType() == "special_set"):
                res = temp2.Execute(self.vars, self)
                if (res == "Error"):
                    PrintText("Error en statement set en " + self.GetName())
                    return "Error"

            if (type(temp) == YaccSymbol):  # al final
                temp = None
            else:
                temp = temp[1].value


class PrintConsole():
    def __init__(self, id, sentence,data_type):
        self.sentence = sentence
        self.outputBox = box
        self.type = type
        self.text = ""
        self.vars = []
        self.type = "print"
        self.id = id.replace("#id", "")
        self.data_type = data_type

    def Execute(self, vars,location):
        print("Print llamado con valor ",self.sentence)
        self.location = location
        if self.id == "println!":
            if self.data_type == "var":
                if self.vars != []:
                    for i in self.vars:
                        if i.GetName() == self.sentence:
                            self.text = str(i.GetValue())
                            self.Insert()
                            return "Exito"
                    PrintText("Error en print en linea " + str(self.sentence.GetLine()))
                    return "Error"
                if global_vars != []:
                    for i in global_vars:
                        if i.GetName() == self.sentence:
                            self.text = str(i.GetValue())
                            self.Insert()
                            return "Exito"
            else:
                self.vars = vars
                if (self.sentence.GetType() != "function"):
                    #print(self.sentence.GetValue())
                    self.text = str(self.sentence.Execute(self.vars,self.location))
                    self.Insert()
                    return "Exito"
                else:
                    return "Error"
        else:
            return "Error"

    def Insert(self):
        self.outputBox.configure(state="normal")
        self.outputBox.insert("end", self.text.replace("+", " ") + "\n")
        self.outputBox.configure(state="disabled")


class sentence():

    def __init__(self, value, sentype, line):
        self.value = value
        self.sentype = sentype
        self.vars = []
        self.line = line
        if self.sentype == "true":
            self.value = "true"
        elif self.sentype == "false":
            self.value = "false"

    def GetValue(self):
        return self.value

    def GetType(self):
        return self.sentype

    def GetLine(self):
        return self.line

    def Execute(self, vars,location):
        self.location = location
        self.vars = vars
        if (self.sentype == "str"):

            new_str = self.SwitchVars(self.value)
            str_list = new_str.split(",")
            res = ""
            for i in str_list:
                if i == "+":
                    pass
                elif i not in "/*-%":
                    res += str(i)
                else:
                    PrintText("Error de operacion con string, solo soporta +")
                    return "Error"
            # print("FinalString = " + str(res))
            return res
        elif (self.sentype == "true"):
            return "true"
        elif (self.sentype == "false"):
            return "false"
        elif (self.sentype == "relation"):
            splited = self.value.split("$")
            flag = self.SolveRelation(splited)
            return flag

        elif self.sentype == "operation":

            new_op = self.SwitchVars(self.value)
            if (new_op == "Error"):
                return "Error"
            else:
                if self.sentype == "operation":
                    res = self.FormList(new_op)
                    return res
        elif (self.sentype == "type"):
            split_val = self.value.split("&")
            if (split_val[0] == "type"):
                print(split_val[1])
                for i in self.vars:
                    if i.GetName() == split_val[1]:
                        # PrintText("Tipo de variable " + split_val[1] + " = " + i.GetType())
                        return i.GetType()
                for i in global_vars:
                    if i.GetName() == split_val[1]:
                        # PrintText("Tipo de variable " + split_val[1] + " = " + i.GetType())
                        return i.GetType()
                PrintText("Error: Variable no encontrada")
                return "Error"
            else:
                PrintText("Error: Funcion introducida no existe")
                return "Error"

        elif self.sentype == "function":
            # print("ENTRO A FUNCTION")
            split = self.value.split("$")

            if (split[0] == "Golpe"):
                Funciones(split[0], "none")
                return "Exito"
            elif (split[0] == "Percutor" or split[0] == "Abanico" or split[0] == "Vertical" or split[0] == "Vibrato"):
                if split[0] == "Vibrato":
                    try:
                        num = split[1].replace(",", "")
                        int(num)
                        Funciones(split[0], int(num))

                        return "Exito"
                    except (ValueError):
                        PrintText("Error: Numero de vibrato no valido")
                        return "Error"
                elif split[0] == "Vertical":
                    if (split[1] == "D" or split[1] == "I"):
                        Funciones(split[0], split[1])
                        return "Exito"
                    else:
                        PrintText("Error: Direccion de vertical no valida")
                        return "Error"
                elif split[0] == "Abanico":
                    if (split[1] == "A" or split[1] == "B"):
                        Funciones(split[0], split[1])
                        return "Exito"
                    else:
                        PrintText("Error: Direccion de abanico no valida")
                        return "Error"
                elif split[0] == "Percutor":
                    if (split[1] == "D" or split[1] == "I" or split[1] == "A" or split[1] == "B" or split[1] == "AB" or
                            split[1] == "DI"):
                        Funciones(split[0], split[1])
                        return "Exito"
                    else:
                        PrintText("Error: Direccion de percutor no valida")
                        return "Error"
                else:
                    return "Error"
            elif split[0] == "Metronomo":
                if (split[1] == "A" or split[1] == "D"):
                    try:
                        num = split[2].replace(",", "")
                        int(num)
                        Metronomo(split[1], int(num))
                        return "Exito"
                    except (ValueError):
                        PrintText("Error: Numero de metronomo no valido")
                        return "Error"
                else:
                    PrintText("Error: Parametro de metronomo no valida")
                    return "Error"
            else:
                PrintText("Error: Funcion introducida no existe")
                return "Error"
        else:
            PrintText("Error: Sentencia" + self.sentype + "no reconocida")

    def SwitchVars(self, op):
        new_op = op.replace("(", "")
        new_op = new_op.replace(")", "")
        if new_op[-1] == ",":
            op_split = op.split(",")[0:-1]
        else:
            op_split = op.split(",")
        for i in op_split:
            if i[0] == "@":
                val = self.ReplaceVar(i)
                if val != "Error":
                    op = op.replace(i, str(val))
                else:
                    return "Error"
            else:
                pass
        return op

    def ReplaceVar(self, name):
        for i in self.vars:
            var_name = i.GetName().replace("+", "")
            if i.GetName() == name:
                return i.GetValue()
            if i.GetType() == "str":
                if self.sentype != "relation":
                    self.sentype = "str"
        for i in global_vars:
            if i.GetName() == name:
                return i.GetValue()
            if i.GetType() == "str":
                if self.sentype != "relation":
                    self.sentype = "str"
        PrintText("Error: Variable no encontrada")
        return "Error"

    def CheckPar(self, opstr):
        started = False
        another = 0
        parlist = []
        par = ""
        i = 0
        while i < len(opstr):
            if not started:
                if opstr[i] == "(":
                    started = True
                    i += 1

            else:
                if opstr[i] == "(":
                    another += 1
                elif (opstr[i] == ")" and another > 0):
                    another -= 1
                elif (opstr[i] == ")" and another == 0):
                    started = False
                    parlist += [par]
                    par = ""
                    i += 1
                par += opstr[i]
            i += 1

        if parlist != []:
            for i in range(0, len(parlist)):
                if (parlist[i][0] != ","):
                    parlist[i] = "," + parlist[i]
                lalala = "(" + parlist[i] + ")"
                laalala = str(self.FormList(parlist[i]))
                opstr = opstr.replace(lalala, laalala)
        return opstr

    def FormList(self, opstr):

        checked_op = self.CheckPar(opstr)

        if (checked_op[0] == ","):
            checked_op = checked_op[1:-1]
        elif (checked_op[-1] == ","):
            checked_op = checked_op[0:-1]

        result = Solve(checked_op.split(","))

        return result

    def VerifyOp(self, op):
        string = False
        num_var = False
        # print("op in verifyop: "+op)
        op_split = op.split(",")[0:-1]
        if len(op_split) == 1:
            num_var = True
        for i in op_split:

            if i == "(" or i in sec_symbols or i in prim_symbols or i == ")":
                pass
            else:
                try:
                    float(i)
                    num_var = True
                except(ValueError):
                    # print(i[0])
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

    def SolveRelation(self,split):
        if split[-1] == "NUM_NUM":
            if split[1] == ">":
                if float(split[0]) > float(split[2]):
                    return True
            if split[1] == "<":
                if float(split[0]) < float(split[2]):
                    return True
            if split[1] == ">=":
                if float(split[0]) >= float(split[2]):
                    return True
            if split[1] == "<=":
                if float(split[0]) <= float(split[2]):
                    return True
            if split[1] == "==":
                if float(split[0]) == float(split[2]):
                    return True
            if split[1] == "<>":
                if float(split[0]) != float(split[2]):
                    return True
            else:
                return False
        elif split[-1] == "NUM_VAR":
            var = self.GetVar(split[2])
            if var != "Error" and var.GetType() == "int":
                if split[1] == ">":
                    if float(split[0]) > float(var.GetValue()):
                        return True
                if split[1] == "<":
                    if float(split[0]) < float(var.GetValue()):
                        return True
                if split[1] == ">=":
                    if float(split[0]) >= float(var.GetValue()):
                        return True
                if split[1] == "<=":
                    if float(split[0]) <= float(var.GetValue()):
                        return True
                if split[1] == "==":
                    if float(split[0]) == float(var.GetValue()):
                        return True
                if split[1] == "<>":
                    if float(split[0]) != float(var.GetValue()):
                        return True
                else:
                    return False
            else:
                return "Error"

        elif split[-1] == "VAR_VAR":
            var1 = self.GetVar(split[0])
            var2 = self.GetVar(split[2])
            if var1 != "Error" and var2 != "Error":
                if var1.GetType() == "int" and var2.GetType() == "int":
                    if split[1] == ">":
                        if float(var1.GetValue()) > float(var2.GetValue()):
                            return True
                    if split[1] == "<":
                        if float(var1.GetValue()) < float(var2.GetValue()):
                            return True
                    if split[1] == ">=":
                        if float(var1.GetValue()) >= float(var2.GetValue()):
                            return True
                    if split[1] == "<=":
                        if float(var1.GetValue()) <= float(var2.GetValue()):
                            return True
                    if split[1] == "==":
                        if float(var1.GetValue()) == float(var2.GetValue()):
                            return True
                    if split[1] == "<>":
                        if float(var1.GetValue()) != float(var2.GetValue()):
                            return True
                else:
                    PrintText("Error: No se puede realizar comparacion, linea " + str(self.line))
                    return "Error"
            else:
                PrintText("Error: Variable no definida, linea " + str(self.line))
                return "Error"
        elif split[-1] == "VAR_NUM":
            var = self.GetVar(split[0])
            if var != "Error" and var.GetType() == "int":
                if split[1] == ">":
                    if float(var.GetValue()) > float(split[2]):
                        return True
                if split[1] == "<":
                    if float(var.GetValue()) < float(split[2]):
                        return True
                if split[1] == ">=":
                    if float(var.GetValue()) >= float(split[2]):
                        return True
                if split[1] == "<=":
                    if float(var.GetValue()) <= float(split[2]):
                        return True
                if split[1] == "==":
                    if float(var.GetValue()) == float(split[2]):
                        return True
                if split[1] == "<>":
                    if float(var.GetValue()) != float(split[2]):
                        return True
                else:
                    return False
            else:
                PrintText("Error: Variable no definida, linea " + str(self.line))
                return "Error"
        elif split[-1] == "VAR_STR":
            var = self.GetVar(split[0])
            if var != "Error" and var.GetType() == "string":
                if split[1] == "==":
                    if var.GetValue() == split[2]:
                        return True
                if split[1] == "<>":
                    if var.GetValue() != split[2]:
                        return True
                if split[1] == ">" or split[1] == "<" or split[1] == ">=" or split[1] == "<=":
                    PrintText("Error: No se puede realizar comparacion, linea " + str(self.line))
                    return "Error"
                else:
                    return False
            else:
                PrintText("Error: Variable no definida, linea " + str(self.line))
                return "Error"
        elif split[-1] == "STR_STR":
            if split[1] == "==":
                if split[0] == split[2]:
                    return True
            if split[1] == "<>":
                if split[0] != split[2]:
                    return True
            if split[1] == ">" or split[1] == "<" or split[1] == ">=" or split[1] == "<=":
                PrintText("Error: No se puede realizar comparacion, linea " + str(self.line))
                return "Error"
            else:
                return False
        elif split[-1] == "VAR_BOOL":
            var = self.GetVar(split[0])
            if var != "Error" and var.GetType() == "bool":
                if split[1] == "==":
                    if var.GetValue() == split[2]:
                        return True
                if split[1] == "<>":
                    if var.GetValue() != split[2]:
                        return True
                if split[1] == ">" or split[1] == "<" or split[1] == ">=" or split[1] == "<=":
                    PrintText("Error: No se puede realizar comparacion, linea " + str(self.line))
                    return "Error"
                else:
                    return False
            else:
                PrintText("Error: Variable no definida, linea " + str(self.line))
                return "Error"
        elif split[-1] == "BOOL_VAR":
            var = self.GetVar(split[0])
            if var != "Error" and var.GetType() == "bool":
                if split[1] == "==":
                    if var.GetValue() == split[2]:
                        return True
                if split[1] == "<>":
                    if var.GetValue() != split[2]:
                        return True
                if split[1] == ">" or split[1] == "<" or split[1] == ">=" or split[1] == "<=":
                    PrintText("Error: No se puede realizar comparacion, linea " + str(self.line))
                    return "Error"
                else:
                    return False
            else:
                PrintText("Error: Variable no definida, linea " + str(self.line))
                return "Error"


    def GetVar(self,name):
        if self.vars != []:
            for i in self.vars:
                if i.GetName() == name:
                    return i
        if global_vars != []:
            for i in global_vars:
                if i.GetName() == name:
                    return i
        PrintText("Error: Variable not found")
        return "Error"

class Block():

    def __init__(self, accion, block_type):
        self.action = accion
        self.type = block_type
        self.next = None

    def SetNext(self, next):
        self.next = next

    def GetNext(self):
        return self.next

    def GetAction(self):
        return self.action

    def GetType(self):
        return self.type

    def Execute(self, vars, location):
        self.action.Execute(vars,location)


class Var():

    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

    def SetType(self, type):
        self.type = type

    def SetName(self, name):
        self.name = name

    def GetName(self):
        return self.name

    def SetValue(self, value):
        self.value = value

    def GetValue(self):
        return self.value

    def GetType(self):
        return self.type


class CuandoStatement():

    def __init__(self,relation,block):

        self.relation = relation
        self.block = block

    def GetRelation(self):
        return self.relation

    def Execute(self,vars,location):
        self.vars = vars
        self.location = location
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
            # COMIENZA EJECUCION DE BLOQUES SEGUN EL TIPO DE BLOQUES
            if (temp2.GetType() == "set"):

                PrintText("Error: No se puede ejecutar un bloque SET, linea " + str(self.location))
                return "Error"

            elif (temp2.GetType() == "sentence"):
                if temp2.GetAction().GetType() == "function":
                    res = temp2.GetAction().Execute(self.vars)
                    if (res == "Error"):
                        PrintText("Error en la funcion introducida en linea " + str(temp2.GetAction().GetLine()))
                        return "Error"

            elif (temp2.GetType() == "statement_if"):
                res = temp2.GetAction().Execute(self.vars, self)
                if (res == "Error"):
                    PrintText("Error en statement if en " + str(temp2.GetAction().GetLine()))
                    return "Error"

            elif (temp2.GetType() == "statement_for"):
                res = temp2.GetAction().Execute(self.vars, self)
                if (res == "Error"):
                    PrintText("Error en statement for en " + self.location.GetName())
                    return "Error"

            elif (temp2.GetType() == "encaso"):
                res = temp2.Execute(self.vars, self.location)
                if (res == "Error"):
                    PrintText("Error en statement encaso en " + self.location.GetName())
                    return "Error"

            elif (temp2.GetType() == "print"):
                res = temp2.GetAction().Execute(self.vars, self.location)
                if res == "Error":
                    print("Error en print en " + str(temp2.GetAction().GetLine()))
                    return "Error"

            elif (temp2.GetType() == "def"):
                PrintText("Error: funcion dentro de funcion")
                return "Error"

            elif (temp2.GetType() == "special_set"):
                PrintText("Error: No se puede ejecutar un bloque SET")
                return "Error"


class statement_EnCaso():
    def __init__(self, cuandos, sino_block):
        self.cuandos = cuandos
        self.sino_block = sino_block

    def Execute(self, vars, location):
        self.vars = vars
        self.location = location
        temp = self.cuandos
        temp2 = None
        cuando_called = False
        while (temp != None):
            if (type(temp) != YaccSymbol):
                if (len(temp) > 1):
                    temp2 = temp[0].value
                else:
                    temp2 = temp[0].value
            else:
                temp2 = temp.value

            flag = temp2.GetRelation().Execute(self.vars, self.location)
            if (flag == "Error"):
                return "Error"
            else:
                if flag:
                    cuando_called = True
                    res = temp2.Execute(self.vars, self.location)
                    if (res == "Error"):
                        PrintText("Error en statement if en " + str(temp2.GetAction().GetLine()))
                        return "Error"
                    else:
                        pass

            if (type(temp) == YaccSymbol):  # al final
                temp = None
            else:
                temp = temp[1].value

        if not cuando_called:
            temp = self.sino_block
            temp2 = None
            while (temp != None):
                if (type(temp) != YaccSymbol):
                    if (len(temp) > 1):
                        temp2 = temp[0].value

                    else:
                        temp2 = temp[0].value
                else:
                    temp2 = temp.value
                # COMIENZA EJECUCION DE BLOQUES SEGUN EL TIPO DE BLOQUES
                if (temp2.GetType() == "set"):

                    PrintText("Error: No se puede ejecutar un bloque SET, linea " + str(self.location))
                    return "Error"

                elif (temp2.GetType() == "sentence"):
                    if temp2.GetAction().GetType() == "function":
                        res = temp2.GetAction().Execute(self.vars)
                        if (res == "Error"):
                            PrintText("Error en la funcion introducida en linea " + str(temp2.GetAction().GetLine()))
                            return "Error"

                elif (temp2.GetType() == "statement_if"):
                    res = temp2.GetAction().Execute(self.vars, self)
                    if (res == "Error"):
                        PrintText("Error en statement if en " + str(temp2.GetAction().GetLine()))
                        return "Error"

                elif (temp2.GetType() == "statement_for"):
                    res = temp2.GetAction().Execute(self.vars, self)
                    if (res == "Error"):
                        PrintText("Error en statement for en " + self.location.GetName())
                        return "Error"

                elif (temp2.GetType() == "encaso"):
                    res = temp2.Execute(self.vars, self.location)
                    if (res == "Error"):
                        PrintText("Error en statement encaso en " + self.location.GetName())
                        return "Error"

                elif (temp2.GetType() == "print"):
                    res = temp2.GetAction().Execute(self.vars, self.location)
                    if res == "Error":
                        print("Error en print en " + str(temp2.GetAction().GetLine()))
                        return "Error"

                elif (temp2.GetType() == "def"):
                    PrintText("Error: funcion dentro de funcion")
                    return "Error"

                elif (temp2.GetType() == "special_set"):
                    res = temp2.Execute(self.vars, self.location)
                    if (res == "Error"):
                        PrintText("Error en statement set en " + self.location.GetName())
                        return "Error"

class DiffSet():

    def __init__(self, setstr, line,set_type):

        self.setstr = setstr
        self.set_type = set_type
        self.line = line

    def Execute(self, vars, location):
        self.vars = vars
        self.location = location
        print(self.set_type)
        if self.set_type == "special_set":
            print("special_set")
            splited = self.setstr.split("$")
            var1 = self.GetVar(splited[0])
            var2 = self.GetVar(splited[1])
            if (var1 != "Error" and var2 != "Error"):
                if (var1.GetType() == "int" and var2.GetType() == "int" and var1 == var2):
                    print(var1.GetValue())
                    neg = var1.GetValue() * (-1)
                    var1.SetValue(neg)
                    print(var1.GetValue())
                    return "Exito"
            else:
                PrintText("Error en set, variable no encontrada o invalida en linea " + str(self.line))
                return "Error"
        else:
            splited = self.setstr.split("$")
            var1 = self.GetVar(splited[0])
            if (var1 != "Error"):
                print(splited[1])
                if (splited[1] == "T"):
                    var1.SetValue("true")
                    var1.SetType("bool")
                elif (splited[1] == "F"):
                    var1.SetValue("false")
                    var1.SetType("bool")
                elif (splited[1] == "Neg"):
                    if var1.GetType() == "bool":
                        if var1.GetValue() == "true":
                            var1.SetValue("false")
                        else:
                            var1.SetValue("true")
                    else:
                        PrintText("Error en set, variable no es booleana en linea " + str(self.line))
                        return "Error"
                else:
                    PrintText("Error en set, parametro invalido en linea en linea " + str(self.line))
                    return "Error"
            else:
                PrintText("Error en set, variable no encontrada o invalida")
                return "Error"

    def GetVar(self,name):
        if self.vars != []:
            for i in self.vars:
                if i.GetName() == name:
                    return i
        if global_vars != []:
            for i in global_vars:
                if i.GetName() == name:
                    return i
        PrintText("Error: Variable not found en linea " + str(self.line))
        return "Error"
