'''
Lexer environment: contains global variables and functions as token rules.
'''
from .grammar import *
from .errors import ParseSyntaxError


# Token class used in output
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token[{self.type}]({self.value})'


# Factory function to create token rule actions
def token_rule_action(name, regex, action):
    def default_action(x): return x

    if action is None:
        action = default_action

    def wrapped_func(t):
        t.value = Token(
            type=name,
            value=action(t.value) if callable(action) else action
        )
        return t

    wrapped_func.__doc__ = regex
    return wrapped_func


# List of token names
tokens = tuple(rule[0] for rule in token_rules)

# Regular expression rules with actions
for name, regex, action in token_rules:
    globals()[f't_{name}'] = token_rule_action(name, regex, action)

# Rule for ignoring spaces
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    t.lexer.lineno += t.value.count('\n')
    t.lexer.lexpos = t.lexpos
    raise ParseSyntaxError(f"Illegal character '{t.value[0]}'",
                           t.lexer.lineno, t.lexer.lexpos)
