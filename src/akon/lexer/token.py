from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    #Keyword types
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    
    #Signs
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    DOUBLE_STAR = auto()
    MOD = auto()
    SLASH = auto()
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
    
    #Semicolon
    SEMICOLON = auto()
    
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
        return f"{__class__.__name__}(type={self.type}, value={self.value}, line={self.line}, column={self.column})"