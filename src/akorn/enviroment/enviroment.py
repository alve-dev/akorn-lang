from akorn.ast import Node
from typing import Any

class Enviroment:
    def __init__(self, parent = None) -> None:
        self.parent = parent
        self.scope: dict[str : Any] = {}
        
    def add_var(self, value: Any, name: str):
        self.scope[name] = value
    
    def get(self, name: str) -> Any:
        if name in self.scope:
            return self.scope[name]
        else:
            if isinstance(self.parent, Enviroment):
                return self.parent.get(name)

        return None

    def exists(self, name: str) -> bool:
        if name in self.scope:
            return True
        else:
            if isinstance(self.parent, Enviroment):
                return self.parent.exists(name)

        return False
    
    def assign(self, name: str, new_value: Any):
        if name in self.scope:
            self.scope[name] = new_value
        else:
            if isinstance(self.parent, Enviroment):
                self.parent.assign(name, new_value)
            
