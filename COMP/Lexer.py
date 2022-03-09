import sys

sys.path.insert(0, "../..")

from COMP.ply import lex

tokens = ['ID','VAR','NUMBER', 'PLUS', 'MINUS', 'DENIAL', 'TIMES', 'POWER', 'DIV', 'FULLDIV', 'MODULE',
                 'COMMA', 'SEMICOLOMN', 'AT', 'GREATER', 'SMALLER', 'RPAR', 'LPAR', 'LBRACK', 'RBRACK', 'GREATEQ',
                 'SMALLEQ', 'COMMENT','WHITESPACE','EQUALS']

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

# t_POINT = r'[.]'
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
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %s" % t.value)
        t.value = 0
    # print "parsed number %s" % repr(t.value)
    return t


analyzer = lex.lex()


def TokenGen(cadena):
    analyzer.input(cadena)
    while True:
        tok = analyzer.token()
        if not tok:
            break
        print(tok)

# #CONSTANTS
# NUMS = '0123456789'
# LETTER_SYMBOL = 'ABCDEFGHIJKLMNOPQRSTUVWabcdefghijklmnopqrstuvwxyz@_?~'
#
# RESERVED = ['SET','Def','if','for','else','EnCaso','EnTons','println!','to',
#             'Step','Cuando','SiNo','Fin-EnCaso','True','False']
#
# #TOKENS
# TT_INT = 'TT_INT'
# TT_FLOAT = 'FLOAT'
# TT_PLUS = 'PLUS'
# TT_MINUS = 'MINUS'
# TT_MULT = 'MULT'
# TT_POWER = 'POWER'
# TT_DIV = 'DIV'
# TT_FULLDIV = 'FULLDIV'
# TT_RPAR = 'RPAR'
# TT_LPAR = 'LPAR'
# TT_LBRACK = 'LBRACK'
# TT_RBRACK = 'RBRACK'
# TT_EQUALS = 'EQUALS'
# TT_GREATER = 'GREATER'
# TT_SMALLER = 'SMALLER'
# TT_GREATEQ = 'GREATEQ'
# TT_SMALLEQ = 'SMALLEQ'
# TT_COMMA = 'COMMA'
# TT_SEMICOLOMN = 'SEMICOLOMN'
#
# class Error:
#
#     def __init__(self,error_name,details):
#         self.error_name = error_name
#         self.details = details
#
#     def as_string(self):
#         result = f'{self.error_name}:{self.details}'
#         return result
#
# class IllegalCharError(Error):
#     def __init__(self, details):
#         super().__init__('Illegal Character',details)
#
# class Token():
#
#     def __init__(self, type, value):
#         self.type = type
#         self.value = value
#
#     def __repr__(self):
#         if self.value: return f'{self.type}:{self.value}'
#         return f'{self.type}'
#
#
# class Lexer():
#
#     def __init__(self, code):
#         self.code = code
#         self.pos = -1
#         self.curr_char = None
#         self.Advance()
#
#     def Advance(self):
#         self.pos += 1
#         if self.pos < len(self.code):
#             self.curr_char = self.code[self.pos]
#         else:
#             self.curr_char = None
#
#     def Token_Gen(self):
#         tokens = []
#
#         while self.curr_char != None:
#             if self.curr_char in ' \t':
#                 self.Advance()
#             #elif self.curr_char in LETTER_SYMBOL:
#             #    tokens.append(self.Words())
#             #    self.Advance()
#             elif self.curr_char in NUMS:
#                 tokens.append(self.Numbers())
#             elif self.curr_char == '+':
#                 tokens.append(Token(TT_PLUS, None))
#                 self.Advance()
#             elif self.curr_char == '-':
#                 tokens.append(Token(TT_MINUS, None))
#                 self.Advance()
#             elif self.curr_char == '/':
#                 tokens.append(Token(TT_DIV, None))
#                 self.Advance()
#             elif self.curr_char == '//':
#                 tokens.append(Token(TT_FULLDIV, None))
#                 self.Advance()
#             elif self.curr_char == '*':
#                 tokens.append(Token(TT_MULT, None))
#                 self.Advance()
#             elif self.curr_char == '**':
#                 tokens.append(Token(TT_POWER, None))
#                 self.Advance()
#             elif self.curr_char == '==':
#                 tokens.append(Token(TT_EQUALS, None))
#                 self.Advance()
#             elif self.curr_char == '<=':
#                 tokens.append(Token(TT_SMALLEQ, None))
#                 self.Advance()
#             elif self.curr_char == '>=':
#                 tokens.append(Token(TT_GREATEQ, None))
#                 self.Advance()
#             elif self.curr_char == '>':
#                 tokens.append(Token(TT_GREATER, None))
#                 self.Advance()
#             elif self.curr_char == '<':
#                 tokens.append(Token(TT_SMALLER, None))
#                 self.Advance()
#             elif self.curr_char == '{':
#                 tokens.append(Token(TT_LBRACK, None))
#                 self.Advance()
#             elif self.curr_char == '}':
#                 tokens.append(Token(TT_RBRACK, None))
#                 self.Advance()
#             elif self.curr_char == '(':
#                 tokens.append(Token(TT_LPAR, None))
#                 self.Advance()
#             elif self.curr_char == ')':
#                 tokens.append(Token(TT_RPAR, None))
#                 self.Advance()
#             elif self.curr_char == ',':
#                 tokens.append(Token(TT_COMMA, None))
#                 self.Advance()
#             elif self.curr_char == ';':
#                 tokens.append(Token(TT_SEMICOLOMN, None))
#                 self.Advance()
#             else:
#                 char = self.curr_char
#                 self.Advance()
#                 return [],IllegalCharError("'"+ char +"'")
#         return tokens, None
#
#
#     def Numbers(self):
#         num_str = ''
#         dot = False
#
#         while self.curr_char != None and self.curr_char in NUMS + '.':
#             if self.curr_char == '.':
#                 if dot:
#                     break
#                 dot = True
#                 num_str += '.'
#             else:
#                 num_str += self.curr_char
#             self.Advance()
#         if not dot:
#             return Token(TT_INT,int(num_str))
#         else:
#             return Token(TT_FLOAT, float(num_str))
#
#     def Words(self):
#
#         str = ''
#
#         while self.curr_char != None and self.curr_char in LETTER_SYMBOL:
#
#             str += self.curr_char
#             self.Advance()
#
#         if str in RESERVED:
#             return Token(str.upper(),None)
#         else:
#             if (str[0] == '@'):
#                 return Token('VAR',str)
#             else:
#                 self.curr_char = '|'
#                 return Token('VAR',str)