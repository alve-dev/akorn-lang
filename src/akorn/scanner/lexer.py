from .token import Token, TokenType
from akorn.diagnostic import ErrorReporter

class Lexer:
    keywords = {
        "var":TokenType.VAR,
        "let":TokenType.LET,
        "int":TokenType.INT,
        "float":TokenType.FLOAT,
        "string":TokenType.STRING,
        "bool":TokenType.BOOL,
        "true":TokenType.TRUE,
        "false":TokenType.FALSE,
        "if":TokenType.IF,
        "else":TokenType.ELSE,
        "elif":TokenType.ELIF,
        "while":TokenType.WHILE,
        "loop":TokenType.LOOP,
        "break":TokenType.BREAK,
        "continue":TokenType.CONTINUE,
        "and":TokenType.AND,
        "or":TokenType.OR,
        "not":TokenType.NOT,
        "none":TokenType.NONE,
    }
    
    def __init__(self, code:str, reporter:ErrorReporter) -> None:
        self.code: str = code
        self.code_length: int = len(self.code)
        self.position: int = 0
        self.column: int = 0
        self.line: int = 1
        self.tokens_array: list[Token] = [] 
        self.reporter: ErrorReporter = reporter


    def advance(self, step: int) -> None:
        self.position += step
        self.column += step
    
    
    def reset_line(self) -> None:
        self.tokens_array.append(Token(TokenType.NEWLINE, "\\n", self.column, self.line))
        self.line += 1
        self.column = 0
     
        
    def peek(self, step: int) -> str:
        """peek(0) == actual character
        \npeek(n) == character n times ahead"""
        
        
        if self.position + step >= self.code_length:
            return '\0'
        
        return self.code[self.position + step]


    def scan_single_comment(self) -> None:
        while (self.position < self.code_length and self.peek(0) != '\n'):
            self.advance(1)


    def scan_multi_comment(self) -> None:
        success: bool = False
        
        while (self.position < self.code_length):
            if self.peek(0) == '*':   
                self.advance(1)
                if self.peek(0) == '/':
                    self.advance(1)
                    success = True
                    break
                else:
                    continue
                
            elif self.peek(0) == '\n':
                self.reset_line()
                self.advance(1)
            
            else:
                self.advance(1)
            
        if not success:
            self.reporter.add_error(
                f"[Lexer Error][line:{self.line}, col:{self.column}] You forgot to close the comment with these characters -> '*/'"
            )
    
    
    def scan_literal_number(self) -> None:
        start_position: int = self.position
        is_decimal: bool = False
                
        while self.position < self.code_length:
            if self.peek(0).isdigit():
                self.advance(1)
            elif (self.peek(0) == '.' and not is_decimal) and self.peek(1).isdigit():
                self.advance(1)
                is_decimal = True
            else:
                break
            
        numero_completo: str = self.code[start_position:self.position]
        
        if is_decimal:
            self.tokens_array.append(Token(TokenType.NUMBER, float(numero_completo), self.column, self.line))
        else:
            self.tokens_array.append(Token(TokenType.NUMBER, int(numero_completo), self.column, self.line))
    
    
    def scan_identifier_or_keyword(self) -> None:
        start_position = self.position
                                
        while (self.position < self.code_length):
            if self.peek(0).isalnum() or self.peek(0) == '_':
                self.advance(1)
            else:
                break
            
        full_identifier: str = self.code[start_position : self.position]
        
        if full_identifier in self.keywords.keys():
            self.tokens_array.append(Token(self.keywords[full_identifier], full_identifier, self.column, self.line))
        else:
            self.tokens_array.append(Token(TokenType.IDENT, full_identifier, self.column, self.line))


    def scan_literal_string(self) -> None:
        start_quotes: str = self.peek(0)
        start_position = self.position
        self.advance(1)
        success: bool = False
        
        while self.position < self.code_length:
            if self.peek(0) == '\n':
                self.advance(1)
                self.reset_line()
            else:
                if self.peek(0) == start_quotes:
                    self.advance(1)
                    success = True
                    break
                else:
                    self.advance(1)
                    
        if not success:
            self.reporter.add_error(
                f"[LexerError][line:{self.line} , col:{self.column}] You forgot to close the string with quotation marks; use them at the end -> '{start_quotes}'"
            )
            self.advance(1)
        else:
            temporal_string = self.code[start_position + 1 : self.position-1]
            
            if "\\n" in temporal_string:
                temporal_string = temporal_string.replace("\\n", "\n")
            if "\\t" in temporal_string:
                temporal_string = temporal_string.replace("\\t", "\t")
            
            self.tokens_array.append(Token(TokenType.STRING_LITERAL, temporal_string, self.column, self.line))
            
            
    def tokenize(self) -> list[Token]:
        while self.position < self.code_length:
             
            #Whitespaces and Newlines
            if self.peek(0) == ' ':
                self.advance(1)
            
            elif self.peek(0) == '\n':
                self.advance(1)
                self.reset_line()
                    
            #Semicolon
            elif self.peek(0) == ';':
                self.tokens_array.append(Token(TokenType.SEMICOLON, ';', self.column, self.line))
                self.advance(1)
            
            #Comma
            elif self.peek(0) == ',':
                self.tokens_array.append(Token(TokenType.COMMA, ',', self.column, self.line))
                self.advance(1)
            
            #Left parenthesis
            elif self.peek(0) == '(':
                self.tokens_array.append(Token(TokenType.LPAREN, '(', self.column, self.line))
                self.advance(1)
            
            #Right parenthesis
            elif self.peek(0) == ')':
                self.tokens_array.append(Token(TokenType.RPAREN, ')', self.column, self.line))
                self.advance(1)
            
            #Left brace
            elif self.peek(0) == "{":
                self.tokens_array.append(Token(TokenType.LBRACE, '{', self.column, self.line))
                self.advance(1)
                
            #Right brace
            elif self.peek(0) == "}":
                self.tokens_array.append(Token(TokenType.RBRACE, '}', self.column, self.line))
                self.advance(1)
                
            #Operator of plus and comuest plus
            elif self.peek(0) == '+':
                if self.peek(1) == '=':
                    self.tokens_array.append(Token(TokenType.PLUS_ASSIGN, '+=', self.column, self.line))
                    self.advance(2)
                else:
                    self.tokens_array.append(Token(TokenType.PLUS, '+', self.column, self.line))
                    self.advance(1)

            #Operators of minus and compuest minus
            elif self.peek(0) == '-':
                if self.peek(1) == '=':
                    self.tokens_array.append(Token(TokenType.MINUS_ASSIGN, '-=', self.column, self.line))
                    self.advance(2)
                else:
                    self.tokens_array.append(Token(TokenType.MINUS, '-', self.column, self.line))
                    self.advance(1)
            
            #Operators of multiplication, power, compuest multiplication and compuest power
            elif self.peek(0) == '*':
                if self.peek(1) == '*':
                    if self.peek(2) == '=':
                        self.tokens_array.append(Token(TokenType.DOUBLE_STAR_ASSIGN, "**=", self.column, self.line))
                        self.advance(3)
                    else:
                        self.tokens_array.append(Token(TokenType.DOUBLE_STAR, "**", self.column, self.line))
                        self.advance(2)
                else:
                    if self.peek(1) == '=':
                        self.tokens_array.append(Token(TokenType.STAR_ASSIGN, "*=", self.column, self.line))
                        self.advance(2)
                    else:
                        self.tokens_array.append(Token(TokenType.STAR, '*', self.column, self.line))
                        self.advance(1)
                
            #Operators of division and compuest division, or comments of single-line and multi-line
            elif self.peek(0) == '/':
                if self.peek(1) == '/':
                    self.advance(2)
                    self.scan_single_comment() 
                elif self.peek(1) == '*':
                    self.advance(2)
                    self.scan_multi_comment()
                elif self.peek(1) == '=':
                    self.tokens_array.append(Token(TokenType.SLASH_ASSIGN, '/=', self.column, self.line))
                    self.advance(2)
                else:
                    self.tokens_array.append(Token(TokenType.SLASH, '/', self.column, self.line))  
                    self.advance(1)    

            #Operators of mod and compound mod
            elif self.peek(0) == '%':
                if self.peek(1) == '=':
                    self.tokens_array.append(Token(TokenType.MOD_ASSIGN, "%=", self.column, self.line))
                    self.advance(2)
                else:
                    self.tokens_array.append(Token(TokenType.MOD, '%', self.column, self.line))
                    self.advance(1)
            
            #Assign sign and Equal operators
            elif self.peek(0) == '=':
                if self.peek(1) == '=':
                    self.tokens_array.append(Token(TokenType.EQUAL, "==", self.column, self.line))
                    self.advance(2)
                else:
                    self.tokens_array.append(Token(TokenType.ASSIGN, '=', self.column, self.line))
                    self.advance(1)
            
            #Less and Less and Equal operators
            elif self.peek(0) == '<':
                if self.peek(1) == '=':
                    self.tokens_array.append(Token(TokenType.LESS_EQUAL, "<=", self.column, self.line))
                    self.advance(2)
                else:
                    self.tokens_array.append(Token(TokenType.LESS, '<', self.column, self.line))
                    self.advance(1)
            
            #Greater and Greater and equal operators
            elif self.peek(0) == '>':
                if self.peek(1) == '=':
                    self.tokens_array.append(Token(TokenType.GREATER_EQUAL, ">=", self.column, self.line))
                    self.advance(2)
                else:
                    self.tokens_array.append(Token(TokenType.GREATER, '>', self.column, self.line))
                    self.advance(1)

            #Diferent operator
            elif self.peek(0) == '!' and self.peek(1) == '=':
                self.tokens_array.append(Token(TokenType.DIFERENT, "!=", self.column, self.line))
                self.advance(2)
            
            #Literals numbers
            elif self.peek(0).isdigit():
                self.scan_literal_number()
                
            #Strings
            elif self.peek(0) == "\"" or self.peek(0) == "'":
                self.scan_literal_string()
            
            #Identifiers or keywords
            elif self.peek(0).isalpha():
                self.scan_identifier_or_keyword()
            
            else:
                self.reporter.add_error(
                    f"[LexerError][line:{self.line}, col:{self.column}] Strange symbol found -> '{self.peek(0)}'"
                )
                self.advance(1)
              
        self.tokens_array.append(Token(TokenType.EOF, None, 0, 0))
        return self.tokens_array

