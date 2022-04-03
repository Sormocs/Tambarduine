import sys
import COMP.Lexer as lex
from COMP.ply import yacc
import COMP.SemanticAn as semantic

tokens = lex.tokens

precedence = (
    ('right','VAR','FOR','IF','WHILE','ELSE'),
    ('right','SET','DEF','TO','CUANDO','SINO'),
    ('left','DIFF'),
    ('left','GREATER','SMALLER','SAME','GREATEQ','SMALLEQ','EQUALS'),
    ('left','PLUS','MINUS'),
    ('left','POWER','TIMES','FULLDIV','DIV','MODULE'),
    ('left','LBRACK','RBRACK'),
    ('left','LPAR','RPAR'),
    ('left','POINT')
)


def p_statement_set(p):
    '''statement : SET VAR COMMA sentence SEMICOLOMN'''
    p[0] = [semantic.statement_set(p[2],p[4][0])] +["set"]
    #print("Valor: "+p[0][0].GetSentence().GetValue())
    #print("Tipo: " + p[0][0].GetSentence().GetType())
#
#
def p_statement_for(p):
     '''statement : FOR VAR TO NUMBER STEP NUMBER LBRACK blockList RBRACK SEMICOLOMN'''
     print("statement for")
     p[0] = [semantic.statement_for(p[2],p[4],p[6]),p[8]] + ["statement_for"]


def p_statement_if(p):
    '''statement : IF LPAR sentence RPAR LBRACK blockList RBRACK SEMICOLOMN'''
    print("statement if")
    p[0] = [semantic.statement_if(p[3][0],p[6],"none",False)] + ["statement_if"]

def p_statement_if2(p):
    '''statement : IF LPAR sentence RPAR LBRACK blockList RBRACK ELSE LBRACK blockList RBRACK SEMICOLOMN'''
    print("statement if")
    p[0] = [semantic.statement_if(p[3][0],p[6],p[10],True)] + ["statement_if"]

def p_statement_EnCaso(p):
    '''statement : ENCASO CUANDO relation ENTONS LBRACK sentence RBRACK SINO LBRACK sentence RBRACK FINENCASO SEMICOLOMN
     | ENCASO factor CUANDO relation ENTONS LBRACK sentence RBRACK SINO LBRACK sentence RBRACK FINENCASO SEMICOLOMN'''
    print("statement 5")
    p[0] = ["objeto en caso"] + ["encaso"]

def p_statement_DEF(p):
    '''statement : DEF var LPAR RPAR LBRACK blockList RBRACK SEMICOLOMN '''
    p[0] = [semantic.statement_DEF(p[2].replace('#var',''),p[6])] + ["def"]


def p_statement_print(p):
    '''statement : ID LPAR sentence RPAR SEMICOLOMN'''
    p[0] = [semantic.PrintConsole(p[1],p[3][0],"sentence")] + ["print"]

def p_statement_print2(p):
    '''statement : ID LPAR VAR RPAR SEMICOLOMN'''
    print("statement print2")
    p[0] = [semantic.PrintConsole(p[1],p[3][0],"var")] + ["print"]


def p_function(p):
    '''function : function1
    | function2
    | function3
    | function4'''
    string = p[1].replace('#id','') + "#function"
    p[0] = string.replace('#operation','')

def p_function1(p):
    '''function1 : ID LPAR ID RPAR SEMICOLOMN'''

    p[0] = str(p[1]) + "$" + str(p[3])

def p_function2(p):
    '''function2 : ID LPAR RPAR SEMICOLOMN'''

    p[0] = str(p[1])


def p_function3(p):
    '''function3 : ID LPAR NUMBER RPAR SEMICOLOMN'''

    p[0] = str(p[1]) + "$" + str(p[3])

def p_function4(p):
    '''function4 : ID LPAR ID COMMA NUMBER RPAR SEMICOLOMN'''
    #print ("function4")
    p[0] = str(p[1]) + "$" + str(p[3]) + "$" + str(p[5])

def p_statementEmpty(p):
    '''statement : empty'''


def p_relation(p):
    '''relation : relation1
    | relation2
    | relation3
    | relation4
    | relation5
    | relation6
    | relation7
    | relation8'''

    string = str(p[1]) +"#relation"
    p[0] = string

def p_relation1(p):
    '''relation1 : NUMBER compare NUMBER'''
    string = str(p[1]) +"$"+ str(p[2]) +"$"+ str(p[3])+"$"+ "NUM_NUM"
    p[0] = string

def p_relation2(p):
    '''relation2 : NUMBER compare VAR'''
    string = str(p[1]) +"$"+ str(p[2]) +"$"+ str(p[3])+"$"+ "NUM_VAR"
    p[0] = string

def p_relation3(p):
    '''relation3 : VAR compare VAR'''
    string = str(p[1]) +"$"+ str(p[2]) +"$"+ str(p[3])+"$"+ "VAR_VAR"
    p[0] = string

def p_relation4(p):
    '''relation4 : VAR compare NUMBER'''
    string = str(p[1]) +"$"+ str(p[2]) +"$"+ str(p[3])+"$"+ "VAR_NUM"
    p[0] = string

