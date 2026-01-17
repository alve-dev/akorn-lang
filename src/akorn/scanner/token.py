from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    #Keyword data typea
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    
    #Keywords var types
    VAR = auto()
    LET = auto()
    
    #Keywords conditionals
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    
    #Keywords loops
    WHILE = auto()
    LOOP = auto()
    BREAK = auto()
    CONTINUE = auto()
    
    #Signs
    PLUS = auto()
    PLUS_ASSIGN = auto()
    MINUS = auto()
    MINUS_ASSIGN = auto()
    STAR = auto()
    STAR_ASSIGN = auto()
    DOUBLE_STAR = auto()
    DOUBLE_STAR_ASSIGN = auto()
    MOD = auto()
    MOD_ASSIGN = auto()
    SLASH = auto()
    SLASH_ASSIGN = auto()
    ASSIGN = auto()
    
    #Signs Comparison
    EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    DIFERENT = auto()
    
    #Signs Booleans
    AND = auto()
    OR = auto()
    NOT = auto()
    
    #Special Simbols
    SEMICOLON = auto()
    COMMA = auto()
    NEWLINE = auto()
    
    #Parens and braces
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    
    #Identifier
    IDENT = auto()
    
    #Literals
    NUMBER = auto()
    STRING_LITERAL = auto()
    TRUE = auto()
    FALSE = auto()
    
    #None Value
    NONE = auto()
    
    #End Of File
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    column: int
    line: int
    
    def __repr__(self):
        return f"{__class__.__name__}(type={self.type}, value='{self.value}', line={self.line}, column={self.column})"