from akon.lexer.lexer import Lexer
from akon.parser.parser import Parser
from akon.runtime.interpreter import Interpreter
from akon.diagnostic.akon_errors import ErrorReporter
from akon.utils.print_ast import print_ast
from akon.utils.print_scope import print_scope
import pathlib

#Reporter Error
reporter = ErrorReporter()

#code -> lexer -> tokens -> parser -> root_node -> interpreter
def main():
    while True:
        #Entrada de comandos
        entrada = input(">> ")
        
        if entrada == "exit":
            break
        
        base_dir = pathlib.Path(__file__).parent
        ruta = base_dir / "examples/test.akon"
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.touch(exist_ok=True)
        
        #Code Akon
        with open(ruta, "r") as ak:
            code = ak.read()
        
        #Lexer
        lexer = Lexer(code, reporter)
        tokens = lexer.get_tokens()
        
        #Parser
        parser = Parser(tokens, reporter)
        root_node = parser.parse_program()
        
        #AST print
        #print("===ABSTRACT SINTACTIC TREE===")
        #print_ast(root_node)
        
        #Interpreter
        interpreter = Interpreter(root_node, reporter)
        interpreter.interpret_main(root_node)
        
        
        
        #print("\n===ENVIROMENT(SCOPE)===")
        #print_scope(root_node.scope)
    
    
if __name__ == "__main__":
    
    try:
        main()
    except:
        reporter.display()