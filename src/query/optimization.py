'''
AST optimization for later analysis.
'''
from typing import Callable, Iterable, Union
from itertools import chain

from src.parser import ASTNode, Token


# Simplification functions
simplify_funcs = dict()


# Register simplification functions
def register_simplify(name: str):
    global simplify_funcs

    def decorator(func: Callable[[Union[ASTNode, Token]],
                                 Union[Iterable[Union[ASTNode, Token]], ASTNode, Token]]):
        if name in simplify_funcs:
            raise ValueError(f"Simplification function with name"
                             f"{name} already registered")
        simplify_funcs[name] = func
        return func

    return decorator


# Recursively simplify the AST
def simplify_ast(node: ASTNode | Token) -> Iterable[ASTNode | Token] | ASTNode | Token:
    if isinstance(node, Token):
        return node
    elif node.type in simplify_funcs:
        return simplify_funcs[node.type](node)
    else:
        # Recursively simplify children
        simplified_values = list()
        for value in node.values:
            if isinstance(value, ASTNode):
                simplified = simplify_ast(value)
                if isinstance(simplified, Iterable):
                    simplified_values.extend(simplified)
                else:
                    simplified_values.append(simplified)
            else:
                simplified_values.append(value)
        node.values = tuple(simplified_values)
        return node


# Helper function: combine all arguments into a single iterable
def combine_args(*args: Iterable[ASTNode | Token] | ASTNode | Token) -> Iterable[ASTNode | Token]:
    iterables = (arg if isinstance(arg, Iterable) else (arg,) for arg in args)
    return chain.from_iterable(iterables)


@register_simplify('col_list')
@register_simplify('cond_list')
def unwrap_list(node: ASTNode | Token) -> Iterable[ASTNode | Token] | ASTNode | Token:
    if isinstance(node, Token):
        return node

    # Simplify the first child
    simplified_first = simplify_ast(node.values[0])
    if len(node.values) == 1:
        return simplified_first

    # Recursively simplify other children
    simplified = simplify_ast(node.values[2])
    return combine_args(simplified_first, simplified)


@register_simplify('col_param')
@register_simplify('group_param')
@register_simplify('cond_param')
def remove_op(node: ASTNode | Token) -> Iterable[ASTNode | Token] | ASTNode | Token:
    if isinstance(node, Token):
        return node

    # Recursively simplify children first
    simplified_values = combine_args(*(simplify_ast(value) for value in node.values))

    # Remove operator tokens
    op_types = ('LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'COLON')
    node.values = tuple(value for value in simplified_values
                        if isinstance(value, ASTNode) or value.type not in op_types)

    return node


@register_simplify('literal')
@register_simplify('compare_op')
def unwrap_symbol(node: ASTNode | Token) -> Iterable[ASTNode | Token] | ASTNode | Token:
    if isinstance(node, Token):
        return node
    return node.values[0]
