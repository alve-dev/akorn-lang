class Node:
    def __repr__() -> str:
        return f"<{__class__.__name__}>"

class NoneValue:
    """Null value of akon"""
    
    def __repr__(self):
        return f"<{__class__.__name__}"

AKON_NONE = NoneValue()
  
class NoneNode(Node):
    def __init__(
        self,
        line: int,
        column: int
        ):
        
        self.value = AKON_NONE
        self.type = "none"
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f"{__class__.__name__}"
        
class LiteralNode(Node):
    def __init__(
        self, 
        value, 
        line, 
        column
        ) -> None:
        
        self.value = value
        self.line = line
        self.column = column

class IntNode(LiteralNode):
    def __init__(
        self,
        value: int,
        line: int,
        column: int
        ) -> None:
        
        self.value = value
        self.type = "int"
        self.line = line
        self.column = column
        
    def __repr__(self) -> str:
        return f"<{__class__.__name__} value={self.value}>"

class FloatNode(LiteralNode):
    def __init__(
        self,
        value: float,
        line: int,
        column: int
        ) -> None:
        
        self.value = value
        self.type = "float"
        self.line = line
        self.column = column
        
    def __repr__(self) -> str:
        return f"<{__class__.__name__} value={self.value}>"

class StringNode(LiteralNode):
    def __init__(
        self,
        value: str,
        line: int,
        column: int
        ) -> None:
        
        self.value = value
        self.type = "string"
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f'<{__class__.__name__} value="{self.value}">'

class BoolNode(LiteralNode):
    def __init__(
        self,
        value: bool,
        line:int,
        column:int
        ) -> None:
        
        self.value = value
        self.type = "bool"
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f"<{__class__.__name__} value={self.value}>"

class UnaryNode(Node):
    def __init__(
        self,
        operator:str,
        node: Node
        ) -> None:
        
        self.operator = operator
        self.node = node
        
    def __repr__(self) -> str:
        return f"<{__class__.__name__} operator={self.operator} value={self.node})>"

class NotBooleanNode(Node):
    def __init__(
        self,
        node: Node
        ) -> None:
        
        self.node = node
        self.line: int = node.line
        self.column: int = node.column
        
    def __repr__(self):
        return f"<{__class__.__name__} value={self.node}"

class BooleanOpNode(Node):
    def __init__(
        self,
        left: Node,
        operator: str,
        right: Node
        ) -> None:
        
        self.left = left
        self.operator = operator
        self.right = right
        
    def __repr__(self):
        return f"<{__class__.__name__} left={self.left} operator={self.operator}, right={self.right}"

class ComparisonOpNode(Node):
    def __init__(
        self,
        left: Node,
        operator: str,
        right: Node
        ) -> None:
        
        self.left = left
        self.operator = operator
        self.right = right
        self.line: int = left.line
        self.column: int = left.column
        
    def __repr__(self):
        return f"<{__class__.__name__} left={self.left} operator={self.operator} right={self.right}"

class BinaryOpNode(Node):
    def __init__(
        self,
        left:Node,
        operator:str,
        right:Node
        ) -> None:
        
        self.left = left
        self.operator = operator
        self.right = right
        self.line: int = left.line
        self.column: int = left.column
        
    def __repr__(self) -> str:
        return f"<{__class__.__name__} left={self.left} operator={self.operator} right={self.right}>"

class VariableNode(Node):
    def __init__(
        self,
        name: str,
        line: int,
        column: int
        ) -> None:
        
        self.name = name
        self.line = line
        self.column = column
    
    def __repr__(self) -> str:
        return f"<{__class__.__name__} name={self.name}>"
        
class AssignmentNode(Node):
    def __init__(
        self,
        name: str,
        value: Node
        ) -> None:
        
        self.name = name
        self.value = value
        
    def __repr__(self) -> str:
        return f"<{__class__.__name__} name={self.name} value={self.value}>"

class DeclarationNode(Node):
    def __init__(
        self,
        name: str,
        type: str,
        value: Node = NoneNode
        ) -> None:
        
        self.name = name
        self.type = type
        self.value = value
        
    def __repr__(self):
        return f"<{__class__.__name__} type={self.type} name={self.name} value={self.value}>"

class ElseNode(Node):
    def __init__(
        self,
        statements: list[Node],
        scope
        ) -> None:
        
        self.statements = statements
        self.scope = scope
        
    def __repr__(self):
        return f"<{__class__.__name__} statements={self.statements}"
    
class ElIfNode(Node):
    def __init__(
        self,
        condition: Node,
        statements: list[Node],
        scope,
        elif_node,
        else_node = NoneNode | ElseNode
        ) -> None:
        
        self.condition = condition
        self.statements = statements
        self.elif_node = elif_node
        self.scope = scope
        self.else_node = else_node

    def __repr__(self):
        return f"<{__class__.__name__} condition={self.condition}, statements={self.statements}>"    
    
class IfNode(Node):
    def __init__(
        self,
        condition: Node,
        statements: list[Node],
        scope,
        elif_nodes: NoneNode | ElIfNode,
        else_node = NoneNode | ElseNode
        ) -> None:
        
        self.condition = condition
        self.statements = statements
        self.elif_node = elif_nodes
        self.else_node = else_node
        self.scope = scope
        
    def __repr__(self):
        return f"<{__class__.__name__} condition={self.condition}, statements={self.condition}"

class CallNode(Node):
    def __init__(
        self,
        callee: str,
        args: list[Node]
        ) -> None:
        
        self.calle = callee
        self.args = args
        
    def __repr__(self):
        return f"<{__class__.__name__} calle={self.calle} args={self.args}"

class ProgramNode(Node):
    def __init__(
        self,
        statements: list[Node],
        scope
        ) -> None:
        
        self.statements = statements
        self.scope = scope
        
    def __repr__(self):
        return f"<{__class__.__name__} statements={self.statements}>"