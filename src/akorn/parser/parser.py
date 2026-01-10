from akorn.scanner import Token, TokenType
from akorn.ast import *
from akorn.diagnostic import ErrorReporter
from akorn.enviroment import Enviroment

class Parser:
    def __init__(self, tokens:list[Token], reporter: ErrorReporter) -> None:
        self.tokens: list[Token] = tokens
        self.position = 0
        self.current_token: Token = self.tokens[self.position] if tokens else Token(TokenType.EOF, None, 0, 0)
        self.length_list = len(self.tokens)
        self.reporter = reporter


    def stop(self):
        raise Exception


    def eat(self, expected_token:TokenType) -> None:
        if self.current_token.type == expected_token:
            self.position += 1
            if self.position < self.length_list:
                self.current_token = self.tokens[self.position]
        else:
            line = self.current_token.line
            col = self.current_token.column
            expected = expected_token.value
            get = self.current_token.value
            
            self.reporter.add_error(
                f"[ParserError][line: {line}, col: {col}] Parser found something unexpected (expected: {expected} , get: {get})"
                )
            self.stop()
            
            
            if self.position < self.length_list:
                self.current_token = self.tokens[self.position]
    
    
    def at_end(self) -> bool:
        return self.current_token.type == TokenType.EOF
    
    
    def peek(self, expected_token: TokenType | list[TokenType]) -> bool:
        if self.position + 1 >= self.length_list:
            return False
        
        next_token = self.tokens[self.position + 1]
        if isinstance(expected_token, list):
            for token_type in expected_token:
                if next_token.type == token_type:
                    return True
            
            return False
        else:
            return next_token.type == expected_token


    def peek_value(self) -> str:
        if self.position + 1 >= self.length_list:
            return ""
        
        next_token = self.tokens[self.position + 1]
        return f"'{next_token.value}'"
    
    
    def parse_statement(self, scope: Enviroment) -> Node:
        #Declaracion de variables
        AKON_TYPES = [TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL]
        if self.current_token.type in [TokenType.VAR, TokenType.LET]:
            if self.peek(AKON_TYPES):
                constant: bool = False
                
                if self.current_token.type == TokenType.LET:
                    constant = True
            
                self.eat(self.current_token.type)
                
                data_type = self.current_token.value
                self.eat(self.current_token.type)
                
                return self.parse_declaration(data_type, constant, scope)
            
            else:
                line = self.current_token.line
                col = self.current_token.column
                expected = "DATA_TYPE"
                get = self.peek_value()
                
                self.reporter.add_error(
                    f"[ParserError][line: {line}, col: {col}] Strange sentence found, perhaps you meant to make a variable declaration?(Expected: {expected}, Get:{get})"
                )
                self.stop()

        elif self.current_token.type in AKON_TYPES:
            line = self.current_token.line
            col = self.current_token.column
            
            self.reporter.add_error(
                f"[ParserError][line: {line}, col: {col}]Incorrect variable declaration, remember to use the keyword 'var' or 'let' at the beginning of a declaration and before the data type (e.g., 'int')"
            )
            self.stop()
        
        #Asignacion de variables o llamado a funcion
        elif self.current_token.type == TokenType.IDENT:
            if self.peek(TokenType.LPAREN):
                return self.parse_call_function(scope)
            else:
                return self.parse_assignment(scope)
            
        #If-Elif-Else
        elif self.current_token.type == TokenType.IF:
            return self.parse_if_statement(scope)

        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while_statement(scope)
        
        #Algo extraño
        else:
            line = self.current_token.line
            col = self.current_token.column
            
            self.reporter.add_error(
                f"[ParserError][line: {line}, col: {col}] Unexpected syntax error"
            )
            self.stop()
            
            
    def valid_var(self, var_name: str, data_type: str, constant: bool, var_value: Node, line: int, column: int, scope: Enviroment) -> bool | None:
        if scope.define_var(var_name, data_type, constant, var_value):
            return True
        else:
            self.reporter.add_error(
                f"[DeclarationError][line: {line}, col: {column}] You tried to redeclare an existing variable in scope, '{var_name}'"
            )
            self.stop()
            

    def parse_declaration(self, data_type: str, constant: bool, scope: Enviroment) -> list[DeclarationNode]:
        node = self.parse_single_declaration(data_type, constant, scope)
        
        declarations = [node]
        #Posible multi-Declaration sino single-declaration
        if self.current_token.type == TokenType.COMMA:
            
            #Hay ident despues de la coma?, sino es error
            if self.peek(TokenType.IDENT):
                self.eat(TokenType.COMMA)
                for declaration in self.parse_declaration(data_type, constant, scope):
                    declarations.append(declaration)
                    
            else:
                line = self.current_token.line
                col = self.current_token.column
                
                self.reporter.add_error(
                    f"[MultiDeclarationError][line: {line}, col: {col}] Possible attempt at multi-declaration of variables, and an ident was needed after the comma"
                )
                self.stop()
            
        return declarations
    

    def parse_single_declaration(self, data_type: str, constant: bool, scope: Enviroment) -> DeclarationNode:
        #Locacion de la declaracion
        line_declaration = self.current_token.line
        column_declaration = self.current_token.column
        
        var_name = self.current_token.value
        self.eat(TokenType.IDENT)
        
        #Es declaracion + asignacion?
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            var_value = self.expression(scope)
            self.valid_var(var_name, data_type, constant, var_value, line_declaration, column_declaration, scope)
            return DeclarationNode(var_name, data_type, var_value)
                        
        #Es declaracion sin asignacion o posible multi-declaration?
        elif self.current_token.type == TokenType.SEMICOLON or self.current_token.type == TokenType.COMMA:
            var_value = NoneNode(self.current_token.line, self.current_token.column)
            self.valid_var(var_name, data_type, constant, var_value, line_declaration, column_declaration, scope)
            return DeclarationNode(var_name, data_type, var_value)
        
        #Es una declaracion invalida
        else:
            expected = "'=' | ';' | ','"
            get = self.current_token.value
            
            self.reporter.add_error(
                f"[ParserError][line: {line_declaration}, col: {column_declaration}] Invalid variable declaration attempt. (expected: {expected}, get: {get})"
            )
            self.stop()

         
    def parse_assignment(self, scope) -> AssignmentNode:
        var_name = self.current_token.value
        self.eat(TokenType.IDENT)
        
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            var_value = self.expression(scope)
        else:
            compuest_signs = [TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN,
                            TokenType.DOUBLE_STAR_ASSIGN, TokenType.MOD_ASSIGN]
            if self.current_token.type in compuest_signs:
                operator: str = None
                
                if self.current_token.type == TokenType.PLUS_ASSIGN:
                    operator = '+'
                elif self.current_token.type == TokenType.MINUS_ASSIGN:
                    operator = '-'
                elif self.current_token.type == TokenType.STAR_ASSIGN:
                    operator = '*'
                elif self.current_token.type == TokenType.SLASH_ASSIGN:
                    operator = '/'
                elif self.current_token.type == TokenType.DOUBLE_STAR_ASSIGN:
                    operator = '**'
                elif self.current_token.type == TokenType.MOD_ASSIGN:
                    operator = '%'
                
                self.eat(self.current_token.type)
                var_value = BinaryOpNode(
                    VariableNode(var_name, self.current_token.line, self.current_token.column),
                    operator,
                    self.expression(scope)
                    )
        
        if scope.assignment_var(var_name, var_value):
            return AssignmentNode(var_name, var_value)
        else:
            line = self.current_token.line 
            col = self.current_token.column
            
            self.reporter.add_error(
                f"[NameError][line: {line}, col: {col}] You tried to access a non-existent variable, '{var_name}'"
            )
            self.stop()
            

    def parse_call_function(self, scope) -> CallNode:
        call_name = self.current_token.value
        self.eat(TokenType.IDENT)
        self.eat(TokenType.LPAREN)
        call_args = []
        
        while True:
            current_arg = self.expression(scope)
            call_args.append(current_arg)
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                continue
            elif self.current_token.type == TokenType.RPAREN:
                self.eat(TokenType.RPAREN)
                break
            else:
                line = self.current_token.line
                col = self.current_token.column
                
                self.reporter.add_error(
                    f"[ParserError][line: {line}, col: {col}] Attempt to call '{call_name}' function failed"
                )
                self.stop()
                
        return CallNode(call_name, call_args)
            
            
    def parse_if_statement(self, scope: Enviroment) -> IfNode:
        branches = []
    
        #Condition
        self.eat(TokenType.IF)
        condition = self.expression(scope)
        
        block = self.parse_block(scope)
        branches.append((condition, block))
        
        while self.current_token.type == TokenType.ELIF:
            self.eat(TokenType.ELIF)
            condition = self.expression(scope)
            
            block = self.parse_block(scope)
            branches.append((condition, block))

        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            block = self.parse_block(scope)
            else_node = ElseNode(block)
            
        else:
            else_node = NoneNode(self.current_token.line, self.current_token.column)
            
        
        return IfNode(branches, else_node)        
    
    
    def parse_while_statement(self, scope: Enviroment) -> WhileNode:
        self.eat(TokenType.WHILE)
        cond = self.expression(scope)
        block = self.parse_block(scope)
        
        return WhileNode(cond, block)
    
    
    def parse_block(self, scope: Enviroment):
        line_block = self.current_token.line
        column_block = self.current_token.column
        self.eat(TokenType.LBRACE)
        scope_block = Enviroment(scope)
        statements = []
        
        while True:
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)

            if self.at_end():
                self.reporter.add_error(
                    f"[ParserError][line: {line_block}, col: {column_block}] " + "A '}' is expected when closing a statement."
                )
                self.stop()
                
            if self.current_token.type == TokenType.RBRACE:
                self.eat(TokenType.RBRACE)
                break
            
            node = self.parse_statement(scope)
            
            if isinstance(node, list):
                for statement in node:
                    statements.append(statement)
            else:
                statements.append(node)
        
        return BlockNode(statements, scope_block)
              
                
    def parse_program(self) -> ProgramNode:
        statements: list[Node] = []
        scope = Enviroment()
        while not self.at_end():
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
                
            if self.at_end():
                break
            
            node = self.parse_statement(scope)
            
            if isinstance(node, list):
                for statement in node:
                    statements.append(statement)
            else:
                statements.append(node)
            
        return ProgramNode(statements, scope)
        
        
    def expression(self, scope) -> Node:
        return self.not_boolean_expr(scope)
    
    
    def not_boolean_expr(self, scope) -> Node:
        if self.current_token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            node = NotBooleanNode(self.not_boolean_expr(scope))
        else:
            node = self.boolean_expr(scope)
            
        return node


    def boolean_expr(self, scope) -> Node:
        node = self.comp_expr(scope)
        
        while self.current_token.type in [TokenType.AND, TokenType.OR]:
            operator = self.current_token.value
            self.eat(self.current_token.type)
            node = BooleanOpNode(node, operator, self.expression(scope))
        
        return node


    def comp_expr(self, scope) -> Node:
        node = self.add_expr(scope)
        
        sign_comparison = [TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL,
                           TokenType.EQUAL, TokenType.DIFERENT]
        
        while self.current_token.type in sign_comparison:
            operator = self.current_token.value
            self.eat(self.current_token.type)
            node = ComparisonOpNode(node, operator, self.comp_expr(scope))
        
        return node    
        
            
    def add_expr(self, scope) -> Node:
        node = self.mult_expr(scope)
        
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.value
            token_type = self.current_token.type
            self.eat(token_type)            
            node = BinaryOpNode(node, op, self.mult_expr(scope))
            
        return node
    
    
    def mult_expr(self, scope) -> Node:
        node = self.unary_expr(scope)
        
        while self.current_token.type in [TokenType.STAR, TokenType.SLASH, TokenType.MOD]:
            op = self.current_token.value
            token_type = self.current_token.type
            self.eat(token_type)
            node = BinaryOpNode(node, op, self.mult_expr(scope))
            
        return node
    
    
    def unary_expr(self, scope) -> Node:
        if self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            operator = self.current_token.value
            token_type = self.current_token.type
            self.eat(token_type)
            node = UnaryNode(operator, self.unary_expr(scope))
            
        else:
            node = self.power_expr(scope)
            
        return node
    
    
    def power_expr(self, scope) -> Node:
        node = self.primitive(scope)
        
        while self.current_token.type == TokenType.DOUBLE_STAR:
            op = "**"
            self.eat(TokenType.DOUBLE_STAR)
            node = BinaryOpNode(node, op, self.power_expr(scope))
            
        return node
    
    
    def primitive(self, scope) -> Node:
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
            node = self.expression(scope)
            self.eat(TokenType.RPAREN)
            return node
        
        #Is a identifier?
        elif self.current_token.type == TokenType.IDENT:
            if self.peek(TokenType.LPAREN):
                return self.parse_call_function(scope)
            else:
                if scope.lookup_var(self.current_token.value):
                    node = VariableNode(self.current_token.value, self.current_token.line, self.current_token.column)
                    self.eat(TokenType.IDENT)
                    return node
                else:
                    line = self.current_token.line
                    col = self.current_token.column
                    name = self.current_token.value
                    
                    self.reporter.add_error(
                        f"[NameErrorAkorn][line: {line}, col: {col}] You tried to access a non-existent variable, '{name}'"
                    )
                self.stop()
                
        else:
            line = self.current_token.line
            col = self.current_token.column
            
            self.error_reporter.add_error(
                f"[ParserError][line: {line}, col: {col}] Unexpected primitive"
            )
            self.eat(self.current_token.type)
            
