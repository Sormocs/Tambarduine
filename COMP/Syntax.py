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
     '''statement : FOR factor TO factor STEP number LBRACK blockList RBRACK'''
     print("statement for")
     semantic.statement_for("for")
     p[0] = ["objeto for"] + ["for"]


def p_statement_if(p):
    '''statement : IF LPAR sentence RPAR LBRACK blockList RBRACK
    | IF LPAR sentence RPAR LBRACK blockList RBRACK ELSE LBRACK blockList RBRACK '''
    print("statement if")
    p[0] = ["objeto if"] + ["if"]


def p_statement_EnCaso(p):
    '''statement : ENCASO CUANDO relation ENTONS LBRACK sentence RBRACK SINO LBRACK sentence RBRACK FINENCASO SEMICOLOMN
     | ENCASO factor CUANDO relation ENTONS LBRACK sentence RBRACK SINO LBRACK sentence RBRACK FINENCASO SEMICOLOMN'''
    print("statement 5")
    p[0] = ["objeto en caso"] + ["encaso"]

def p_statement_DEF(p):
    '''statement : DEF var LPAR RPAR LBRACK blockList RBRACK SEMICOLOMN'''
    p[0] = [semantic.statement_DEF(p[2].replace(',#var',''),p[6])] + ["def"]



def p_statement_print(p):
    '''statement : id LPAR sentence RPAR SEMICOLOMN'''

    p[0] = [semantic.PrintConsole(p[1],p[3][0])] + ["print"]


def p_function(p):
    '''function : function1
    | function2
    | function3
    | function4'''
    p[0] = p[1].replace('#id','') + "#function"

def p_function1(p):
    '''function1 : id LPAR id RPAR SEMICOLOMN'''
    #semantic.Funciones(p[1], p[3])
    p[0] = str(p[1]) + "$" + str(p[3])

def p_function2(p):
    '''function2 : id LPAR RPAR SEMICOLOMN'''
    #semantic.Funciones(p[1], "none")
    p[0] = str(p[1])


def p_function3(p):
    '''function3 : id LPAR number RPAR SEMICOLOMN'''
    #semantic.Funciones(p[1], p[3])
    p[0] = str(p[1]) + "$" + str(p[3])

def p_function4(p):
    '''function4 : id LPAR id COMMA number RPAR SEMICOLOMN'''
    print ("function4")
    #semantic.Metronomo(p[1], p[3], p[5])
    p[0] = str(p[1]) + "$" + str(p[3]) + "$" + str(p[5])

def p_statementEmpty(p):
    '''statement : empty'''


def p_relation1(p):
    '''relation : factor GREATER factor
    | factor SMALLER factor
    | factor GREATEQ factor
    | factor SMALLEQ factor
    | factor DIFF factor
    | factor EQUALS factor'''
    print("Comparacion")
    p[0] = str(p[1]).replace('#var','') + str(p[2]) + str(p[3].replace('#var',''))+"#relation"

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
    p[0] = "#false"

def p_var(p):
    '''var : VAR'''
    p[0] = str(p[1]) + ",#var"

def p_string(p):
    '''string : QUOT id_list QUOT'''
    p[0] = str(p[2]) + ",#str"

def p_id_list(p):
    '''id_list : id
    | id id_list'''
    try:
        p[0] = p[1].replace('#id',',') + p[2].replace('#id',',')
    except (IndexError):
        p[0] = p[1].replace('#id','')

def p_id(p):
    '''id : ID'''
    p[0] = str(p[1]) + "#id"

def p_sentence(p):
    '''sentence : relation
    | opList
    | factor
    | function'''
    split = p[1].split("#")
    line = str(p.lineno)
    #print("line:" + line)
    p[0] = [semantic.sentence(split[0],split[1],400)] + ["sentence"]

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


def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    try:
        semantic.PrintText("Error de sintaxis en linea " + str(p.lineno) + " en " + str(p.value))
    except (AttributeError):
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
    for i in semantic.methods:
        if i.GetName() == "@Principal":
            detected = True
            i.Execute()
            break
    if not detected:
        semantic.PrintText("No se encontro el metodo principal")
