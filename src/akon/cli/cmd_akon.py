from akon.lexer.lexer import Lexer
from akon.parser.parser import Parser
from akon.runtime.interpreter import Interpreter
from akon.utils.print_ast import print_ast
import pathlib

def cmd_akon_run(rute_script: str, reporter):
    ruta = pathlib.Path(rute_script)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.touch(exist_ok=True)
        
    #Code Akon
    with open(ruta, "r") as file_ak:
        code = file_ak.read()
    
    #Lexer
    lexer = Lexer(code, reporter)
    tokens = lexer.tokenize()
    
    if reporter.has_errors():
        reporter.display()
        return    
    
    #Parser
    parser = Parser(tokens, reporter)
    root_node = parser.parse_program()
    
    if reporter.has_errors():
        reporter.display()
        return
    
    #Interprete
    interpreter = Interpreter(root_node, reporter)
    interpreter.interpret_main(root_node)
    
    if reporter.has_errors():
        reporter.display()
        return
    
def cmd_akon_tokens(rute_script: str, reporter):
    ruta = pathlib.Path(rute_script)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.touch(exist_ok=True)
        
    #Code Akon
    with open(ruta, "r") as file_ak:
        code = file_ak.read()
    
    #Lexer
    lexer = Lexer(code, reporter)
    tokens = lexer.tokenize()
    
    if reporter.has_errors():
        reporter.display()
        return
    
    #Print Tokens
    print("Tokens of akon script\n")
    len_tokens = len(tokens)
    
    for i in range(len_tokens):
        print(f"{i} => {tokens[i]}")

def cmd_akon_ast(rute_script: str, reporter):
    ruta = pathlib.Path(rute_script)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.touch(exist_ok=True)
        
    #Code Akon
    with open(ruta, "r") as file_ak:
        code = file_ak.read()
    
    #Lexer
    lexer = Lexer(code, reporter)
    tokens = lexer.tokenize()
    
    if reporter.has_errors():
        reporter.display()
        return
    
    #Parser
    parser = Parser(tokens, reporter)
    root_node = parser.parse_program()
    
    if reporter.has_errors():
        reporter.display()
        return
    
    #Print ast
    print_ast(root_node)
   
def cmd_akon_version():
    print("--Akon Programming Language: v0.1.0--")

def cmd_akon_help():
    print("--Akon-Cli Commands--\n\n")
    
    print("-ast: Command that executes an akon script and displays its parent node, syntax: akon ast [path to akon script]\n")
    print("-exit: Command that exits the akon repl, syntax: akon repl, can only be done in the repl\n")
    print("-help: displays all akon-cli commands with their function and syntax, syntax: akon help\n")
    print("-repl: activates the interactive mode of the akon programming language, syntax: akon repl\n")
    print("-run: Command that fully executes an akon script, syntax: akon run [path to akon script]\n")
    print("-token: Command that executes an akon script up to the lexer and displays the created tokens, syntax: akon token [path to akon script]\n")
    print("-version: displays the current language version, syntax: akon version\n")
    
        