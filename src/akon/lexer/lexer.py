from string import ascii_letters
from .token import Token, TokenType
from akon.diagnostic.akon_errors import LexerError, ErrorReporter

class Lexer:
    keywords = {
        "var":TokenType.VAR,
        "let":TokenType.LET,
        "int":TokenType.INT,
        "float":TokenType.FLOAT,
        "string":TokenType.STRING,
        "bool":TokenType.BOOL,
        "True":TokenType.TRUE,
        "False":TokenType.FALSE,
        "if":TokenType.IF,
        "else":TokenType.ELSE,
        "elif":TokenType.ELIF,
        "and":TokenType.AND,
        "or":TokenType.OR,
        "not":TokenType.NOT,
        "none":TokenType.NONE,
    }
    
    def __init__(self, code:str, reporter:ErrorReporter) -> None:
        self.code = code
        self.position: int = 0
        self.column: int = 0
        self.line: int = 1
        self.current_char: str = self.code[self.position] if code else None
        self.tokens_array: list[Token] = [] 
        self.code_length: int = len(self.code)
        self.reporter = reporter

    def stop(self):
        raise Exception

    def advance(self) -> None:
        self.position += 1
        self.column += 1
        
        if self.current_char == '\n':
            self.column = 0
            self.line += 1
            
        if self.position < self.code_length:
            self.current_char = self.code[self.position]
        else:
            self.current_char = None
            
    def peek(self) -> str:
        if self.position + 1 == self.code_length:
            return ""
        
        return self.code[self.position + 1]
                                 
    def tokenize(self) -> list[Token]:
        while self.position < self.code_length:
             
            #Whitespaces and newlines
            if self.current_char.isspace():
                self.advance()
                    
            #Semicolon
            elif self.current_char == ';':
                self.tokens_array.append(Token(TokenType.SEMICOLON, ';', self.column, self.line))
                self.advance()
            
            #Comma
            elif self.current_char == ',':
                self.tokens_array.append(Token(TokenType.COMMA, ',', self.column, self.line))
                self.advance()
            
            #Left parenthesis
            elif self.current_char == '(':
                self.tokens_array.append(Token(TokenType.LPAREN, '(', self.column, self.line))
                self.advance()
            
            #Right parenthesis
            elif self.current_char == ')':
                self.tokens_array.append(Token(TokenType.RPAREN, ')', self.column, self.line))
                self.advance()
            
            #Left brace
            elif self.current_char == "{":
                self.tokens_array.append(Token(TokenType.LBRACE, '{', self.column, self.line))
                self.advance()
                
            #Right brace
            elif self.current_char == "}":
                self.tokens_array.append(Token(TokenType.RBRACE, '}', self.column, self.line))
                self.advance()
                
            #Operator of plus and comuest plus
            elif self.current_char == '+':
                if self.peek() == '=':
                    self.tokens_array.append(Token(TokenType.PLUS_ASSIGN, '+=', self.column, self.line))
                    self.advance()
                else:
                    self.tokens_array.append(Token(TokenType.PLUS, '+', self.column, self.line))
                    
                self.advance()

            #Operators od minus and compuest minus
            elif self.current_char == '-':
                if self.peek() == '=':
                    self.tokens_array.append(Token(TokenType.MINUS_ASSIGN, '-=', self.column, self.line))
                    self.advance()
                else:
                    self.tokens_array.append(Token(TokenType.MINUS, '-', self.column, self.line))
                    
                self.advance()
            
            #Operators of multiplication, power, compuest multiplication and compuest power
            elif self.current_char == '*':
                if self.peek() == '*':
                    self.advance()
                    
                    if self.peek() == '=':
                        self.tokens_array.append(Token(TokenType.DOUBLE_STAR_ASSIGN, "**=", self.column, self.line))
                        self.advance()
                    else:
                        self.tokens_array.append(Token(TokenType.DOUBLE_STAR, "**", self.column, self.line))
                        
                else:
                    if self.peek == '=':
                        self.tokens_array.append(Token(TokenType.STAR_ASSIGN, "*=", self.column, self.line))
                        self.advance()
                    else:
                        self.tokens_array.append(Token(TokenType.STAR, '*', self.column, self.line))
                
                self.advance()
                
            #Operators of division and compuest division, or comments of single-line and multi-line
            elif self.current_char == '/':
                if self.peek() == '/':
                    while (self.position < self.code_length and self.current_char != '\n'):
                        self.advance()
                        
                elif self.peek() == '*':
                    while (self.position < self.code_length):
                        self.advance()    
                
                        if self.current_char == '*':
                            self.advance()    
                    
                            if self.current_char == "/":
                                break
                    
                    if self.position == self.code_length:
                        self.reporter.add_error(
                            LexerError(
                                "You forgot to close the comment with these characters",
                                self.line,
                                self.column,
                                bad_char="*/",
                            )
                        )
                        self.stop()
                    
                elif self.peek() == '=':
                    self.tokens_array.append(Token(TokenType.SLASH_ASSIGN, '/=', self.column, self.line))
                    self.advance()
                
                else:
                    self.tokens_array.append(Token(TokenType.SLASH, '/', self.column, self.line))
                    
                    
                self.advance()    

            #Operators of mod and compound mod
            elif self.current_char == '%':
                if self.peek() == '=':
                    self.tokens_array.append(Token(TokenType.MOD_ASSIGN, "%=", self.column, self.line))
                    self.advance()
                else:
                    self.tokens_array.append(Token(TokenType.MOD, '%', self.column, self.line))
                    
                self.advance()
            
            #Assign sign and Equal operators
            elif self.current_char == '=':
                if self.peek == '=':
                    self.tokens_array.append(Token(TokenType.EQUAL, "==", self.column, self.line))
                    self.advance()
                else:
                    self.tokens_array.append(Token(TokenType.ASSIGN, '=', self.column, self.line))
                    
                self.advance()
            
            #Less and Less and Equal operators
            elif self.current_char == '<':
                if self.peek() == '=':
                    self.tokens_array.append(Token(TokenType.LESS_EQUAL, "<=", self.column, self.line))
                    self.advance()
                else:
                    self.tokens_array.append(Token(TokenType.LESS, '<', self.column, self.line))

                self.advance()
            
            #Greater and Greater and equal operators
            elif self.current_char == '>':
                if self.peek() == '=':
                    self.tokens_array.append(Token(TokenType.GREATER_EQUAL, ">=", self.column, self.line))
                    self.advance()
                else:
                    self.tokens_array.append(Token(TokenType.GREATER, '>', self.column, self.line))

                self.advance()

            #Diferent operator
            elif self.current_char == '!' and self.peek == '=':
                self.tokens_array.append(Token(TokenType.DIFERENT, "!=", self.column, self.line))
                self.advance()
                self.advance()
            
            #Literals numbers
            elif self.current_char.isdigit():
                start_pos = self.position
                while (self.position < self.code_length) and (self.current_char.isdigit() or self.current_char == '.'):
                    self.advance()
        
                numero_completo = self.code[start_pos:self.position]
                for letter in ascii_letters:
                    if letter in numero_completo:
                        self.reporter.add_error(
                            LexerError(
                                "Invalid numeric literal",
                                self.line,
                                self.column,
                                bad_char=numero_completo,
                            )
                        )
                        self.stop()
        
                if '.' in numero_completo:
                    self.tokens_array.append(Token(TokenType.NUMBER, float(numero_completo), self.column, self.line))
                else:
                    self.tokens_array.append(Token(TokenType.NUMBER, int(numero_completo), self.column, self.line))
            
            #Identifiers and keywords
            elif self.current_char.isalpha():
                start_pos = self.position
                while ((self.position < self.code_length) and (self.current_char.isalnum() or self.current_char == '_')):
                    self.advance()
                
                full_identifier = self.code[start_pos:self.position]
                if full_identifier in self.keywords.keys():
                    self.tokens_array.append(Token(self.keywords[full_identifier], full_identifier, self.column, self.line))
                else:
                    self.tokens_array.append(Token(TokenType.IDENT, full_identifier, self.column, self.line))
                
            #Strings
            elif self.current_char == "\"" or self.current_char == "\'":
                start_pos = self.position
                start_quotes = self.current_char
                self.advance()
                while (self.position < self.code_length) and (self.current_char != start_quotes or self.current_char == "\\"):
                    self.advance()
            
                self.advance()
                temporal_string = self.code[start_pos:self.position]
        
                if temporal_string[0] != start_quotes or temporal_string[-1] != start_quotes:
                    self.reporter.add_error(
                        LexerError(
                            "You forgot to close the string with quotation marks; use them at the end",
                            self.line,
                            self.column,
                            bad_char=start_quotes,
                        )
                    )
                    self.stop()
        
                if "\\n" in temporal_string:
                    temporal_string = temporal_string.replace("\\n", "\n")
                if "\\t" in temporal_string:
                    temporal_string = temporal_string.replace("\\t", "\t")
                if "\\\\" in temporal_string:
                    temporal_string = temporal_string.replace("\\\\", "\\")
                        
                temporal_string = temporal_string[1:-1]
                self.tokens_array.append(Token(TokenType.STRING_LITERAL, temporal_string, self.column, self.line))
            
            else:
                self.reporter.add_error(
                    LexerError(
                        "Strange symbol found",
                        self.line,
                        self.column,
                        bad_char=self.current_char,
                    )
                )
                self.stop()
              
        self.tokens_array.append(Token(TokenType.EOF, None, 0, 0))
        return self.tokens_array
