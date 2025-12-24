from akon.lexer.token import Token, TokenType
from akon.ast.nodes import *
from akon.diagnostic.akon_errors import ParserError, NameErrorAkon, DeclarationError, MultiDeclarationError, ErrorReporter
from akon.enviroment.enviroment import Enviroment

class Parser:
    def __init__(self, tokens:list[Token], reporter: ErrorReporter, env: Enviroment) -> None:
        self.tokens: list[Token] = tokens
        self.position = 0
        self.current_token: Token = self.tokens[self.position] if tokens else Token(TokenType.EOF, None, 0, 0)
        self.length_list = len(self.tokens)
        self.reporter = reporter
        self.env = env

    def stop(self) -> None:
        raise Exception

    def eat(self, expected_token:TokenType) -> None:
        if self.current_token.type == expected_token:
            self.position += 1
            if self.position < self.length_list:
                self.current_token = self.tokens[self.position]
        else:
            self.error_reporter.add_error(
                ParserError(
                    "Parser found something unexpected",
                    self.current_token.line,
                    self.current_token.column,
                    expected = expected_token.v,
                    get = self.current_token.value
                    )
                )
            self.stop()
            
            if self.position < self.length_list:
                self.current_token = self.tokens[self.position]
    
    def at_end(self) -> bool:
        return self.current_token.type == TokenType.EOF
    
    def peek(self, expected_token: TokenType) -> bool:
        if self.position + 1 >= self.length_list:
            return False
        
        next_token = self.tokens[self.position + 1]
        return next_token.type == expected_token

    def peek_value(self) -> str:
        if self.position + 1 >= self.length_list:
            return ""
        
        next_token = self.tokens[self.position + 1]
        return f"'{next_token.value}'"
    
    def parse_statement(self) -> Node:
        #Declaracion de variables
        AKON_TYPES = [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL]
        
        if self.current_token.type in AKON_TYPES:
            if self.peek(TokenType.IDENT):
                var_type_token = self.current_token
                self.eat(var_type_token.type)
                return self.parse_declaration(var_type_token)
            else:
                self.reporter.add_error(
                    ParserError(
                        "Strange sentence found, perhaps you meant to make a variable declaration?",
                        self.current_token.line,
                        self.current_token.column,
                        expected="IDENTIFIER",
                        get=self.peek_value(),
                    )
                )
                self.stop() 
        
        #Asignacion de variables
        elif self.current_token.type == TokenType.IDENT:
            if self.peek(TokenType.ASSIGN):
                return self.parse_assignment()
            elif self.peek(TokenType.LPAREN):
                return self.parse_call_function()
                
        #Numero
        elif self.current_token.type == TokenType.NUMBER:
            return self.expression()
        
        #Strings Literals
        elif self.current_token.type == TokenType.STRING_LITERAL:
            return self.expression()
        
        #Algo extraño
        else:
            self.reporter.add_error(
                ParserError(
                    "Unexpected syntax error.",
                    self.current_token.line,
                    self.current_token.column,
                    expected="",
                    get="",
                )
            )
            self.stop()

    def valid_var(self, var_name: str, var_type: str, var_value: Node, line: int, column: int) -> bool | None:
        if self.env.define_var(var_name, var_type, var_value):
            return True
        else:
            self.reporter.add_error(
                    DeclarationError(
                        "You tried to redeclare an existing variable in scope",
                        line,
                        column,
                        name = var_name,
                    )
                )
            self.stop()

    def parse_declaration(self, var_type_token: TokenType) -> list[DeclarationNode]:
        node = self.parse_single_declaration(var_type_token)
        
        declarations = [node]
        #Posible multi-Declaration sino single-declaration
        if self.current_token.type == TokenType.COMMA:
            
            #Hay ident despues de la coma?, sino es error
            if self.peek(TokenType.IDENT):
                self.eat(TokenType.COMMA)
                for declaration in self.parse_declaration(var_type_token):
                    declarations.append(declaration)
                    
            else:
                self.reporter.add_error(
                    MultiDeclarationError(
                        "Possible attempt at multi-declaration of variables, and an ident was needed after the comma.",
                        self.current_token.line,
                        self.current_token.column
                    )
                )
        
        return declarations

    def parse_single_declaration(self, var_type_token: TokenType) -> DeclarationNode:
        #Locacion de la declaracion
        line_declaration = self.current_token.line
        column_declaration = self.current_token.column
        
        #Informacion de la declaracion
        var_type = var_type_token.value
        var_name = self.current_token.value
        self.eat(TokenType.IDENT)
        
        #Es declaracion + asignacion?
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            var_value = self.expression()
            self.valid_var(var_name, var_type, var_value, line_declaration, column_declaration)
            return DeclarationNode(var_name, var_type, var_value)
                        
        #Es declaracion sin asignacion o posible multi-declaration?
        elif self.current_token.type == TokenType.SEMICOLON or self.current_token.type == TokenType.COMMA:
            var_value = NoneNode(self.current_token.line, self.current_token.column)
            self.valid_var(var_name, var_type, var_value, line_declaration, column_declaration)
            return DeclarationNode(var_name, var_type, var_value)
        
        #Es una declaracion invalida
        else:
            self.reporter.add_error(
                    ParserError(
                        "Invalid variable declaration attempt.",
                        line_declaration,
                        column_declaration,
                        expected="'=' | ';' | ','",
                        get=self.current_token.value,
                    )
            )
            self.stop()          
         
    def parse_assignment(self) -> AssignmentNode:
        var_name = self.current_token.value
        self.eat(TokenType.IDENT)
        self.eat(TokenType.ASSIGN)
        
        var_value = self.expression()
        if self.env.assignment_var(var_name, var_value):
            return AssignmentNode(var_name, var_value)
        else:
            self.reporter.add_error(
                NameErrorAkon(
                    "You tried to access a non-existent variable",
                    self.current_token.line,
                    self.current_token.column,
                    name=var_name,
                )
            )
            self.stop()
    
    def parse_call_function(self) -> CallNode:
        call_name = self.current_token.value
        self.eat(TokenType.IDENT)
        self.eat(TokenType.LPAREN)
        call_args = []
        
        while True:
            current_arg = self.expression()
            call_args.append(current_arg)
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                continue
            elif self.current_token.type == TokenType.RPAREN:
                self.eat(TokenType.RPAREN)
                break
            else:
                self.reporter.add_error(
                    ParserError(
                        f"Attempt to call {call_name} function failed",
                        self.current_token.line,
                        self.current_token.column,
                        expected="",
                        get="",
                    )
                )
                self.stop()
        
        return CallNode(call_name, call_args)
            
    def parse_program(self) -> ProgramNode:
        statements: list[Node] = []
        while not self.at_end():
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
                
            if self.at_end():
                break
            
            node = self.parse_statement()
            
            if isinstance(node, list):
                for statement in node:
                    statements.append(statement)
            else:
                statements.append(node)
            
        return ProgramNode(statements)
        
    def expression(self) -> Node:
        return self.not_boolean_expr()

    def not_boolean_expr(self) -> Node:
        if self.current_token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            node = NotBooleanNode(self.not_boolean_expr())
        else:
            node = self.boolean_expr()
            
        return node

    def boolean_expr(self) -> Node:
        node = self.comp_expr()
        
        while self.current_token.type in [TokenType.AND, TokenType.OR]:
            operator = self.current_token.value
            self.eat(self.current_token.type)
            node = BooleanOpNode(node, operator, self.expression())
        
        return node

    def comp_expr(self) -> Node:
        node = self.add_expr()
        
        sign_comparison = [TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL,
                           TokenType.EQUAL, TokenType.DIFERENT]
        
        while self.current_token.type in sign_comparison:
            operator = self.current_token.value
            self.eat(self.current_token.type)
            node = ComparisonOpNode(node, operator, self.comp_expr())
        
        return node    
            
    def add_expr(self) -> Node:
        node = self.mult_expr()
        
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.value
            token_type = self.current_token.type
            self.eat(token_type)            
            node = BinaryOpNode(node, op, self.mult_expr())
            
        return node
    
    def mult_expr(self) -> Node:
        node = self.unary_expr()
        
        while self.current_token.type in [TokenType.STAR, TokenType.SLASH, TokenType.MOD]:
            op = self.current_token.value
            token_type = self.current_token.type
            self.eat(token_type)
            node = BinaryOpNode(node, op, self.mult_expr())
            
        return node
    
    def unary_expr(self) -> Node:
        if self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            operator = self.current_token.value
            token_type = self.current_token.type
            self.eat(token_type)
            node = UnaryNode(operator, self.unary_expr())
            
        else:
            node = self.power_expr()
            
        return node
    
    def power_expr(self) -> Node:
        node = self.primitive()
        
        while self.current_token.type == TokenType.DOUBLE_STAR:
            op = "**"
            self.eat(TokenType.DOUBLE_STAR)
            node = BinaryOpNode(node, op, self.power_expr())
            
        return node
    
    def primitive(self) -> Node:
        # Is a NUMBER?
        if self.current_token.type == TokenType.NUMBER:
            if isinstance(self.current_token.value, float):
                node = FloatNode(self.current_token.value, self.current_token.line, self.current_token.column)
            else:
                node = IntNode(self.current_token.value, self.current_token.line, self.current_token.column)
            
            self.eat(TokenType.NUMBER)
            return node

        # is a STRING_LITERAL
        if self.current_token.type == TokenType.STRING_LITERAL:
            node = StringNode(self.current_token.value, self.current_token.line, self.current_token.column)
            self.eat(TokenType.STRING_LITERAL)
            return node
        
        # is a bool
        if self.current_token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return BoolNode(True, self.current_token.line, self.current_token.column)
        if self.current_token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return BoolNode(False, self.current_token.line, self.current_token.column)
        
        #is a None value
        if self.current_token.type == TokenType.NONE:
            self.eat(TokenType.NONE)
            return NoneNode(self.current_token.line, self.current_token.column)
        
        # Is a LPAREN?
        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node
        
        #Is a identifier?
        elif self.current_token.type == TokenType.IDENT:
            if self.env.lookup_var(self.current_token.value):
                node = VariableNode(self.current_token.value, self.current_token.line, self.current_token.column)
                self.eat(TokenType.IDENT)
                return node
            else:
                self.reporter.add_error(
                NameErrorAkon(
                    "You tried to access a non-existent variable",
                    self.current_token.line,
                    self.current_token.column,
                    name=self.current_token.value,
                )
            )
            self.stop()
                
            
        else:
            self.error_reporter.add_error(
                ParserError(
                    "unexpected primitive",
                    self.current_token.line,
                    self.current_token.column,
                    expected = "",
                    get = self.current_token.value
                )
            )
            self.eat(self.current_token.type)

