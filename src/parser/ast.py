'''
Abstract Syntax Tree (AST) generated by the parser.
'''
from ply.yacc import YaccProduction


class ASTNode:
    def __init__(self, type: str, obj: YaccProduction):
        self.type = type
        self.values = tuple(obj[1:])

    def visualize(self, indent=0):
        print(' ' * indent + self.type)
        for value in self.values:
            if isinstance(value, ASTNode):
                value.visualize(indent + 4)
            else:
                print(' ' * (indent + 4) + str(value))

    def __repr__(self):
        return f"{self.__class__.__name__}[{self.type}]{self.values}"
