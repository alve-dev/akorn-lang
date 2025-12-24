from string import ascii_letters
from .token import Token, TokenType
from akon.diagnostic.akon_errors import LexerError, ErrorReporter

class Lexer:
    keywords = {
        "Int":TokenType.INT,
        "Float":TokenType.FLOAT,
        "String":TokenType.STRING,
        "Bool":TokenType.BOOL,
        "True":TokenType.TRUE,
        "False":TokenType.FALSE,
        "if":TokenType.IF,
        "and":TokenType.AND,
        "or":TokenType.OR,
        "not":TokenType.NOT,
        "None":TokenType.NONE,
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

    def _read_comment(self) -> int | str:
        #comment one line
        if self.current_char == "/":
            while (self.position < self.code_length and self.current_char != '\n'):
                self.advance()

        #comment multi-line
        elif self.current_char == '*':
            while (self.position < self.code_length):
                self.advance()    
                
                if self.current_char == '*':
                    self.advance()    
                    
                    if self.current_char == "/":
                        self.advance()
                        return
                
            self.reporter.add_error(
                LexerError(
                    "You forgot to close the comment with these characters",
                    self.line,
                    self.column,
                    bad_char="*/",
                )
            )
            self.stop()
                              
    def _read_number(self) -> Token:
        #Logica para identificar numeros
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
                return None
        
        if '.' in numero_completo:
            return Token(TokenType.NUMBER, float(numero_completo), self.column, self.line)
        else:
            return Token(TokenType.NUMBER, int(numero_completo), self.column, self.line)
        
    def _read_ident(self) -> Token:
        start_pos = self.position
            
        while self.position < self.code_length and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()
                
        full_identifier = self.code[start_pos:self.position]
        if full_identifier in self.keywords.keys():
            return Token(self.keywords[full_identifier], full_identifier, self.column, self.line)
        else:
            return Token(TokenType.IDENT, full_identifier, self.column, self.line)
    
    def _read_string(self) -> Token:
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
            return None
        
        if "\\n" in temporal_string:
            temporal_string = temporal_string.replace("\\n", "\n")
        if "\\t" in temporal_string:
            temporal_string = temporal_string.replace("\\t", "\t")
        if "\\\\" in temporal_string:
            temporal_string = temporal_string.replace("\\\\", "\\")
                
        temporal_string = temporal_string[1:-1]
        return Token(TokenType.STRING_LITERAL, temporal_string, self.column, self.line)

    def _read_star(self) -> Token:
        start_pos = self.position
        while (self.position < self.code_length and self.current_char == '*'):
            self.advance()
            
        temporal_sign = self.code[start_pos:self.position]
        if temporal_sign == '*':
            token = Token(TokenType.STAR, '*', self.column, self.line)
        elif temporal_sign == "**":
            token = Token(TokenType.DOUBLE_STAR, '**', self.column, self.line)
        else:
            self.reporter.add_error(
                LexerError(
                    "Strange symbol found, you might want to use '*' or '**'",
                    self.line,
                    self.column,
                    bad_char=temporal_sign
                )
            )
            self.stop()
            return None
        
        return token

    def _read_equal(self) -> Token:
        start_pos = self.position
        while self.position < self.code_length and self.current_char == "=":
            self.advance()
                
        temporal_sign = self.code[start_pos:self.position]
        if temporal_sign == '=':
            token = Token(TokenType.ASSIGN, '=', self.column, self.line)
        elif temporal_sign == "==":
            token = Token(TokenType.EQUAL, "==", self.column, self.line)
        else:
            self.reporter.add_error(
                LexerError(
                    "Strange symbol found, you might want to use '=' or '=='",
                    self.line,
                    self.column,
                    bad_char=temporal_sign,
                )
            )
            self.stop()
            return None
        
        return token        
    
    def _read_comparison(self) -> Token:
        start_pos = self.position
        while self.position < self.code_length and (self.current_char in ['<', '>', '!'] or self.current_char == '='):
            self.advance()
                          
        temporal_sign = self.code[start_pos:self.position]
        if temporal_sign == '<':
            token = Token(TokenType.LESS, '<', self.column, self.line)
        elif temporal_sign == '>':
            token = Token(TokenType.GREATER, '>', self.column, self.line)
        elif temporal_sign == '>=':
            token = Token(TokenType.GREATER_EQUAL, ">=", self.column, self.line)
        elif temporal_sign == '<=':
            token = Token(TokenType.LESS_EQUAL, "<=", self.column, self.line)
        elif temporal_sign == '!=':
            token = Token(TokenType.DIFERENT, "!=", self.column, self.line)
        else:
            self.reporter.add_error(
                LexerError(
                    "Strange symbol found, you might want to use '<', '>', '<=', '>=' or '!='",
                    self.line,
                    self.column,
                    bad_char=temporal_sign,
                )
            )
            self.stop()
            return None
        
        return token
            
    def get_tokens(self) -> list[Token]:
        while self.position < self.code_length:
             
            #Whitespaces and newlines
            if self.current_char.isspace():
                self.advance()
                    
            #Semicolon
            elif self.current_char == ';':
                token = Token(TokenType.SEMICOLON, ';', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            
            #Comma
            elif self.current_char == ',':
                token = Token(TokenType.COMMA, ',', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            
            #Parenthesis, Brackets and Braces
            elif self.current_char == '(':
                token = Token(TokenType.LPAREN, '(', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == ')':
                token = Token(TokenType.RPAREN, ')', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == "{":
                token = Token(TokenType.LBRACE, '{', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == "}":
                token = Token(TokenType.RBRACE, '}', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
                
            #Aritmethic Operators
            elif self.current_char == '+':
                token = Token(TokenType.PLUS, '+', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == '-':
                token = Token(TokenType.MINUS, '-', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            elif self.current_char == '*':
                token = self._read_star()
                if token != None:
                    self.tokens_array.append(token)
                    
            #Slash = commenst or division
            elif self.current_char == '/':
                self.advance()
                if self.current_char == '/' or self.current_char == '*':
                    self._read_comment()
                else:
                    token = Token(TokenType.SLASH, '/', self.column, self.line)
                    self.tokens_array.append(token)
                    
            elif self.current_char == '%':
                token = Token(TokenType.MOD, '%', self.column, self.line)
                self.tokens_array.append(token)
                self.advance()
            
            #Assign sign and Equal sign
            elif self.current_char == '=':
                token = self._read_equal()
                if token != None:
                    self.tokens_array.append(token)
            
            #Comparison signs, except equal
            elif self.current_char in ['<', '>', '!']:
                token = self._read_comparison()
                if token != None:
                    self.tokens_array.append(token)
            
            #Numbers
            elif self.current_char.isdigit():
                token = self._read_number()
                if token != None:
                    self.tokens_array.append(token)
            
            #Identifiers and Keywords
            elif self.current_char.isalpha():
                token = self._read_ident()
                if token != None:
                    self.tokens_array.append(token)
                
            #Strings
            elif self.current_char == "\"" or self.current_char == "\'":
                token = self._read_string()
                if token != None:
                    self.tokens_array.append(token)
            
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
