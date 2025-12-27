from akon.ast.nodes import *
from akon.diagnostic.akon_errors import ErrorReporter, ZeroDivisionErrorAkon, RuntimeErrorAkon
from akon.enviroment.enviroment import Enviroment

class Interpreter:
    def __init__(self, root_node: ProgramNode, reporter: ErrorReporter):
        self.root_node = root_node
        self.reporter = reporter
    
    def stop(self):
        raise Exception
        
    def interpret_statements(self, node):
        statements = node.statements
        scope = node.scope
        for statement in statements:
            if isinstance(statement, DeclarationNode) or isinstance(statement, AssignmentNode):
                var_value = self.visit_declar_assign(statement, scope)
                statement.value = var_value
                self.update_scope_var(
                    statement.name,
                    var_value,
                    scope,
                )
            elif isinstance(statement, CallNode):
                self.visit_call_node(statement, scope)
            elif isinstance(statement, IfNode):
                self.visit_if_node(statement)
           
    def update_scope_var(self, var_name, var_value, scope: Enviroment):        
        scope.assignment_var(var_name, var_value, True)
   
    def visit_literal(self, literal_node: LiteralNode):
        return literal_node.value
           
    def visit_unary(self, unary_node: UnaryNode, scope: Enviroment):
        sign_unary = unary_node.operator
        value = self.visit_node(unary_node.node, scope)
            
        if sign_unary == '-':
            return -value
        elif sign_unary == '+':
            return +value
    
    def visit_comparison_operation(self, comparison_op_node: ComparisonOpNode, scope: Enviroment):
        left = self.visit_node(comparison_op_node.left, scope)
        operator = comparison_op_node.operator
        right = self.visit_node(comparison_op_node.right, scope)
        
        if operator == '<':
            return left < right
        elif operator == '>':
            return left > right
        elif operator == '<=':
            return left <= right
        elif operator == '>=':
            return left >= right
        elif operator == '==':
            return left == right
        elif operator == '!=':
            return left != right
               
    def visit_boolean_operation(self, boolean_op_node: BooleanOpNode, scope: Enviroment):
        left = self.visit_node(boolean_op_node.left, scope)
        operator = boolean_op_node.operator
        
        # short-circuit
        if operator == "and" and left == False:
            return False
        elif operator == "or" and left == True:
            return True 
        
        right = self.visit_node(boolean_op_node.right, scope)
        
        if operator == "and":
            return left and right
        if operator == "or":
            return left or right

    def visit_not_boolean_operator(self, not_boolean_operator: NotBooleanNode, scope: Enviroment):
        line_operation = not_boolean_operator.line
        column_operation = not_boolean_operator.column
        value_bool = self.visit_node(not_boolean_operator.node, scope)
        
        if isinstance(value_bool, bool):
            return not value_bool
        else:
            self.reporter.add_error(
                RuntimeErrorAkon(
                    "You cannot operate on a non-Bool value with the boolean operator not",
                    line_operation,
                    column_operation,
                )
            )
            self.stop()

    def visit_binary_operation(self, binary_op_node: BinaryOpNode, scope: Enviroment):
        line_operation = binary_op_node.left.line
        column_operation = binary_op_node.left.column
        left = self.visit_node(binary_op_node.left, scope)
        operator = binary_op_node.operator
        right = self.visit_node(binary_op_node.right, scope)
        
        if operator == '+':
            return left + right
        
        elif operator == '-':
            return left - right
        
        elif operator == '*':
            return left * right
        
        elif operator == '/':
            if right == 0:
                self.reporter.add_error(
                    ZeroDivisionErrorAkon(
                        "You cannot divide a number by zero",
                        line_operation,
                        column_operation
                    )
                )
                self.stop()
            else:
                return left / right
            
        elif operator == '%':
            if right == 0:
                self.reporter.add_error(
                    ZeroDivisionErrorAkon(
                        "You cannot find the modulus of a number divided by zero",
                        line_operation,
                        column_operation,
                    )
                )
                self.stop()
            else:
                return left % right
            
        elif operator == "**":
            return left ** right

    def visit_variable(self, var_node: VariableNode, scope: Enviroment):
        pack = scope.get_var(var_node.name)
        
        if pack["interpreted"]:
            return pack["value"]
        else:
            return self.visit_node(pack["value"])
    
    def visit_declar_assign(self, decl_assign_node: DeclarationNode | AssignmentNode, scope: Enviroment):
        return self.visit_node(decl_assign_node.value, scope)

    def visit_elif_node(self, elif_node: ElIfNode):
        bool_conditional = self.visit_node(elif_node.condition, elif_node.scope)
        
        if bool_conditional:
            self.interpret_statements(elif_node)
        elif isinstance(elif_node.elif_node, ElIfNode):
            self.visit_elif_node(elif_node.elif_node)
        elif isinstance(elif_node.else_node, ElseNode):
            self.interpret_statements(elif_node.else_node)
    
    def visit_if_node(self, if_node: IfNode):
        bool_conditional = self.visit_node(if_node.condition, if_node.scope)
        
        if bool_conditional:
            self.interpret_statements(if_node)
        elif isinstance(if_node.elif_node, ElIfNode):
            self.visit_elif_node(if_node.elif_node)
        else:
            self.interpret_statements(if_node.else_node)

    # Builtin Functions temporals
    def builtin_write(args) -> None:
        values = []
        for arg in args:
            values.append(arg)
        
        print(*values)
        return None
    
    def builtin_read_int(args) -> int:
        values = []
        for arg in args:
            values.append(arg)
            
        input_int = input(*values)
        
        while True:
            try:
                input_int = int(input_int)
                break
            except ValueError:
                input_int = input(*values)
         
        return input_int
    
    def builtin_read_float(args) -> float:
        values = []
        for arg in args:
            values.append(arg)
            
        input_float = input(*values)
        
        while True:
            try:
                input_float = float(input_float)
                break
            except ValueError:
                input_float = input(*values)
         
        return input_float
        
    def builtin_read_string(args) -> str:
        values = []
        for arg in args:
            values.append(arg)
            
        input_string = input(*values)
        return input_string
    
    def builtin_read_bool(args) -> bool:
        values = []
        for arg in args:
            values.append(arg)
            
        input_string = input(values[0])
        
        while True:
            if input_string == values[1]:
                return True
            elif input_string == values[2]:
                return False
            else:
                input_string = input(values[0])
            
            
            
    BUILTINS = {
        "write":builtin_write,
        "readInt":builtin_read_int,
        "readFloat":builtin_read_float,
        "readString":builtin_read_string,
        "readBool":builtin_read_bool,
    }

    def visit_call_node(self, call_node: CallNode, scope: Enviroment):
        args = []
            
        for arg in call_node.args:
            value_arg = self.visit_node(arg, scope)
            args.append(value_arg)
                
        return self.BUILTINS[call_node.calle](args)

    def visit_node(self, node: Node, scope: Enviroment):
        if isinstance(node, CallNode):
            return self.visit_call_node(node, scope)
        
        if isinstance(node, VariableNode):
            return self.visit_variable(node, scope)
        
        elif isinstance(node, BinaryOpNode):
            return self.visit_binary_operation(node, scope)
        
        elif isinstance(node, UnaryNode):
            return self.visit_unary(node, scope)
        
        elif isinstance(node, NotBooleanNode):
            return self.visit_not_boolean_operator(node, scope)
        
        elif isinstance(node, ComparisonOpNode):
            return self.visit_comparison_operation(node, scope)
        
        elif isinstance(node, BooleanOpNode):
            return self.visit_boolean_operation(node, scope)
        
        elif isinstance(node, IntNode):
            return self.visit_literal(node)
        
        elif isinstance(node, FloatNode):
            return self.visit_literal(node)
        
        elif isinstance(node, BoolNode):
            return self.visit_literal(node)
        
        elif isinstance(node, StringNode):
            return self.visit_literal(node)
        