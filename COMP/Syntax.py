from COMP.ply import yacc
from COMP.Lexer import tokens

precedence = (
    ('right', 'COMMA', 'EQUALS'),
    ('left', 'GREATER', 'SMALLER', 'GREATEQ', 'SMALLEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV', 'FULLDIV'),
    ('left', 'MODULE'),
    ('left', 'POWER'),
    ('left', 'LPAR', 'RPAR', 'LBRACK', 'PBRACK'),

)


def p_program(p):
    '''program : block'''
    print("program")


def p_statement_set(p):
    '''statement : SET VAR COMMA NUMBER SEMICOLOMN'''
    print("statement set")


def p_statement_for(p):
    '''statement : FOR VAR TO NUMBER STEP NUMBER'''
    print("statement for")


def p_statement_if(p):
    """statement : IF LBRACK sentence RBRACK
               |IF LBRACK sentence RBRACK ELSE LBRACK sentence RBRACK
               """
    print("statement if")


def p_statementEnCaso(p):
    """statement : EnCaso Cuando ID relation term EnTons LBRACK sentence RBRACK SiNo LBRACK sentence RBRACK
    Fin-EnCaso SEMICOLOMN  | EnCaso ID Cuando relation term EnTons LBRACK sentence RBRACK SiNo LBRACK sentence RBRACK Fin-EnCaso SEMICOLOMN"""
    print("statement 5")


def p_statementEmpty(p):
    '''statement : empty'''
    print("nulo")


def p_relation(p):
    """relation : factor GREATER factor
                | factor SMALLER factor
                | factor GREATERQ factor
                | factor SMALLERQ factor
                """
    print("Comparacion")


def p_expression(p):
    '''expression : term relation term'''
    print("Expression")


def p_arithmetic(p):
    """arithmetic : factor PLUS factor
                | factor MINUS factor
                | factor TIMES factor
                | factor DIV factor
                | factor FULLDIV factor
                | factor MODULE factor
                | factor POWER factor
                """
    print("Operación Aritmética")


def p_factor(p):
    """factor : ID
            | NUMBER
            | STRING
            | BOOL
            | empty"""
    print("Factor")


def p_sentence(p):
    """sentence : statement
                | relation
                | arithmetic
                | factor
                | expression  """


def p_empty(p):
    '''empty :'''
    pass


def p_error(p):
    print("Error de sintaxis ", p)


parser = yacc.yacc()
#result = parser.parse(cadena)
#print (result)
