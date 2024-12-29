"""
Exceptions raised by the parser.
"""

class ParseSyntaxError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return f"{self.message} (line {self.line}, column {self.column})" \
            if self.line is not None and self.column is not None else self.message
