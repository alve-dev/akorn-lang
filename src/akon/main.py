from akon.lexer.lexer import Lexer
from akon.parser.parser import Parser
from akon.runtime.interpreter import Interpreter
from akon.enviroment.enviroment import Enviroment
from akon.diagnostic.akon_errors import ErrorReporter
from akon.utils.print_ast import print_ast
from akon.utils.print_scope import print_scope

#Reporter Error
reporter = ErrorReporter()

#code -> lexer -> tokens -> parser -> root_node -> interpreter
def main():
    #Code Akon
    code = """
    print("Alejandro");"""
    
    #Lexer
    lexer = Lexer(code, reporter)
    tokens = lexer.get_tokens()
    
    #Enviroment
    enviroment = Enviroment()
    
    #Parser
    parser = Parser(tokens, reporter, enviroment)
    root_node = parser.parse_program()
    
    #AST print
    #print("===ABSTRACT SINTACTIC TREE===")
    print_ast(root_node)
    
    #Interpreter
    interpreter = Interpreter(root_node, reporter, enviroment)
    interpreter.interpret()
    
    #print("\n===ENVIROMENT(SCOPE)===")
    #print_scope(enviroment)
    
    
if __name__ == "__main__":
    
    try:
        main()
    except:
        reporter.display()