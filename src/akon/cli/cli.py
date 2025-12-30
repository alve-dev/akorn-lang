from sys import argv
from .repl import repl
from .cmd_akon import cmd_akon_run, cmd_akon_tokens, cmd_akon_ast, cmd_akon_version, cmd_akon_help

def run_cli(reporter):
    if len(argv) < 3 or argv[1] != "akon":
        print("Usage: akon [commands]")
        return
    
    args = argv[2:]
    
    if args[0] == "run":
        try:
            cmd_akon_run(args[1], reporter)
        except IndexError:
            print("Usage: akon run [rute script akon]")
            
    elif args[0] == "token":
        try:
            cmd_akon_tokens(args[1], reporter)
        except IndexError:
            print("Usage: akon token [rute script akon]")

    elif args[0] == "ast":
        try:
            cmd_akon_ast(args[1], reporter)
        except IndexError:
            print("Usage: akon ast [rute script akon]")
            
    elif args[0] == "version":
        cmd_akon_version()
        
    elif args[0] == "help":
        cmd_akon_help()
    
    elif args[0] == "repl":
        repl(reporter)
    
# run = correr el archivo en el interprete
# tokens = correr hasta conseguir lista de tokens y mostarlas
# ast = correr hasta conseguir nodos y ponerlos
# version = mostrar la version en la que esta el lenguaje
# exit = salir de repl
# help muestra comandos de akon-cli