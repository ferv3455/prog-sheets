'''
Grammar configuration file for the parser. This is the only file that needs to be modified to change the grammar.
'''

################### Add token rules here ###################
'''
Token rule syntax: ('TOKEN_NAME', 'REGEX_PATTERN', ACTION)

If ACTION is None, the token value is the matched string.
If ACTION is callable, the value is the return value of ACTION function applied to the string.
Otherwise, the value is ACTION itself.
'''

token_rules = (
    # Keywords
    ('PLOT', r'绘图', 'plot'),
    ('SHOW', r'输出', 'show'),
    ('SUM', r'总和', 'sum'),
    ('COUNT', r'计数', 'count'),
    ('AVERAGE', r'平均', 'average'),
    ('MAX', r'最大', 'max'),
    ('MIN', r'最小', 'min'),

    # Operators
    ('LPAREN', r'\(', None),
    ('RPAREN', r'\)', None),
    ('LBRACKET', r'\[', None),
    ('RBRACKET', r'\]', None),
    ('COLON', r':', None),
    ('COMMA', r',', None),
    ('EQUAL', r'=', None),
    ('GREATER', r'>', None),
    ('LESS', r'<', None),
    ('GEQ', r'>=', None),
    ('LEQ', r'<=', None),
    ('NEQ', r'!=', None),

    # Identifiers
    ('ID', r'[a-zA-Z_\u4e00-\u9fff][a-zA-Z0-9_\u4e00-\u9fff]*', None),

    # Literals
    ('NUMBER', r'\d+', int),
    ('FLOAT', r'\d+\.\d+', float),
    ('STRING', r'"[^"]*"', lambda s: s[1:-1]),
)

################### End of custom token rules ###################

################### Add grammar rules here ###################
'''
Grammar rule syntax: 'RULE_NAME': 'RULE_BODY'
'''

# Begin with statement
start = 'statement'

# Detailed grammar rules
grammar = {
    # Source
    'statement': '''
        statement : ID EQUAL query
                  | PLOT query
                  | SHOW query
    ''',

    # Components
    'literal': '''
        literal : NUMBER
                | FLOAT
                | STRING
    ''',
    'compare_op': '''
        compare_op : GREATER
                   | LESS
                   | GEQ
                   | LEQ
                   | NEQ
                   | EQUAL
    ''',

    # Query command
    'query': '''
        query : ID col_param group_param cond_param
    ''',
    'col_param': '''
        col_param :
                  | LPAREN col_list RPAREN
    ''',
    'col_list': '''
        col_list : ID COMMA col_list
                 | ID
    ''',
    'group_param': '''
        group_param :
                    | LBRACKET ID RBRACKET
                    | LBRACKET ID COMMA COUNT RBRACKET
                    | LBRACKET ID COMMA SUM RBRACKET
                    | LBRACKET ID COMMA SUM COMMA ID RBRACKET
                    | LBRACKET ID COMMA AVERAGE RBRACKET
                    | LBRACKET ID COMMA AVERAGE COMMA ID RBRACKET
                    | LBRACKET ID COMMA MAX RBRACKET
                    | LBRACKET ID COMMA MAX COMMA ID RBRACKET
                    | LBRACKET ID COMMA MIN RBRACKET
                    | LBRACKET ID COMMA MIN COMMA ID RBRACKET
    ''',
    'cond_param': '''
        cond_param :
                   | COLON cond_list
    ''',
    'cond_list': '''
        cond_list : condition COMMA cond_list
                  | condition
    ''',
    'condition': '''
        condition : ID compare_op literal
    ''',
}

################### End of custom grammar rules ###################
