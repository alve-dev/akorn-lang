from .cmd_akon import cmd_akon_ast, cmd_akon_help, cmd_akon_run, cmd_akon_tokens, cmd_akon_version

def repl(reporter):
    while True:
        cmd = input(">> ")
        
        args = cmd.split(" ")
        
        if len(args) < 2 or args[0] != "akon":
            print("Usage: akon [command]")
            continue
        
        if args[1] == "exit":
            break
        
        elif args[1] == "run":
            try:
                cmd_akon_run(args[2], reporter)
            except IndexError:
                print("Usage: akon run [rute script akon]")
            
        elif args[1] == "token":
            try:
                cmd_akon_tokens(args[2], reporter)
            except IndexError:
                print("Usage: akon token [rute script akon]")
        
        elif args[1] == "ast":
            try:
                cmd_akon_ast(args[2], reporter)
            except IndexError:
                print("Usage: akon ast [rute script akon]")
        
        elif args[1] == "version":
            cmd_akon_version()
        
        elif args[1] == "help":
            cmd_akon_help()
            
        
        