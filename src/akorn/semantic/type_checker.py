from akorn.ast import *
from akorn.diagnostic import ErrorReporter

class TypeChecker:
    def __init__(
        self,
        program_ast: ProgramNode,
        reporter: ErrorReporter
        ) -> None:
        
        self.program_ast = program_ast
        self.reporter = reporter
    
    def stop(self) -> None:
        raise Exception
    
    def check_types(self) -> None:
        statements = self.program_ast.statements
        for statement in statements:
            if isinstance(statement, DeclarationNode):
                self.check_declaration(statement)
            elif isinstance(statement, AssignmentNode):
                self.check_assignment(statement)
                
    def check_declaration(self, statement: DeclarationNode) -> None:
        self.check_value(statement.value, statement.type)
            
    def check_binary_op(self, statement: BinaryOpNode) -> None:
        self.check_value(statement.left)
        self.check_value(statement.right)
    
    def check_unary_op(self, statement: UnaryNode) -> None:
        pass
    
    def check_variable(self, statement: VariableNode) -> None:
        pass
    
    def check_literals(self, statement: LiteralNode) -> None:
        pass
    
    def check_value(self, statement: Node, type) -> None:
        if isinstance(statement.value, BinaryOpNode):
            self.check_binary_op(statement.value, statement.type)
        elif isinstance(statement.value, UnaryNode):
            self.check_unary_op(statement.value, statement.type)
        elif isinstance(statement.value, VariableNode):
            self.check_variable(statement.value, statement.type)
        elif isinstance(statement.value, LiteralNode):
            self.check_literals(statement.value, statement.type)

"""def check_assignment(self, statement: AssignmentNode) -> None:
if statement"""