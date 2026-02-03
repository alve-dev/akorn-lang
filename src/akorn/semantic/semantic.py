from akorn.ast import *
from akorn.diagnostic import ErrorReporter
from akorn.enviroment import Enviroment
from dataclasses import dataclass

@dataclass(slots=True)
class Symbol:
    type_name: str
    is_mutable: bool
    is_none: bool
    
    
class Semantic:
    def __init__(self, reporter: ErrorReporter) -> None:
        self.reporter = reporter
        
           
    def check_ast(self, ast: Node):
        scope = ast.scope
        for node in ast.statements:
            if isinstance(node, DeclarationNode):
                self.check_declaration(node, scope)
            elif isinstance(node, IfNode):
                for branch in node.branches:
                    self.check_condition(branch[0], scope)
                    self.check_ast(branch[1])
    
    def check_condition(self, condition: Node, scope: Enviroment):
        # una condicion puede ser:
        # bool node if true
        # variable node if is_none
        # not boolean op if not false
        # boolean op if true or false
        # comparison op if 5 < 4
             
        if isinstance(condition, BoolNode):
            pass
        
        elif isinstance(condition, NotBooleanNode):
            self.check_not_boolean_op(condition, scope)
            
        elif isinstance(condition, BooleanOpNode):
            self.check_boolean_op(condition, scope)
            
        elif isinstance(condition, ComparisonOpNode):
            self.check_comparison_op(condition, scope)
            
        elif isinstance(condition, VariableNode):
            var_type = self.check_variable(condition, scope)
            
            if var_type == "non-existent":
                self.declare_error(
                    f"Error in condition, use of non-existent variable, an attempt was made to use a variable called '{condition.name}', give it a value or use a valid expression for the condition, remember that conditions must always have an expression that returns a bool",
                    condition.line,
                    condition.column
                )
            
            elif var_type == "none":
                self.declare_error(
                    f"Error in condition, use of variable exists but is empty. An attempt was made to use a variable called '{condition.name}' which is none. Please assign a value or use a valid expression for the condition. Remember that conditions must always have an expression that returns a boolean.",
                    condition.line,
                    condition.column
                )
            
            elif var_type == "bool":
                pass
            
            else:
                self.declare_error(
                    f"Error in condition, use of variable exists but with a non-boolean value. An attempt was made to use a variable called '{condition.name}' which is a '{var_type}'. Please use a valid expression for the condition. Remember that conditions must always have an expression that returns a boolean.",
                    condition.line,
                    condition.column
                )
        
        else:
            self.declare_error(
                f"Error in condition, in the condition you used an invalid expression, try to use a valid condition that returns a boolean.",
                condition.line,
                condition.column
            )
        
        
    def declare_error(self, msg: str, line: int, col: int) -> None:
        self.reporter.add_error(
            f"[SemanticError][line: {line}, col: {col}] {msg}"
        )
    
    
    def check_declaration(self, decl_node: DeclarationNode, scope: Enviroment):
        success = False
        is_none = False
        
        if decl_node.type == "int":
            if isinstance(decl_node.value, UnaryNode):
                success = self.check_unary_node(decl_node.value, scope, "int")
                
            elif isinstance(decl_node.value, IntNode):
                success = True
            
            elif isinstance(decl_node.value, NoneNode):
                success = True
                is_none = True
            
            elif isinstance(decl_node.value, VariableNode):
                var_type = self.check_variable(decl_node.value, scope)
                
                if var_type == "non-existent":
                    self.declare_error(
                        f"Variable called '{decl_node.value.name}' does not exist, try using an existing variable or a valid expression of type 'int'.",
                        decl_node.value.line,
                        decl_node.value.column
                    )
                    
                elif var_type != "int":
                    self.declare_error(
                        f"A value 'float' was expected, but a value '{decl_node.value.label}' was found for the variable '{decl_node.value.name}', try using an existing variable or a valid epression of type 'int'.",
                        decl_node.value.line,
                        decl_node.value.column
                    )
                
                elif var_type == "none":
                    self.declare_error(
                        f"The variable '{decl_node.value.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value, or another valid expression.",
                        decl_node.value.line,
                        decl_node.value.column
                    )
                    
                else:
                    success = True
                    
            elif isinstance(decl_node.value, BinaryOpNode):
                success = self.check_binary_op(decl_node.value, scope, "int")

            else:
                self.declare_error(
                    f"An expression of type 'int' was expected, but a '{decl_node.value.label}' was found",
                    decl_node.value.line,
                    decl_node.value.column
                )
        
        elif decl_node.type == "float":
            if isinstance(decl_node.value, UnaryNode):
                success = self.check_unary_node(decl_node.value, scope, "float")
                
            elif isinstance(decl_node.value, FloatNode):
                success = True
                
            elif isinstance(decl_node.value, NoneNode):
                success = True
                is_none = True
            
            elif isinstance(decl_node.value, VariableNode):
                var_type = self.check_variable(decl_node.value, scope)
                
                if var_type == "non-existent":
                    self.declare_error(
                        f"Variable called '{decl_node.value.name}' does not exist, try using an existing variable or a valid expression of type 'float'.",
                        decl_node.value.line,
                        decl_node.value.column
                    )
                    
                elif var_type != "float":
                    self.declare_error(
                        f"A value 'float' was expected but a value '{decl_node.value.label}' was found for the variable '{decl_node.value.name}', try using an existing variable or value of type 'float'.",
                        decl_node.value.line,
                        decl_node.value.column
                    )
                    
                elif var_type == "none":
                    self.declare_error(
                        f"The variable '{decl_node.value.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value, or another valid expression.",
                        decl_node.value.line,
                        decl_node.value.column
                    )
                    
                else:
                    success = True
                    
            elif isinstance(decl_node.value, BinaryOpNode):
                success = self.check_binary_op(decl_node.value, scope, "float")

            else:
                self.declare_error(
                    f"An expression of type 'float' was expected, but a '{decl_node.value.label}' was found",
                    decl_node.value.line,
                    decl_node.value.column
                )
        
        elif decl_node.type == "bool":
            if isinstance(decl_node.value, BoolNode):
                success = True
                
            elif isinstance(decl_node.value, NoneNode):
                success = True
                is_none = True
                
            elif isinstance(decl_node.value, VariableNode):
                var_type = self.check_variable(decl_node.value, scope)
                
                if var_type == "non-existent":
                    self.declare_error(
                        f"Variable called '{decl_node.value.name}' does not exist, try using an existing variable or a valid expression of type 'boolean value'.",
                        decl_node.value.line,
                        decl_node.value.column
                    )
                    
                elif var_type != "bool":
                    self.declare_error(
                        f"A value 'boolean value' was expected, but a value '{decl_node.value.label}' was found for the variable '{decl_node.value.name}', try using a variable or value of type 'boolean value'.",
                        decl_node.value.line,
                        decl_node.value.column
                    )
                    
                elif var_type == "none":
                    self.declare_error(
                        f"The variable '{decl_node.value.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value, or another valid expression.",
                        decl_node.value.line,
                        decl_node.value.column
                    )
                    
                else:
                    success = True
                    
            elif isinstance(decl_node.value, BooleanOpNode):
                success = self.check_boolean_op(decl_node.value, scope)
                
            elif isinstance(decl_node.value, ComparisonOpNode):
                success = self.check_comparison_op(decl_node.value, scope)
                
            elif isinstance(decl_node.value, NotBooleanNode):
                success = self.check_not_boolean_op(decl_node.value, scope)
                
            else:
                self.declare_error(
                    f"An expression of type 'bool' was expected, but a '{decl_node.value.label}' was found",
                    decl_node.value.line,
                    decl_node.value.column
                )
                 
        if success:
                symbol = Symbol(decl_node.type, decl_node.mutable, is_none)
                scope.add_var(symbol, decl_node.name)
                
        
    def check_unary_node(self, unary_node: UnaryNode, scope: Enviroment, type_expected: str = "undefined", return_type: bool = False):
        """Un UnaryNode puede tener un IntNode,
        FloatNode, UnaryNode o un BinaryOpNode como value"""
        
        success = False
        if isinstance(unary_node.node, IntNode):
            if type_expected == "int":
                success = True
            
            elif type_expected == "undefined":
                success = True
                type_expected = "int"
            
            self.declare_error(
                f"A value '{type_expected}' was expected, but a value 'float' was found, try using a variable or a expresion of type 'float'.",
                unary_node.node.line,
                unary_node.node.column
            )
        
        if isinstance(unary_node.node, FloatNode):
            if type_expected == "float":
                success = True
            
            elif type_expected == "undefined":
                success = True
                type_expected = "float"
            
            self.declare_error(
                f"A value '{type_expected}' was expected, but a value 'int' was found, try using a variable or a expresion of type 'int'.",
                unary_node.node.line,
                unary_node.node.column
            )
        
        elif isinstance(unary_node.node, NoneNode):
            self.declare_error(
                f"Empty expression error, a 'none' value was used in the unary operation '{unary_node.operator}', please use a valid expression, remember that 'none' values ​​are unusable",
                unary_node.node.line,
                unary_node.node.column
            )
        
        elif isinstance(unary_node.node, UnaryNode):
            if type_expected == "undefined":
                type_expected, success = self.check_unary_node(unary_node.node, scope, return_type=True)

            else:
                success = self.check_unary_node(unary_node.node, scope, type_expected)
        
        elif isinstance(unary_node.node, BinaryOpNode):
            if type_expected == "undefined":
                type_expected, success = self.check_binary_op(unary_node.node, scope, return_type=True)
            
            else:
                success = self.check_binary_op(unary_node.node, scope, type_expected)
        
        elif isinstance(unary_node.node, VariableNode):
            var_type = self.check_variable(unary_node.node, scope)
            
            if var_type == "non-existent":
                self.declare_error(
                    f"Variable called '{unary_node.name}' does not exist, try using an existing variable or a valid expression of type '{type_expected}'.",
                    unary_node.node.line,
                    unary_node.node.column
                )
                
            elif var_type == "none":
                self.declare_error(
                    f"The variable '{unary_node.node.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value,\nor another valid expression.",
                    unary_node.node.line,
                    unary_node.node.column
                )
            
            elif var_type != type_expected:
                self.declare_error(
                    f"An {type_expected} value was expected, but {unary_node.value.label} was  for the variable {unary_node.node.name}.\nRemember that for unary '-' or '+' only valid numbers are allowed, Try using a valid expression like '{type_expected}'",
                    unary_node.node.line,
                    unary_node.node.column
                )
            
            elif type_expected == "undefined" and (var_type != "int" or var_type != "float"):
                self.declare_error(
                    f"You tried to convert an invalid value to negative in this operation; try using an int or float.",
                    unary_node.node.line,
                    unary_node.node.column
                )
            
            else:
                success = True
                
                if type_expected == "undefined":
                    type_expected = var_type
                
        else:
            self.declare_error(
                f"An {type_expected} value was expected, but {unary_node.node.label} was found, remember that for unary '-' or '+' only valid numbers are allowed.",
                unary_node.line,
                unary_node.column
            )
        
        if return_type:
            return type_expected, success
        
        return success
    
    
    def check_variable(self, var_node: VariableNode, scope: Enviroment):
        if scope.exists(var_node.name):
            symbol = scope.get(var_node.name)
            
            if symbol.is_none:
                return "none"
            
            return symbol.type_name
            
        return "non-existent"
    
    
    def check_binary_op(self, binary_op: BinaryOpNode , scope: Enviroment, type_expected: str = "undefined", return_type: bool = False):
        """Un BinaryOpNode puede tener IntNodes, FloatNodes, UnaryNodes,
        otro BinaryOpNode"""
        
        # Parte Left
        left_success = False
        
        if isinstance(binary_op.left, IntNode):
            if type_expected == "int":
                left_success = True
                
            elif type_expected == "undefined":
                type_expected = "int"
                left_success = True
                
            else:
                self.declare_error(
                    f"A value '{type_expected}' was expected in the operation '{binary_op.operator}', but a value 'int' was found, try using a variable or a expresion of type '{type_expected}'.",
                    binary_op.left.line,
                    binary_op.left.column
                )
        
        elif isinstance(binary_op.left, FloatNode):
            if type_expected == "float":
                left_success = True
                
            elif type_expected == "undefined":
                type_expected = "float"
                left_success = True
            
            else:
                self.declare_error(
                    f"A value '{type_expected}' was expected in the operation '{binary_op.operator}', but a value 'float' was found, try using a variable or a expresion of type '{type_expected}'",
                    binary_op.left.line,
                    binary_op.left.column
                )
        
        elif isinstance(binary_op.left, UnaryNode):
            if type_expected == "undefined":
                type_expected, left_success = self.check_unary_node(binary_op.left, scope, return_type=True)
                
            else:
                left_success = self.check_unary_node(binary_op.left, scope, type_expected)
        
        elif isinstance(binary_op.left, NoneNode):
            self.declare_error(
                f"Empty expression error, a 'none' value was used in the arithmetic operation '{binary_op.operator}', please use a valid expression, remember that 'none' values ​​are unusable",
                binary_op.left.line,
                binary_op.left.column
            )
        
        elif isinstance(binary_op.left, VariableNode):
            var_type = self.check_variable(binary_op.left, scope)
            
            if var_type == "non-existent":
                self.declare_error(
                    f"Variable called '{binary_op.left.name}' does not exist, try using an existing variable or a valid expression of type '{type_expected}'.",
                    binary_op.left.line,
                    binary_op.left.column
                )
                
            elif var_type == "none":
                self.declare_error(
                    f"The variable '{binary_op.left.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value,\nor another valid expression.",
                    binary_op.left.line,
                    binary_op.left.column
                )
                
            elif var_type != type_expected:
                self.declare_error(
                    f"A value '{type_expected}' was expected, but a value '{binary_op.value.label}' was found for the variable '{binary_op.value.name}',\ntry using a variable or value of type '{type_expected}'.",
                    binary_op.left.line,
                    binary_op.left.column
                )
                
            elif type_expected == "undefined" and (var_type != "int" or var_type != "float"):
                self.declare_error(
                    f"You're trying to perform an arithmetic operation with invalid values; try using only int or float.",
                    binary_op.left.line,
                    binary_op.left.column
                )
                
            else:
                left_success = True
                
                if type_expected == "undefined":
                    type_expected = var_type
                
        elif isinstance(binary_op.left, BinaryOpNode):
            if type_expected == "undefined":
                type_expected, left_success = self.check_binary_op(binary_op.left, scope, return_type=True) 
            
            else:
                left_success = self.check_binary_op(binary_op.left, scope, type_expected)
            
        else:
            self.declare_error(
                f"A value '{type_expected}' was expected in the operation '{binary_op.operator}', but a value '{binary_op.left.label}' was found, try using a variable or a expresion of type '{type_expected}'.",
                binary_op.left.line,
                binary_op.left.column
            )
        
        # Parte Right
        right_success = False
        if isinstance(binary_op.right, IntNode):
            if type_expected == "int":
                right_success = True
                
            elif type_expected == "undefined":
                type_expected = "int"
                right_success = True
                
            else:
                self.declare_error(
                    f"A value '{type_expected}' was expected in the operation '{binary_op.operator}', but a value 'int' was found, try using a variable or a expresion of type '{type_expected}'.",
                    binary_op.right.line,
                    binary_op.right.column
                )
        
        elif isinstance(binary_op.right, FloatNode):
            if type_expected == "float":
                right_success = True
                
            elif type_expected == "undefined":
                type_expected = "float"
                right_success = True
                
            else:
                self.declare_error(
                    f"A value '{type_expected}' was expected in the operation '{binary_op.operator}', but a value 'float' was found, try using a variable or a expresion of type '{type_expected}'",
                    binary_op.right.line,
                    binary_op.right.column
                )
        
        elif isinstance(binary_op.right, NoneNode):
            self.declare_error(
                f"Empty expression error, a 'none' value was used in the arithmetic operation '{binary_op.operator}', please use a valid expression, remember that 'none' values ​​are unusable",
                binary_op.right.line,
                binary_op.right.column
            )
        
        elif isinstance(binary_op.right, UnaryNode):
            if type_expected == "undefined":
                type_expected, right_success = self.check_unary_node(binary_op.right, scope, return_type=True)
            
            else:
                right_success = self.check_unary_node(binary_op.right, scope, type_expected)
        
        elif isinstance(binary_op.right, VariableNode):
            var_type = self.check_variable(binary_op.right, scope)
        
            if var_type == "non-existent":
                self.declare_error(
                    f"Variable called '{binary_op.right.name}' does not exist, try using an existing variable or a valid expression of type '{type_expected}'.",
                    binary_op.right.line,
                    binary_op.right.column
                )
            
            if var_type == "none":
                self.declare_error(
                    f"The variable '{binary_op.right.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value,\nor another valid expression.",
                    binary_op.right.line,
                    binary_op.right.column
                )
            
            elif var_type != type_expected:
                self.declare_error(
                    f"A value '{type_expected}' was expected, but a value '{binary_op.value.label}' was found for the variable '{binary_op.value.name}',\ntry using a variable or value of type '{type_expected}'.",
                    binary_op.left.line,
                    binary_op.left.column
                )
            
            elif type_expected == "undefined" and (var_type != "int" or var_type != "float"):
                self.declare_error(
                    f"You're trying to perform an arithmetic operation with invalid values; try using only int or float.",
                    binary_op.right.line,
                    binary_op.right.column
                )
                
            else:
                right_success = True
                
                if type_expected == "undefined":
                    type_expected = var_type
                
        elif isinstance(binary_op.right, BinaryOpNode):
            if type_expected == "undefined":
                type_expected, right_success = self.check_binary_op(binary_op.right, scope, return_type=True)
            
            else:
                right_success = self.check_binary_op(binary_op.left, scope, type_expected)
            
        else:
            self.declare_error(
                    f"A value '{type_expected}' was expected in the arithmetic operation, but a value '{binary_op.right.label}' was found, try using a variable or a expresion of type '{type_expected}'.",
                    binary_op.right.line,
                    binary_op.right.column
            )
        
        if return_type:
            return type_expected, left_success and right_success

        return left_success and right_success


    def check_boolean_op(self, boolean_op: BooleanOpNode, scope: Enviroment):
        
        #Part left
        left_success = False
        
        if isinstance(boolean_op.left, BoolNode):
            left_success = True
        
        elif isinstance(boolean_op.left, NoneNode):
            self.declare_error(
                f"Empty expression error, a 'none' value was used in the boolean operation '{boolean_op.operator}', please use a valid expression, remember that 'none' values ​​are unusable",
                boolean_op.left.line,
                boolean_op.left.column
            )
        
        elif isinstance(boolean_op.left, BooleanOpNode):
            left_success = self.check_boolean_op(boolean_op.left, scope)
        
        elif isinstance(boolean_op.left, ComparisonOpNode):
            left_success = self.check_comparison_op(boolean_op.left, scope)
            
        elif isinstance(boolean_op.left, NotBooleanNode):
            left_success = self.check_not_boolean_op(boolean_op.left, scope)
            
        elif isinstance(boolean_op.left, VariableNode):
            var_type = self.check_variable(boolean_op.left, scope)
            
            if var_type == "non-existent":
                self.declare_error(
                    f"Variable called '{boolean_op.left.name}' does not exist, try using a valid expression of type 'bool'.",
                    boolean_op.left.line,
                    boolean_op.left.column
                )
                
            elif var_type == "none":
                self.declare_error(
                    f"The variable '{boolean_op.left.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value,\nor another valid expression.",
                    boolean_op.left.line,
                    boolean_op.left.column
                )
            
            elif var_type != "bool":
                self.declare_error(
                    f"A value 'bool' was expected in the operation {boolean_op.operator}, but a value '{boolean_op.left.label}' was found, try using a variable or value of type 'bool'.",
                    boolean_op.left.line,
                    boolean_op.left.column
                )
            
            else:
                left_success = True
        
        else:
            self.declare_error(
                f"A value 'bool' was expected, but a value '{boolean_op.left.label}' was found, try using a variable or a expresion of type 'bool'.",
                boolean_op.left.line,
                boolean_op.left.column
            )
            
       #Part right
        right_success = False
        
        if isinstance(boolean_op.right, BoolNode):
            right_success = True
        
        elif isinstance(boolean_op.right, NoneNode):
            self.declare_error(
                f"Empty expression error, a 'none' value was used in the boolean operation '{boolean_op.operator}', please use a valid expression, remember that 'none' values ​​are unusable",
                boolean_op.right.line,
                boolean_op.right.column
            )
        
        elif isinstance(boolean_op.right, BooleanOpNode):
            right_success = self.check_boolean_op(boolean_op.right, scope)
        
        elif isinstance(boolean_op.right, ComparisonOpNode):
            right_success = self.check_comparison_op(boolean_op.right, scope)
            
        elif isinstance(boolean_op.right, NotBooleanNode):
            right_success = self.check_not_boolean_op(boolean_op.right, scope)
            
        elif isinstance(boolean_op.right, VariableNode):
            var_type = self.check_variable(boolean_op.right, scope)
            
            if var_type == "non-existent":
                self.declare_error(
                    f"Variable called '{boolean_op.right.name}' does not exist, try using a valid expression of type 'bool'.",
                    boolean_op.right.line,
                    boolean_op.right.column
                )
                
            elif var_type == "none":
                self.declare_error(
                    f"The variable '{boolean_op.right.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value,\nor another valid expression.",
                    boolean_op.right.line,
                    boolean_op.right.column
                )
            
            elif var_type != "bool":
                self.declare_error(
                    f"A value 'bool' was expected in the operation {boolean_op.operator}, but a value '{boolean_op.right.label}' was found, try using a variable or value of type 'bool'.",
                    boolean_op.right.line,
                    boolean_op.right.column
                )
            
            else:
                right_success = True
        
        else:
            self.declare_error(
                f"A value 'bool' was expected, but a value '{boolean_op.left.label}' was found, try using a variable or a expresion of type 'bool'.",
                boolean_op.right.line,
                boolean_op.right.column
            )
    
        return left_success and right_success
            
                
    def check_not_boolean_op(self, not_boolean_op: NotBooleanNode, scope: Enviroment):
        
        success = False
        
        if isinstance(not_boolean_op.node, BoolNode):
            success = True
        
        elif isinstance(not_boolean_op.node, NoneNode):
            self.declare_error(
                f"Empty expression error, a 'none' value was used in the not boolean operation '{not_boolean_op.operator}', please use a valid expression, remember that 'none' values ​​are unusable",
                not_boolean_op.node.line,
                not_boolean_op.node.column
            )
        
        elif isinstance(not_boolean_op.node, BooleanOpNode):
            success = self.check_boolean_op(not_boolean_op.node, scope)
            
        elif isinstance(not_boolean_op.node, ComparisonOpNode):
            success = self.check_comparison_op(not_boolean_op.node, scope)
            
        elif isinstance(not_boolean_op.node, NotBooleanNode):
            success = self.check_not_boolean_op(not_boolean_op.node, scope)
            
        elif isinstance(not_boolean_op.node, VariableNode):
            var_type = self.check_variable(not_boolean_op.node, scope)
            
            if var_type == "non-existent":
                self.declare_error(
                    f"Variable called '{not_boolean_op.node.name}' does not exist, try using a valid expression.",
                    not_boolean_op.node.line,
                    not_boolean_op.node.column
                )
                
            elif var_type == "none":
                self.declare_error(
                    f"The variable '{not_boolean_op.node.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value,\nor another valid expression.",
                    not_boolean_op.node.line,
                    not_boolean_op.node.column
                )
            
            elif var_type != "bool":
                self.declare_error(
                    f"A value 'bool' was expected in the operation 'not', but a value '{not_boolean_op.node.label}' was found, try using a variable or value of type 'bool'.",
                    not_boolean_op.node.line,
                    not_boolean_op.node.column
                )
            
            else:
                success = True
            
        else:
            self.declare_error(
                f"A value 'bool' was expected, but a value '{not_boolean_op.node.label}' was found, try using a expresion of type 'bool'.",
                not_boolean_op.node.line,
                not_boolean_op.node.column
            )
            
        return success
            
        
    def check_comparison_op(self, comparison_op: ComparisonOpNode, scope: Enviroment):
        
        # Equality
        if comparison_op.operator == "==" or comparison_op.operator == "!=":
            
            # Part left
            left_type: str
            left_success = False
            
            if (isinstance(comparison_op.left, BoolNode) or
                isinstance(comparison_op.left, IntNode) or
                isinstance(comparison_op.left, FloatNode) or
                isinstance(comparison_op.left, StringNode)
                ):
                left_type = comparison_op.left.type
                left_success = True
            
            elif isinstance(comparison_op.left, NoneNode):
                self.declare_error(
                    f"Empty expression error, a 'none' value was used in the equality operation '{comparison_op.operator}', please use a valid expression, remember that 'none' values ​​are unusable",
                    comparison_op.left.line,
                    comparison_op.left.column
                )
            
            elif isinstance(comparison_op.left, ComparisonOpNode):
                left_type = "bool"
                left_success = self.check_comparison_op(comparison_op.left, scope)
            
            elif isinstance(comparison_op.left, NotBooleanNode):
                left_type = "bool"
                left_success = self.check_not_boolean_op(comparison_op.left, scope)
                
            elif isinstance(comparison_op.left, BinaryOpNode):
                left_type, left_success = self.check_binary_op(comparison_op.left, scope, return_type=True)
            
            elif isinstance(comparison_op.left, UnaryNode):
                left_type, left_success = self.check_unary_node(comparison_op.left, scope, return_type=True)
                
            elif isinstance(comparison_op.left, BooleanOpNode):
                left_type = "bool"
                left_success = self.check_boolean_op(comparison_op.left, scope)
            
            elif isinstance(comparison_op.left, VariableNode):
                var_type = self.check_variable(comparison_op.left, scope)
                
                if var_type == "non-existent":
                    self.declare_error(
                        f"Variable called '{comparison_op.left.name}' does not exist, try using a valid expression.",
                        comparison_op.left.line,
                        comparison_op.left.column
                    )
                    
                elif var_type == "none":
                    self.declare_error(
                        f"The variable '{comparison_op.left.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value,\nor another valid expression.",
                        comparison_op.left.line,
                        comparison_op.left.column
                    )
                
                elif not(var_type == "string" or
                      var_type == "bool" or
                      var_type == "int" or
                      var_type == "float"
                    ):
                    self.declare_error(
                        f"A valid value was expected in the equality operation '{comparison_op.operator}', try using valid expressions on both sides of the operation",
                        comparison_op.left.line,
                        comparison_op.left.column
                    )
                
                else:
                    left_type = var_type
                    left_success = True
                    
            else:
                self.declare_error(
                    f"A valid value was expected in the equality operation '{comparison_op.operator}', try using valid expressions on both sides of the operation",
                    comparison_op.left.line,
                    comparison_op.left.column
                )
            
            
            # Part right
            right_success = False
            
            if (isinstance(comparison_op.right, BoolNode) or
                isinstance(comparison_op.right, IntNode) or
                isinstance(comparison_op.right, FloatNode) or
                isinstance(comparison_op.right, StringNode)
                ):

                if left_type != comparison_op.right.type:
                    self.declare_error(
                        f"Equality operation error '{comparison_op.operator}', the type of the expression right does not match the type of the expression left,\ntry using expressions that match in types, these are the types found: (left: '{left_type}', right: '{comparison_op.right.type}')",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                    
                else:
                    right_success = True
            
            elif isinstance(comparison_op.right, NoneNode):
                self.declare_error(
                    f"Empty expression error, a 'none' value was used in the equality operation '{comparison_op.operator}', please use a valid expression, remember that 'none' values ​​are unusable",
                    comparison_op.right.line,
                    comparison_op.right.column
                )
            
            elif isinstance(comparison_op.right, ComparisonOpNode):
                if left_type != "bool":
                    self.declare_error(
                        f"Equality operation error '{comparison_op.operator}', The type of expression 'right' does not match the type of expression 'left',\nremember that equality and comparison operations always return a bool, these are the types found: (left: '{left_type}', right: 'bool')",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                    
                else:
                    right_success = self.check_comparison_op(comparison_op.right, scope)
                
            elif isinstance(comparison_op.right, NotBooleanNode):
                if left_type != "bool":
                    self.declare_error(
                        f"Equality operation error '', The type of expression 'right' does not match the type of expression 'left',\nremember that the boolean 'not' operation always returns a bool, these are the types found: (left: '', right: 'bool')",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                
                else:
                    right_success = self.check_not_boolean_op(comparison_op.right, scope)
                
            elif isinstance(comparison_op.right, BinaryOpNode):
                if left_type == "int" or left_type == "float":
                    right_type, right_success = self.check_binary_op(comparison_op.right, scope, return_type=True)
                    
                    if left_type != right_type:
                        self.declare_error(
                            f"Equality operation error '{comparison_op.operator}', the type of the expression right does not match the expression left,\nremember that arithmetic operations always return a number of the same type as the numbers in the operation (int or float), also remember that two numbers in an equality operation must ALWAYS match in type, types found: (left: '{left_type}', right: '{right_type}')",
                            comparison_op.right.line,
                            comparison_op.right.column
                        )
                        right_success = False
                        
                else:
                    self.declare_error(
                        f"Equality operation error '{comparison_op.operator}', the type of the expression right does not match the expression left,\nremember that arithmetic operations always return a number of the same type as the numbers in the operation (int or float), also remember that two numbers in an equality operation must ALWAYS match in type, types found: (left: '{left_type}', right: '{right_type}')",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                         
            elif isinstance(comparison_op.right, UnaryNode):
                if left_type == "int" or left_type == "float":
                    right_type, right_success = self.check_unary_node(comparison_op.right, scope, return_type=True)

                    if left_type != right_type:
                        self.declare_error(
                            f"Equality operation error '{comparison_op.operator}', the type of the expression right does not match the expression left,\nremember that unary operations '-' always return a number of the same type as the numbers in the operation (int or float), also remember that two numbers in an equality operation must ALWAYS match in type, types found: (left: '{left_type}', right: '{right_type}')",
                            comparison_op.right.line,
                            comparison_op.right.column
                        )
                        right_success = False
                        
                else:
                    self.declare_error(
                        f"Equality operation error '{comparison_op.operator}', the type of the expression right does not match the expression left,\nremember that unary operations '-' always return a number of the same type as the numbers in the operation (int or float), also remember that two numbers in an equality operation must ALWAYS match in type, types found: (left: '{left_type}', right: '{right_type}')",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                
            elif isinstance(comparison_op.right, BooleanOpNode):
                if left_type == "bool":
                    left_success = self.check_boolean_op(comparison_op.left, scope)

                else:
                    self.declare_error(
                        f"Equality operation error '{comparison_op.operator}', the type of the expression right does not match the expression left,\nremember that boolean operations always return a bool, returned types: (left: '{left_type}', right: 'bool')",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                    
            elif isinstance(comparison_op.right, VariableNode):
                var_type = self.check_variable(comparison_op.right, scope)
                
                if var_type == "non-existent":
                    self.declare_error(
                        f"Variable called '{comparison_op.right.name}' does not exist, try using a valid expression.",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                    
                elif var_type == "none":
                    self.declare_error(
                        f"The variable '{comparison_op.right.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value,\nor another valid expression.",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                
                elif not(var_type == "string" or
                      var_type == "bool" or
                      var_type == "int" or
                      var_type == "float"
                    ):
                    self.declare_error(
                        f"A valid value was expected in the equality operation '{comparison_op.operator}', try using valid expressions on both sides of the operation",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                
                else:
                    
                    if left_type != var_type:
                        self.declare_error(
                            f"Equality operation error '{comparison_op.operator}', the type of the expression right does not match the expression left, returned types: (left: '{left_type}', right: '{right_type}')",
                            comparison_op.right.line,
                            comparison_op.right.column
                        )
                        
                    left_success = True
                    
            else:
                self.declare_error(
                    f"A valid value was expected in the equality operation '{comparison_op.operator}', try using valid expressions on both sides of the operation",
                    comparison_op.right.line,
                    comparison_op.right.column
                )
            
            return left_success and right_success
            
        # Other comparison
        else:
            # Part left
            left_type: str
            left_success = False
            
            if (isinstance(comparison_op.left, IntNode) or
                isinstance(comparison_op.left, FloatNode) or
                isinstance(comparison_op.left, StringNode)
                ):
                left_type = comparison_op.left.type
                left_success = True
            
            elif isinstance(comparison_op.left, NoneNode):
                self.declare_error(
                    f"Empty expression error, a 'none' value was used in the comparison operation '{comparison_op.operator}', please use a valid expression, remember that 'none' values ​​are unusable",
                    comparison_op.left.line,
                    comparison_op.left.column
                )
            
            elif isinstance(comparison_op.left, BinaryOpNode):
                left_type, left_success = self.check_binary_op(comparison_op.left, scope, return_type=True)
            
            elif isinstance(comparison_op.left, UnaryNode):
                left_type, left_success = self.check_unary_node(comparison_op.left, scope, return_type=True)
            
            elif isinstance(comparison_op.left, VariableNode):
                var_type = self.check_variable(comparison_op.left, scope)
                
                if var_type == "non-existent":
                    self.declare_error(
                        f"Variable called '{comparison_op.left.name}' does not exist, try using a valid expression.",
                        comparison_op.left.line,
                        comparison_op.left.column
                    )
                
                elif var_type == "none":
                    self.declare_error(
                        f"The variable '{comparison_op.left.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value,\nor another valid expression.",
                        comparison_op.left.line,
                        comparison_op.left.column
                    )
                
                elif not(var_type == "string" or
                      var_type == "int" or
                      var_type == "float"
                    ):
                    self.declare_error(
                        f"A valid value was expected in the comparison operation '{comparison_op.operator}', try using valid expressions on both sides of the operation",
                        comparison_op.left.line,
                        comparison_op.left.column
                    )
                
                else:
                    left_type = var_type
                    left_success = True
                    
            else:
                self.declare_error(
                    f"A valid value was expected in the comparison operation '{comparison_op.operator}', try using valid expressions on both sides of the operation",
                    comparison_op.left.line,
                    comparison_op.left.column
                )
            
            
            # Part right
            right_success = False
            
            if (isinstance(comparison_op.right, IntNode) or
                isinstance(comparison_op.right, FloatNode) or
                isinstance(comparison_op.right, StringNode)
                ):

                if left_type != comparison_op.right.type:
                    self.declare_error(
                        f"Comparison operation error '{comparison_op.operator}', the type of the expression right does not match the type of the expression left,\ntry using expressions that match in types, these are the types found: (left: '{left_type}', right: '{comparison_op.right.type}')",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                        
                else:
                    right_success = True
            
            elif isinstance(comparison_op.right, NoneNode):
                self.declare_error(
                    f"Empty expression error, a 'none' value was used in the comparison operation '{comparison_op.operator}', please use a valid expression, remember that 'none' values ​​are unusable",
                    comparison_op.right.line,
                    comparison_op.right.column
                )
            
            elif isinstance(comparison_op.right, BinaryOpNode):
                if left_type == "int" or left_type == "float":
                    right_type, right_success = self.check_binary_op(comparison_op.right, scope, return_type=True)
                    
                    if left_type != right_type:
                        self.declare_error(
                            f"Comparison operation error '{comparison_op.operator}', the type of the expression right does not match the expression left,\nremember that arithmetic operations always return a number of the same type as the numbers in the operation (int or float), also remember that two numbers in an equality operation must ALWAYS match in type, types found: (left: '{left_type}', right: '{right_type}')",
                            comparison_op.right.line,
                            comparison_op.right.column
                        )
                        right_success = False
                        
                else:
                    self.declare_error(
                        f"Comparison operation error '{comparison_op.operator}', the type of the expression right does not match the expression left,\nremember that arithmetic operations always return a number of the same type as the numbers in the operation (int or float), also remember that two numbers in an equality operation must ALWAYS match in type, types found: (left: '{left_type}', right: '{right_type}')",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                         
            elif isinstance(comparison_op.right, UnaryNode):
                if left_type == "int" or left_type == "float":
                    right_type, right_success = self.check_unary_node(comparison_op.right, scope, return_type=True)

                    if left_type != right_type:
                        self.declare_error(
                            f"Comparison operation error '{comparison_op.operator}', the type of the expression right does not match the expression left,\nremember that unary operations '-' always return a number of the same type as the numbers in the operation (int or float), also remember that two numbers in an equality operation must ALWAYS match in type, types found: (left: '{left_type}', right: '{right_type}')",
                            comparison_op.right.line,
                            comparison_op.right.column
                        )
                        right_success = False
                        
                else:
                    self.declare_error(
                        f"Comparison operation error '{comparison_op.operator}', the type of the expression right does not match the expression left,\nremember that unary operations '-' always return a number of the same type as the numbers in the operation (int or float), also remember that two numbers in an equality operation must ALWAYS match in type, types found: (left: '{left_type}', right: '{right_type}')",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                                   
            elif isinstance(comparison_op.right, VariableNode):
                var_type = self.check_variable(comparison_op.right, scope)
                
                if var_type == "non-existent":
                    self.declare_error(
                        f"Variable called '{comparison_op.right.name}' does not exist, try using a valid expression.",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                    
                elif var_type == "none":
                    self.declare_error(
                        f"The variable '{comparison_op.right.name}' exists but has no assigned value; its current value 'none' is not manipulable. Try assigning it a valid value,\nor another valid expression.",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                
                elif not(var_type == "string" or
                      var_type == "int" or
                      var_type == "float"
                    ):
                    self.declare_error(
                        f"A valid value was expected in the comparison operation '{comparison_op.operator}', try using valid expressions on both sides of the operation",
                        comparison_op.right.line,
                        comparison_op.right.column
                    )
                
                else:
                    
                    if left_type != var_type:
                        self.declare_error(
                            f"Equality operation error '{comparison_op.operator}', the type of the expression right does not match the expression left, returned types: (left: '{left_type}', right: '{right_type}')",
                            comparison_op.right.line,
                            comparison_op.right.column
                        )
                        
                    left_success = True
                    
            else:
                self.declare_error(
                    f"A valid value was expected in the comparison operation '{comparison_op.operator}', try using valid expressions on both sides of the operation",
                    comparison_op.right.line,
                    comparison_op.right.column
                )
            
            return left_success and right_success
        
        
        
        
    
            
        