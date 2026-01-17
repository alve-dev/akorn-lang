from akorn.scanner import Token, TokenType
from akorn.ast import *
from akorn.diagnostic import ErrorReporter
from akorn.enviroment import Enviroment

class Parser:
    def __init__(self, tokens:list[Token], reporter: ErrorReporter) -> None:
        self.tokens: list[Token] = tokens
        self.position = 0
        self.length_list = len(self.tokens)
        self.reporter = reporter


    def at_end(self) -> bool:
        return self.tokens[self.position].type == TokenType.EOF


    def advance(self) -> bool:
        if self.at_end():
            return False
        
        self.position += 1
        return True


    def synchronize(self):
        while not self.at_end():
            if self.peek_token(0).type == TokenType.SEMICOLON:
                return
        
            match self.peek_token(0).type:
                case TokenType.VAR : return
                case TokenType.LET : return
                case TokenType.IDENT : return
                case TokenType.IF : return
                case TokenType.WHILE : return
                case TokenType.LOOP : return
                case _: pass
                
            self.advance()            
    

    def peek_token(self, step) -> Token:
        if self.position + step >= self.length_list:
            return None
        
        return self.tokens[self.position + step]


    #Seguir mañana y arreglar los comentarios de errores en las lines e columnas

    def line(self) -> int:
        if self.at_end:
            return self.peek_token(-1).line
        return self.peek_token(0).line
    
    
    def column(self) -> int:
        if self.at_end:
            return self.peek_token(-1).column
        return self.peek_token(0).column
    
    
    def check(self, type: TokenType) -> bool:
        if self.at_end(): 
            return False
    
        return self.peek_token(0).type == type


    def match_token_type(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        
        return False


    def declare_error(self, message):
        self.reporter.add_error(
                f"[ParserError][line: {self.line()}, col: {self.column()}] {message}"
            )
        self.synchronize()


    def eat(self, type: TokenType, message: str) -> bool:
        if not self.match_token_type(type):
            self.declare_error(message)
            return False
        
        return True
    
    
    def parse_statement(self, scope: Enviroment) -> Node:
        none_aux = NoneNode(self.line(), self.column())
        
        #Declaracion de variables
        if self.match_token_type(TokenType.VAR, TokenType.LET):
            if self.match_token_type(TokenType.INT, TokenType.FLOAT, TokenType.STRING, TokenType.BOOL):
                constant: bool = False
                
                if self.peek_token(-2).type == TokenType.LET:
                    constant = True
            
                data_type = self.peek_token(-1).value
                
                return self.parse_declaration(data_type, constant, scope)
            
            else:
                self.declare_error("The variable declaration attempt failed; the variable's data type was missing after the mutated type.")
                return none_aux
        
        #Asignacion de variables o llamado a funcion
        elif self.match_token_type(TokenType.IDENT):
            if self.match_token_type(TokenType.LPAREN):
                return self.parse_call_function(scope)
            else:
                return self.parse_assignment(scope)
            
        #If Statement
        elif self.match_token_type(TokenType.IF):
            return self.parse_if_statement(scope)

        # While Statement
        elif self.match_token_type(TokenType.WHILE):
            return self.parse_while_statement(scope, False)
        
        # Loop Statement
        elif self.match_token_type(TokenType.LOOP):
            return self.parse_while_statement(scope, True)
        
        # Break Statement
        elif self.match_token_type(TokenType.BREAK):
            return BreakStatement()

        # Continue Statement
        elif self.match_token_type(TokenType.CONTINUE):
            return ContinueStatement()
            
        #Algo extraño
        else:
            self.declare_error("Unexpected syntax error")
            return none_aux
            
            
    def valid_var(self, var_name: str, data_type: str, constant: bool, var_value: Node, scope: Enviroment) -> bool | None:
        if scope.define_var(var_name, data_type, constant, var_value):
            return True
        else:
            self.declare_error(f"You tried to redeclare an existing variable in scope, '{var_name}'")
            return False
            

    def parse_declaration(self, data_type: str, constant: bool, scope: Enviroment) -> list[DeclarationNode]:
        node = self.parse_single_declaration(data_type, constant, scope)
        
        declarations = [node]
        #Posible multi-Declaration sino single-declaration
        if self.match_token_type(TokenType.COMMA):
            
            for declaration in self.parse_declaration(data_type, constant, scope):
                declarations.append(declaration)
            
        return declarations
    

    def parse_single_declaration(self, data_type: str, constant: bool, scope: Enviroment) -> DeclarationNode:
        #Locacion de la declaracion
        none_aux = NoneNode(self.line(), self.column())
        
        if not self.eat(TokenType.IDENT, "Variable declaration attempt failed, identifier not declared"):
            return none_aux
        
        var_name = self.peek_token(-1).value
        
        #Es declaracion + asignacion?
        if self.match_token_type(TokenType.ASSIGN):
            var_value = self.expression(scope)
        elif self.check(TokenType.SEMICOLON) or self.check(TokenType.COMMA):
            var_value = none_aux
        else:
            self.declare_error("Variable declaration attempt failed; neither assignment operator ('=') for initialization \nnor semicolon (';') to terminate the statement with an empty declaration was found.")
            return none_aux
        
        if self.valid_var(var_name, data_type, constant, var_value, scope):
            return DeclarationNode(var_name, data_type, var_value)
        else:
            return none_aux
        
         
    def parse_assignment(self, scope) -> AssignmentNode:
        var_name = self.peek_token(-1).value
        none_aux = NoneNode(self.line(), self.column())
        
        if self.match_token_type(TokenType.ASSIGN):
            var_value = self.expression(scope)
            
        elif self.match_token_type(TokenType.PLUS_ASSIGN):
            var_value = BinaryOpNode(
                VariableNode(var_name, self.line(), self.column()),
                "+",
                self.expression(scope)
            )
        
        elif self.match_token_type(TokenType.MINUS_ASSIGN):
            var_value = BinaryOpNode(
                VariableNode(var_name, self.line(), self.column()),
                "-",
                self.expression(scope)
            )
        
        elif self.match_token_type(TokenType.STAR_ASSIGN):
            var_value = BinaryOpNode(
                VariableNode(var_name, self.line(), self.column()),
                "*",
                self.expression(scope)
            )
        
        elif self.match_token_type(TokenType.SLASH_ASSIGN):
            var_value = BinaryOpNode(
                VariableNode(var_name, self.line(), self.column()),
                "/",
                self.expression(scope)
            )
        
        elif self.match_token_type(TokenType.DOUBLE_STAR_ASSIGN):
            var_value = BinaryOpNode(
                VariableNode(var_name, self.line(), self.column()),
                "**",
                self.expression(scope)
            )
        
        elif self.match_token_type(TokenType.MOD_ASSIGN):
            var_value = BinaryOpNode(
                VariableNode(var_name, self.line(), self.column()),
                "%",
                self.expression(scope)
            )
                
        else:
            self.declare_error("The attempt to assign to a variable failed; the common assignment operator or compound assignment operator was not found.")
            return none_aux
        
        if scope.assignment_var(var_name, var_value):
            return AssignmentNode(var_name, var_value)    
        else:
            self.declare_error(f"Variable assignment attempt failed, variable '{var_name}' does not exist")
            return none_aux
            

    def parse_call_function(self, scope) -> CallNode | NoneNode:
        call_name = self.peek_token(-2).value
        call_args = []
        
        while True:
            current_arg = self.expression(scope)
            call_args.append(current_arg)
            if self.match_token_type(TokenType.COMMA):
                continue
            elif self.match_token_type(TokenType.RPAREN):
                break
            else:
                self.declare_error("The function call failed; I needed closing parenthesis ')' or ',' to continue providing arguments.")
                return NoneNode(self.line(), self.column())
                
        return CallNode(call_name, call_args)
            
            
    def parse_if_statement(self, scope: Enviroment) -> IfNode:
        branches = []
        
        #Condition
        condition = self.expression(scope)
        
        block = self.parse_block(scope)
        branches.append((condition, block))
        
        while self.match_token_type(TokenType.ELIF):
            condition = self.expression(scope)
            
            block = self.parse_block(scope)
            branches.append((condition, block))

        if self.match_token_type(TokenType.ELSE):
            block = self.parse_block(scope)
            else_node = ElseNode(block)
            
        else:
            else_node = NoneNode(self.line(), self.column())
            
        
        return IfNode(branches, else_node)        
    
    
    def parse_while_statement(self, scope: Enviroment, loop: bool) -> WhileNode:
        if loop:
            cond = BoolNode(True, self.current_token.line, self.current_token.column)
        else:
            cond = self.expression(scope)
            
        block = self.parse_block(scope)
        
        return WhileNode(cond, block)
    
    
    def parse_block(self, scope: Enviroment) -> BlockNode | NoneNode:
        none_aux = NoneNode(self.line(), self.column())
        
        if not self.eat(TokenType.LBRACE, "Attempt at statement with code block failed, opening block '{' could not be found"):
            return none_aux
            
        scope_block = Enviroment(scope)
        statements = []
        
        while True:
            if self.match_token_type(TokenType.SEMICOLON):
                continue

            if self.at_end():
                self.declare_error("Attempt at statement with code block failed, block closure '}' not found")
                return none_aux
                
            if self.match_token_type(TokenType.RBRACE):
                break
            
            node = self.parse_statement(scope_block)
            
            if isinstance(node, list):
                for statement in node:
                    statements.append(statement)
            else:
                statements.append(node)
        
        return BlockNode(statements, scope_block)
              
                
    def parse_program(self) -> ProgramNode:
        statements: list[Node] = []
        scope = Enviroment()
        
        while True:
            if self.match_token_type(TokenType.SEMICOLON):
                continue
                
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
        return self.or_expr(scope)
    

    def or_expr(self, scope) -> Node:
        node = self.and_expr(scope)
        
        while self.match_token_type(TokenType.OR):
            node = BooleanOpNode(node, "or", self.or_expr(scope))
        
        return node
    
    
    def and_expr(self, scope) -> Node:
        node = self.not_boolean_expr(scope)
        
        while self.match_token_type(TokenType.AND):
            node = BooleanOpNode(node, "and", self.and_expr(scope))
            
        return node
    
    
    def not_boolean_expr(self, scope) -> Node:
        if self.match_token_type(TokenType.NOT):
            node = NotBooleanNode(self.not_boolean_expr(scope))
        else:
            node = self.equality_expr(scope)
            
        return node


    def equality_expr(self, scope) -> Node:
        node = self.comp_expr(scope)
        
        while self.match_token_type(TokenType.EQUAL, TokenType.DIFERENT):
            node = ComparisonOpNode(node, self.peek_token(-1).value, self.equality_expr(scope))
            
        return node


    def comp_expr(self, scope) -> Node:
        node = self.add_expr(scope)
        
        while self.match_token_type(TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL):
            node = ComparisonOpNode(node, self.peek_token(-1).value, self.comp_expr(scope))
        
        return node    
        
            
    def add_expr(self, scope) -> Node:
        node = self.mult_expr(scope)
        
        while self.match_token_type(TokenType.PLUS, TokenType.MINUS):
            node = BinaryOpNode(node, self.peek_token(-1).value, self.mult_expr(scope))
            
        return node
    
    
    def mult_expr(self, scope) -> Node:
        node = self.unary_expr(scope)
        
        while self.match_token_type(TokenType.STAR, TokenType.SLASH, TokenType.MOD):
            node = BinaryOpNode(node, self.peek_token(-1).value, self.mult_expr(scope))
            
        return node
    
    
    def unary_expr(self, scope) -> Node:
        if self.match_token_type(TokenType.PLUS, TokenType.MINUS):
            node = UnaryNode(self.peek_token(-1), self.unary_expr(scope))
        else:
            node = self.power_expr(scope)
            
        return node
    
    
    def power_expr(self, scope) -> Node:
        node = self.primitive(scope)
        
        while self.match_token_type(TokenType.DOUBLE_STAR):
            node = BinaryOpNode(node, "**", self.power_expr(scope))
            
        return node
    
    
    def primitive(self, scope) -> Node:
        none_aux = NoneNode(self.line(), self.column())
        
        # Is a NUMBER?
        if self.match_token_type(TokenType.NUMBER):
            current_token = self.peek_token(-1)
            
            if isinstance(current_token.value, float):
                node = FloatNode(current_token.value, current_token.line, current_token.column)
            else:
                node = IntNode(current_token.value, current_token.line, current_token.column)
            
            return node

        # is a STRING_LITERAL
        if self.match_token_type(TokenType.STRING_LITERAL):
            current_token = self.peek_token(-1)
            node = StringNode(current_token.value, current_token.line, current_token.column)
            return node
                        
       # is a bool
        if self.match_token_type(TokenType.TRUE):
            return BoolNode(True, self.line(), self.column())
        
        if self.match_token_type(TokenType.FALSE):
            return BoolNode(False, self.line(), self.column())
        
        #is a None value
        if self.match_token_type(TokenType.NONE):
            return none_aux
        
        # Is a LPAREN?
        if self.match_token_type(TokenType.LPAREN):
            node = self.expression(scope)
            if not self.eat(TokenType.RPAREN, "Priority exploitation attempt failed, parenthesis lock ')' not found"):
                return none_aux
            return node
        
        #Is a identifier?
        elif self.match_token_type(TokenType.IDENT):
            if self.match_token_type(TokenType.LPAREN):
                return self.parse_call_function(scope)
            else:
                variable_token = self.peek_token(-1)
                if scope.lookup_var(variable_token.value):
                    node = VariableNode(variable_token.value, variable_token.line, variable_token.column)
                    return node
                else:
                    self.declare_error(f"Attempt to use variable failed, variable '{variable_token.value}' was not found")
                    return none_aux
                
        self.declare_error("Unexpected primitive")
        return none_aux
            
