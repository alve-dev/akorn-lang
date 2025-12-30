from akon.ast import Node

class Enviroment:
    def __init__(self, parent = None) -> None:
        self.parent = parent
        self.scope = {"variables":{}}
    
    def stop(self):
        raise Exception
    
    def define_var(self, name: str, type: str, constant: bool, value: Node) -> bool:
        if self.lookup_var(name):
            return False
        else:
            self.scope["variables"].update({
                    name:{
                        "var_type" : type,
                        "var_value" : value,
                        "is_constant": constant,
                        "interpreted": False
                    }
                }
            )
            return True
        
    def assignment_var(self, name: str, value, interpreted: bool = False) -> bool:
        if name in self.scope["variables"].keys():
            self.scope["variables"][name]["var_value"] = value
            self.scope["variables"][name]["interpreted"] = interpreted
            return True
        else:
            if (self.parent, Enviroment):
                return self.parent.assignment_var(name, value, interpreted)
                
            else:
                return False
    
    def get_var(self, name: str):
        if name in self.scope["variables"]:
            value = self.scope["variables"][name]["var_value"]
            interpreted = self.scope["variables"][name]["interpreted"]
            get_var_pack = {"value":value, "interpreted":interpreted}
        else:
            if isinstance(self.parent, Enviroment):
                get_var_pack = self.parent.get_var(name)
                
            else:
                self.stop()
        
        return get_var_pack

    def lookup_var(self, name: str) -> bool:
        if "variables" in self.scope.keys():
            if name in self.scope["variables"].keys():
                return True
            else:
                if isinstance(self.parent, Enviroment):
                    return self.parent.lookup_var(name)
        
        return False   
        
        
        