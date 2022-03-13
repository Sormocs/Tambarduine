import sys
from COMP.ply import yacc
import os
from Lexer import token
from sys import stdin

precedence = (
    ('right', 'COMMA', 'EQUALS'),
    ('left', 'GREATER', 'SMALLER', 'GREATEQ', 'SMALLEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV', 'FULLDIV'),
    ('left', 'MODULE'),
    ('left', 'POWER'),
    ('left', 'LPAR', 'RPAR'),

)


#terminales: tokens
def p_program(p):
    """program = block"""
    p[0] = p.program(p[1], "program")
    print "program"


def p_statement4(p):
    """statement: IF condition THEN statement"""
    print "statement 4"


def p_statementEmpty(p):
    """statement: empty"""
    print "nulo"


def p_statementList1(p):
    """statement: statement"""
    print "statementList 1"


def p_statementList2(p):
    """statement: statementList ; statement"""
    print "statementList 2"


def p_condition2(p):
    """condition : expression relation expression"""
    print "condition 2"


def p_relation1(p):
    """relation : COMMA"""
    print "relation 1"


def p_relation2(p):
    """relation : GREATER"""
    print "relation 2"


def p_relation3(p):
    """relation : SMALLER"""
    print "relation 3"


def p_relation4(p):
    """relation : SMALLEQ"""
    print "relation 4"

def p_relation5(p):
    """relation : GREATEQ"""
    print "relation 5"



def p_expression1(p):
    """expression : term"""
    print "expression 1"


def p_expression2(p):
    """expression : addingOperatior term"""
    print "expression 2"


def p_expression3(p):
    """expression : expression addingOperator term"""
    print "expression 3"


def p_term1(p):
    """term : factor"""
    print "term 1"


def p_term2(p):
    """term : term multiplyingOperator factor"""
    print "term 2"


def p_multiplyingOperator1(p):
    """multiplyingOperator : TIMES"""
    print "multiplyingOperator 1"


def p_multiplyingOperator2(p):
    """multiplyingOperator : DIVIDE"""
    print "multiplyingOperator 2"


def p_factor1(p):
    """factor : ID"""
    print "factor 1"


def p_factor2(p):
    """factor : NUMBER"""
    print "factor 2"


def p_factor3(p):
    """factor : LPARENT expression RPARENT"""
    print "factor 3"


def p_empty(p):
    """empty : """
    pass


def p_error(p):
    print "error de sintaxis", p
    print "error en la linea " + str(p.lineno)


parser = yacc.yacc()
result = parser.parse(cadena)
print result
