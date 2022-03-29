import sys

sys.path.insert(0, "../..")

from COMP.ply import lex

tokens = ['ID','VAR','NUMBER', 'PLUS', 'MINUS', 'DENIAL', 'TIMES', 'POWER', 'DIV', 'FULLDIV', 'MODULE',
                 'COMMA', 'SEMICOLOMN', 'AT', 'GREATER', 'SMALLER', 'RPAR', 'LPAR', 'LBRACK', 'RBRACK', 'GREATEQ',
                 'SMALLEQ', 'COMMENT','WHITESPACE','EQUALS','POINT']

reserved = {'SET': 'SET',
            'Def': 'DEF',
            'if': 'IF',
            'for': 'FOR',
            'else': 'else',
            'EnCaso': 'EnCaso',
            'EnTons': 'EnTons',
            'println!': 'PRINT',
            'to': 'TO',
            'Step': 'STEP',
            'Cuando': 'CUANDO',
            'SiNo': 'SINO',
            'Fin-EnCaso': 'FINENCASO',
            'True': 'TRUE',
            'False': 'FALSE'}

token = tokens + list(reserved.values())

t_POINT = r'[.]'
t_COMMA = r'[,]'
t_SEMICOLOMN = '[;]'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\*\*'
t_DIV = r'/'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRACK = r'\{'
t_RBRACK = r'\}'
t_GREATER = r'\>'
t_SMALLER = r'\<'
t_GREATEQ = r'<='
t_SMALLEQ = r'>='
t_ignore = r' '
t_EQUALS = r'=='
t_FULLDIV = r'\\'


def t_COMMENT(t):
    r'\#.*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_VAR(t):
    r'@[A-Za-z_][\w_]*'
    if t.value.upper() in reserved:
        t.value = t.value.upper()
        t.type = t.value
    return t

def t_ID(t):
    r'[A-Za-z_][\w_]*'
    if t.value.upper() in reserved:
        t.value = t.value.upper()
        t.type = t.value
    return t


def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Integer value too large %s" % t.value)
        t.value = 0
    return t


analyzer = lex.lex()


def TokenGen(cadena):
    analyzer.input(cadena)
    while True:
        tok = analyzer.token()
        if not tok:
            break
        print(tok)