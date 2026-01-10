from .cmd_akorn import cmd_akorn_ast, cmd_akorn_help, cmd_akorn_run, cmd_akorn_tokens, cmd_akorn_version

def repl(reporter):
    while True:
        cmd = input(">> ")
        
        args = cmd.split(" ")
        
        if len(args) < 1:
            print("Usage: [command]")
            continue
        
        if args[0] == "exit":
            break
        
        elif args[0] == "run":
            try:
                cmd_akorn_run(args[1], reporter)
            except IndexError:
                print("Usage: run [rute script akon]")
            
        elif args[0] == "token":
            try:
                cmd_akorn_tokens(args[1], reporter)
            except IndexError:
                print("Usage: token [rute script akon]")
        
        elif args[0] == "ast":
            try:
                cmd_akorn_ast(args[1], reporter)
            except IndexError:
                print("Usage: ast [rute script akon]")
        
        elif args[0] == "version":
            cmd_akorn_version()
        
        elif args[0] == "help":
            cmd_akorn_help()
            
        
        