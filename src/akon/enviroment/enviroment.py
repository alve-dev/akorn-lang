from akon.ast.nodes import Node

class Enviroment:
    def __init__(self) -> None:
        self.env = {}
    
    def define_var(self, name: str, type: str, value: Node) -> bool:
        if self.lookup(name):
            return False
        
        else:
            self.env[name] = {
                "var_type" : type,
                "var_value" : value,
            }
            return True
        
    def assignment_var(self, name: str, value: Node) -> bool:
        if self.lookup(name):
            self.env[name]["var_value"] = value.value
            return True
            
        else:
            return False
            
    def lookup(self, name: str) -> bool:
        if name in self.env.keys():
            return True
        
        return False   
        
        
        