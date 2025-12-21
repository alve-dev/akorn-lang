from akon.lexer.lexer import Lexer
from akon.parser.parser import Parser
from akon.enviroment.enviroment import Enviroment
from akon.diagnostic.akon_errors import ErrorReporter
from akon.utils.print_ast import print_ast

#Reporter Error
reporter = ErrorReporter()

def main():
    #Code Akon
    code = """Int number = 5;
    number = 10;"""
    
    #Lexer
    lexer = Lexer(code, reporter)
    tokens = lexer.get_tokens()
    
    #Enviroment
    env = Enviroment()
    
    #Parser
    parser = Parser(tokens, reporter, env)
    root_node = parser.parse_program()
    
    #AST print
    print_ast(root_node)
    print(env.env)
    
    
    
if __name__ == "__main__":
    
    try:
        main()
    except:
        reporter.display()