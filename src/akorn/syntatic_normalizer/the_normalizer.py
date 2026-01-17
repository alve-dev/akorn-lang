from akorn.scanner import Token, TokenType
from akorn.diagnostic import ErrorReporter

class TheNormalizer:
    tokens_valids = [
        TokenType.NUMBER,
        TokenType.STRING_LITERAL,
        TokenType.IDENT,
        TokenType.TRUE,
        TokenType.FALSE,
        TokenType.RPAREN,
        TokenType.CONTINUE,
        TokenType.BREAK  
    ]
    
    def __init__(self, tokens: list[Token], reporter: ErrorReporter):
        self.tokens = tokens
        self.index = 0
        self.lenght = len(tokens)
        self.reporter = reporter
        
    def is_valid(self, type: TokenType) -> bool:
        return type in self.tokens_valids
        
    def is_end(self) -> bool:
        return self.tokens[self.index].type == TokenType.EOF
    
    def peek_type(self, step: int) -> TokenType:
        if self.index + step > self.lenght:
            return TokenType.NONE
        
        if self.tokens[self.index + step] == TokenType.EOF:
            return TokenType.NONE
        
        return self.tokens[self.index + step].type
    
    def line(self) -> int:
        return self.tokens[self.index].line
        
    def column(self) -> int:
        return self.tokens[self.index].column
    
    def declare_error(self, msg: str):
        self.reporter.add_error(
            f"[TerminationError][line: {self.line()}, col: {self.column()}] {msg}"
        )
        self.index += 1
        
    def normalizer(self) -> list[Token]:
        depth = 0
        semicolon_mode: bool = None
        mode_verified = False
        
        while not self.is_end():
            if self.peek_type(0) == TokenType.NEWLINE:
                if not depth > 0:
                    if self.is_valid(self.peek_type(-1)) and self.peek_type(1) != TokenType.LBRACE:
                        if mode_verified and semicolon_mode:
                            self.declare_error("You are using both newlines and semicolons in the terminator; please use only one style.")
                        
                        self.tokens[self.index] = Token(TokenType.SEMICOLON, ';', self.column(), self.line())
                        
                        if not mode_verified:
                            semicolon_mode = False
                            mode_verified = True
                        
                        self.index += 1
                        
                    else:
                        self.tokens.pop(self.index)
                        self.lenght -= 1
                        
                else:
                    self.tokens.pop(self.index)
                    self.lenght -= 1
            
            
            elif self.peek_type(0) == TokenType.LPAREN:
                depth += 1
                self.index += 1
            
            elif (depth > 0) and (self.peek_type(0) == TokenType.RPAREN):
                depth -= 1
                self.index += 1
            
            elif (self.peek_type(0) == TokenType.SEMICOLON):
                if depth > 0:
                    self.declare_error("semicolon found in an unexpected place, remove it")
                
                elif mode_verified and not semicolon_mode:
                    self.declare_error("You are using both newlines and semicolons in the terminator; please use only one style.")
                    
                elif not self.is_valid(self.peek_type(-1)):
                    self.declare_error("Semicolon in an unexpected position, please remove it")
                
                else:
                    if not mode_verified:
                        semicolon_mode = True
                        mode_verified = True
                
                self.index += 1

            else:
                self.index += 1
                        
        
        
        if not semicolon_mode and self.is_valid(self.peek_type(-1)):
            column = self.tokens[self.index - 1].column + 1
            line = self.tokens[self.index - 1].line
            self.tokens.append(self.tokens[self.index])
            self.tokens[self.index] = Token(TokenType.SEMICOLON, ';', column, line)
            
        return self.tokens