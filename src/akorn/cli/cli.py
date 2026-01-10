from sys import argv
from .repl import repl
from .cmd_akorn import cmd_akorn_run, cmd_akorn_tokens, cmd_akorn_ast, cmd_akorn_version, cmd_akorn_help

def run_cli(reporter):
    if len(argv) < 2 or argv[1] != "akorn":
        print("Usage: akorn [commands]")
        return
    
    args = argv[2:]
    
    if args[0] == "run":
        try:
            cmd_akorn_run(args[1], reporter)
        except IndexError:
            print("Usage: akorn run [rute script akon]")
            
    elif args[0] == "token":
        try:
            cmd_akorn_tokens(args[1], reporter)
        except IndexError:
            print("Usage: akorn token [rute script akon]")

    elif args[0] == "ast":
        try:
            cmd_akorn_ast(args[1], reporter)
        except IndexError:
            print("Usage: akorn ast [rute script akon]")
            
    elif args[0] == "version":
        cmd_akorn_version()
        
    elif args[0] == "help":
        cmd_akorn_help()
    
    elif args[0] == "repl":
        repl(reporter)
    
# run = correr el archivo en el interprete
# tokens = correr hasta conseguir lista de tokens y mostarlas
# ast = correr hasta conseguir nodos y ponerlos
# version = mostrar la version en la que esta el lenguaje
# exit = salir de repl
# help muestra comandos de akon-cli