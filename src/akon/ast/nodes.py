class Node:
    def __repr__() -> str:
        return f"<{__class__.__name__}>"

class NullValue:
    """Null value of akon"""
    
    def __repr__(self):
        return "NONE"

AKON_NONE = NullValue()
  
class NoneNode:
    def __init__(self, line: int, column: int):
        self.value = AKON_NONE
        self.type = "NONE"
        self.line = line
        self.column = column
        
class LiteralNode(Node):
    pass

class IntNode(LiteralNode):
    def __init__(self, value: str, line: int, column: int) -> None:
        self.value = int(value)
        self.type = "INT"
        self.line = line
        self.column = column
        
    def __repr__(self) -> str:
        return f"<{__class__.__name__} value={self.value}>"

class FloatNode(LiteralNode):
    def __init__(self, value: str, line: int, column: int) -> None:
        self.value = value
        self.type = "FLOAT"
        self.line = line
        self.column = column
        
    def __repr__(self) -> str:
        return f"<{__class__.__name__} value={self.value}>"

class StringNode(LiteralNode):
    def __init__(self, value: str, line: int, column: int) -> None:
        self.value = value
        self.type = "STRING"
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f"{__class__.__name__} string={self.value})"

class BoolNode(LiteralNode):
    def __init__(self, value: bool, line:int, column:int) -> None:
        self.value = value
        self.type = "BOOL"
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f"<{__class__.__name__} value={self.value}>"

class UnaryNode(Node):
    def __init__(self, operator:str, node: Node) -> None:
        self.operator = operator
        self.node = node
        
    def __repr__(self) -> str:
        return f"<{__class__.__name__} operator={self.operator} value={self.node})>"

class BooleanOpNode(Node):
    def __init__(self, left: Node, operator: str, right: Node) -> None:
        self.left = left
        self.operator = operator
        self.right = right
        
    def __repr__(self):
        return f"<{__class__.__name__} left={self.left} operator={self.operator}, right={self.right}"

class ComparisonOpNode(Node):
    def __init__(self, left: Node, operator: str, right: Node) -> None:
        self.left = left
        self.operator = operator
        self.right = right
        
    def __repr__(self):
        return f"<{__class__.__name__} left={self.left} operator={self.operator} right={self.right}"

class BinaryOpNode(Node):
    def __init__(self, left:Node, operator:str, right:Node):
        self.left = left
        self.operator = operator
        self.right = right
        
    def __repr__(self) -> str:
        return f"<{__class__.__name__} left={self.left} operator={self.operator} right={self.right}>"

class VariableNode(Node):
    def __init__(self, name: str) -> None:
        self.name = name
    
    def __repr__(self) -> str:
        return f"<{__class__.__name__} name={self.name}>"
        
class AssignmentNode(Node):
    def __init__(self, name: str, value: Node) -> None:
        self.name = name
        self.value = value
        
    def __repr__(self) -> str:
        return f"<{__class__.__name__} name={self.name} value={self.value}>"
        
    def evaluate(self):
        return self.value.evaluate()
    
    def pretty_print(self):
        return f"{self.name} = {self.value.pretty_print()}"

class DeclarationNode(Node):
    def __init__(self, name: str, type: str, value: Node = NoneNode):
        self.name = name
        self.type = type
        self.value = value
        
    def __repr__(self):
        return f"<{__class__.__name__} type={self.type} name={self.name} value={self.value}>"
        
class ProgramNode(Node):
    def __init__(self, statements: list[Node]) -> None:
        self.statements = statements
        
    def __repr__(self):
        return f"<{__class__.__name__} statements={self.statements}>"