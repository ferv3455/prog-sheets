'''
Parser environment: contains global variables and functions as grammar rules.
'''
from .ast import ASTNode
from .errors import ParseSyntaxError
from .lex import *


# Factory function to create grammar rule functions
def grammar_rule_action(name, syntax):
    def wrapped_func(p):
        p[0] = ASTNode(name, p)

    wrapped_func.__doc__ = syntax
    return wrapped_func


# Grammar rules
for name, syntax in grammar.items():
    globals()[f'p_{name}'] = grammar_rule_action(name, syntax)


# Error handling rule
def p_error(p):
    if p:
        raise ParseSyntaxError(f"Invalid token '{p.value}' of type '{p.type}'",
                               p.lineno, p.lexpos)
    else:
        raise ParseSyntaxError('Incomplete statement', None, None)
