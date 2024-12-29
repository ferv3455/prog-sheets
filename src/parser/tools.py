'''
Generate the lexer and parser for the language.
'''
import ply.lex as lex
import ply.yacc as yacc

from .lex import *
from .parse import *


# Build the lexer
lexer = lex.lex()

# Build the parser
parser = yacc.yacc()
