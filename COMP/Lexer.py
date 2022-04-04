import sys

sys.path.insert(0, "../..")

from COMP.ply import lex

reserved = ['SET','DEF','IF','FOR','ELSE','ENCASO','ENTONS','TO','STEP','CUANDO','SINO','FINENCASO',
            'TRUE','FALSE','WHILE']

tokens = reserved +['ID','VAR','NUMBER', 'PLUS', 'MINUS', 'TIMES', 'POWER', 'DIV', 'FULLDIV','QUOT',
                    'MODULE','COMMA', 'SEMICOLOMN','GREATER', 'SMALLER', 'RPAR', 'LPAR', 'LBRACK',
                    'RBRACK', 'GREATEQ','SMALLEQ','EQUALS','POINT','SAME','DIFF']

t_POINT = r'[.]'
t_COMMA = r'[,]'
t_SEMICOLOMN = r'[;]'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\*\*'
t_DIV = r'/'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRACK = r'\{'
t_RBRACK = r'\}'
t_GREATER = r'>'
t_SMALLER = r'<'
t_GREATEQ = r'>='
t_SMALLEQ = r'<='
t_ignore = r' '
t_EQUALS = r'=='
t_FULLDIV = r'//'
t_SAME = r'='
t_DIFF = r'<>'
t_QUOT = r'"'


def t_COMMENT(t):
    r'\#.*'
    pass

def t_ID(t):
    r'[A-Za-z_][a-zA-Z!0-9_?!$:]*'
    if t.value.upper() in reserved:
        t.value = t.value.upper()
        t.type = t.value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_VAR(t):
    r'@[a-zA-Z_][a-zA-Z0-9_?!$]{2,10}'
    return t

def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %s" % t.value)
        t.value = 0
    return t


analyzer = lex.lex()


def TokenGen(cadena):
    analyzer.lineno = 0
    analyzer.input(cadena)
    while True:
        tok = analyzer.token()
        if not tok:
            break
        print(tok)
