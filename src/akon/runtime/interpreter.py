from akon.ast.nodes import *
from akon.diagnostic.akon_errors import ErrorReporter, ZeroDivisionErrorAkon, RuntimeErrorAkon
from akon.enviroment.enviroment import Enviroment

class Interpreter:
    def __init__(self, ast: ProgramNode, reporter: ErrorReporter, env: Enviroment):
        self.ast = ast
        self.reporter = reporter
        self.env = env
    
    def builtin_print(args) -> None:
        values = [str(arg) for arg in args]
        print(*values)
        return None
    
    BUILTINS = {
        "print":builtin_print,
    }
    
    def visit_call_node(self, call_node: CallNode):
        for call_node.calle in self.BUILTINS:
            args = [self.visit_node(arg) for arg in call_node.args]
            return self.BUILTINS[call_node.calle](args)
    
    def stop(self):
        raise Exception
        
    def interpret(self):
        statements = self.ast.statements
        for statement in statements:
            if isinstance(statement, DeclarationNode) or isinstance(statement, AssignmentNode):
                var_value = self.visit_declar_assign(statement)
                statement.value = var_value
                self.update_scope_var(
                    statement.name,
                    var_value,
                )
            elif isinstance(statement, CallNode):
                self.visit_call_node(statement)

    def update_scope_var(self, var_name, var_value):
        self.env.scope["variables"][var_name]["var_value"] = var_value
        self.env.scope["variables"][var_name]["interpreted"] = True
   
    def visit_literal(self, literal_node: LiteralNode):
        return literal_node.value
           
    def visit_unary(self, unary_node: UnaryNode):
        sign_unary = unary_node.operator
        value = self.visit_node(unary_node.node)
            
        if sign_unary == '-':
            return -value
        elif sign_unary == '+':
            return +value
    
    def visit_comparison_operation(self, comparison_op_node: ComparisonOpNode):
        left = self.visit_node(comparison_op_node.left)
        operator = comparison_op_node.operator
        right = self.visit_node(comparison_op_node.right)
        
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
               
    def visit_boolean_operation(self, boolean_op_node: BooleanOpNode):
        left = self.visit_node(boolean_op_node.left)
        operator = boolean_op_node.operator
        right = self.visit_node(boolean_op_node.right)
        
        if operator == "and":
            return left and right
        if operator == "or":
            return left or right

    def visit_not_boolean_operator(self, not_boolean_operator: NotBooleanNode):
        line_operation = not_boolean_operator.line
        column_operation = not_boolean_operator.column
        value_bool = self.visit_node(not_boolean_operator.node)
        
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

    def visit_binary_operation(self, binary_op_node: BinaryOpNode):
        line_operation = binary_op_node.left.line
        column_operation = binary_op_node.left.column
        left = self.visit_node(binary_op_node.left)
        operator = binary_op_node.operator
        right = self.visit_node(binary_op_node.right)
        
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

    def visit_variable(self, var_node: VariableNode):
        var_value = self.env.scope[var_node.name]["var_value"]
        
        if self.env.scope["variables"][var_node.name]["interpreted"]:
            return var_value
        else:
            return self.visit_node(var_value)
    
    def visit_declar_assign(self, decl_assign_node: DeclarationNode | AssignmentNode):
        return self.visit_node(decl_assign_node.value)

    def visit_node(self, node: Node):
        if isinstance(node, VariableNode):
            return self.visit_variable(node)
        
        elif isinstance(node, BinaryOpNode):
            return self.visit_binary_operation(node)
        
        elif isinstance(node, UnaryNode):
            return self.visit_unary(node)
        
        elif isinstance(node, NotBooleanNode):
            return self.visit_not_boolean_operator(node)
        
        elif isinstance(node, ComparisonOpNode):
            return self.visit_comparison_operation(node)
        
        elif isinstance(node, BooleanOpNode):
            return self.visit_boolean_operation(node)
        
        elif isinstance(node, IntNode):
            return self.visit_literal(node)
        
        elif isinstance(node, FloatNode):
            return self.visit_literal(node)
        
        elif isinstance(node, BoolNode):
            return self.visit_literal(node)
        
        elif isinstance(node, StringNode):
            return self.visit_literal(node)
        