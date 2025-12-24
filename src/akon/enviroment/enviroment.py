from akon.ast.nodes import Node

class Enviroment:
    def __init__(self) -> None:
        self.scope = {"variables":{}}
    
    def define_var(self, name: str, type: str, value: Node) -> bool:
        if self.lookup_var(name):
            return False
        
        else:
            self.scope["variables"] = {
                name: {
                    "var_type" : type,
                    "var_value" : value,
                    "interpreted": False,
                }
            }
            return True
        
    def assignment_var(self, name: str, value: Node) -> bool:
        if self.lookup(name):
            self.scope["variables"][name]["var_value"] = value
            return True
            
        else:
            return False
       
    def lookup_var(self, name: str) -> bool:
        if name in self.scope["variables"].keys():
            return True
        
        return False   
        
        
        