def p_relation5(p):
    '''relation5 : VAR compare string'''
    string = str(p[1]) +"$"+ str(p[2]) +"$"+ str(p[3])+"$"+ "VAR_STR"
    p[0] = string

def p_relation6(p):
    '''relation6 : string compare string'''
    string = str(p[1]) + "$" + str(p[2]) + "$" + str(p[3]) + "$" + "STR_STR"
    p[0] = string

def p_relation7(p):
    '''relation7 : TRUE compare VAR
    | FALSE compare VAR'''
    string = str(p[1]) + "$" + str(p[2]) + "$" + str(p[3]) + "$" + "BOOL_VAR"
    p[0] = string

def p_relation8(p):
    '''relation8 : VAR compare TRUE
    | VAR compare FALSE'''
    string = str(p[1]) + "$" + str(p[2]) + "$" + str(p[3]) + "$" + "VAR_BOOL"
    p[0] = string


def p_compare(p):
    '''compare : SMALLER
    | GREATER
    | SMALLEQ
    | GREATEQ
    | EQUALS
    | DIFF'''
    p[0] = str(p[1])

def p_operation(p):
    '''operation : operation2
    | number
    | var
    | string
    | float
    | operation3'''
    p[0] = str(p[1]).replace('#var','')

def p_operation2(p):
    '''operation2 : number symbol
    | var symbol
    | string symbol
    | float symbol
    | operation3 symbol'''
    p[0] = str(p[1])+str(p[2])

def p_operation3(p):
    '''operation3 : parenthesis'''
    p[0] = "(,"+str(p[1])+"),"

def p_opList(p):
    '''opList : operation
    | operation opList'''
    try:
        p[0] = str(p[1])+str(p[2])
    except(IndexError):
        p[0] = str(p[1]).replace('#var','') + "#operation"

def p_parenthesis(p):
    '''parenthesis : LPAR opList RPAR'''
    p[0] = str(p[2]).replace('#operation','')

def p_symbol(p):
    '''symbol : MINUS
    | PLUS
    | TIMES
    | POWER
    | DIV
    | FULLDIV
    | MODULE'''

    p[0] = str(p[1]) + ","


def p_factor(p):
    '''factor : number
    | true
    | false
    | var
    | string
    | id
    | empty'''
    p[0] = str(p[1])

def p_number(p):
    '''number : NUMBER'''
    p[0] = str(p[1]) + ","

def p_float(p):
    '''float : NUMBER POINT NUMBER'''
    p[0] = str(p[1])+str(p[2])+str(p[3]) + ","

def p_true(p):
    '''true : TRUE'''
    p[0] = str(p[0])+"#true"

def p_false(p):
    '''false : FALSE'''
    p[0] = str(p[0])+ "#false"

def p_var(p):
    '''var : VAR'''
    p[0] = str(p[1]) + "#var"

def p_string(p):
    '''string : QUOT id_list QUOT'''
    p[0] = str(p[2])

def p_id_list(p):
    '''id_list : id
    | id id_list'''
    try:
        p[0] = p[1].replace('#id',',') + " " +p[2].replace('#id',',')
    except (IndexError):
        p[0] = p[1].replace('#id','') + "#str"

def p_id(p):
    '''id : ID'''
    p[0] = str(p[1]) + "#id"

def p_sentence(p):
    '''sentence : relation
    | factor
    | function
    | type
    | opList'''
    split = p[1].split("#")
    line = str(p.lineno)
    #print(split)
    #print(p.__dict__)
    if "#str" in p[1]:
        string = p[1].replace("#str","")
        split = string.split("#")
        p[0] = [semantic.sentence(split[0], "str", p.stack[-1].lineno)] + ["sentence"]
    else:
        p[0] = [semantic.sentence(split[0],split[-1],p.stack[-1].lineno)] + ["sentence"]

def p_block(p):
    '''block : statement
    | sentence'''
    p[0] = semantic.Block(p[1][0],p[1][1])

def p_blockList(p):
    '''blockList : block
     | block blockList'''
    if len(p.slice) > 2:
        p[0] = (p.slice[1],p.slice[2])
    else:
        p[0] = (p.slice[1])

    # print(p.__dict__)
    # print(p.slice[1])

def p_type(p):
    '''type : ID LPAR VAR RPAR '''
    #print("Entro en type")
    p[0] = str(p[1])+"&"+str(p[3]) + "#type"

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    try:
        print("Error p",p)
        semantic.PrintText("Error de sintaxis en linea " + str(p.lineno + 1) + " en " + str(p.value))
    except (AttributeError):
        print("Error p", p)
        semantic.PrintText("Falta ;")

parser = yacc.yacc()

def Parsear(cadena,box):
    semantic.methods = []
    semantic.global_vars = []
    lex.analyzer.lineno = 0
    semantic.box = box
    #lex.TokenGen(cadena)
    result = parser.parse(cadena)
    detected = False

    if semantic.methods != []:
        for i in semantic.methods:
            if i.GetName() == "@Principal":
                detected = True
                i.Execute()
                #INSTRUCCION semantic.FUNCION()
                break
        if not detected:
            semantic.PrintText("No se encontro el metodo principal")
