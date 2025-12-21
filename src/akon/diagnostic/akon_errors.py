from __future__ import annotations
from typing import Optional, Any
from rich.console import Console


class AkonError:
    """Base class for all errors in the CyLp language."""
    
    def __init__(
        self,
        message: str,
        line: int,
        column: int,
        token: Optional[str] = None,
        **extra: Any,
    ) -> None:
        self.message = message
        self.line = line
        self.column = column
        self.token = token
        self.__dict__.update(extra)
    
    def details(self):
        return " "
       
    def format(self) -> str:
        """Returns a pretty string of the error"""
        
        location = f"line: {self.line}, col: {self.column}"
        token_part = f" cerca de '{self.token}'" if self.token else ""
        detail = self.details()
        
        return f"[cyan]{location}[/] [bold red]{self.__class__.__name__}[/]: {self.message}[yellow]{detail}{token_part}[/]"
   
    
    def format_file(self) -> str:
        """Returns a plain string of the error"""
        
        location = f"line: {self.line}, col: {self.column}"
        token_part = f" cerca de '{self.token}'" if self.token else ""
        detail = self.details()
        
        return f"{location} {self.__class__.__name__}: {self.message}{detail}{token_part}"      
            
    def __str__(self):
        """For print(error) to work automatically"""
        return self.format()
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.message}', {self.line}, {self.column})"
 
class LexerError(AkonError):
    """Lexical error: prohibited character or sequence.
    
    Extra attributes: bad_char = the incorrect character."""    
    def details(self):
        return f" -> '{self.bad_char}'"
        
class ParserError(AkonError):
    """Syntax error: the parser expected something different.
    
    Extra attributes:
        expected = Lo que el parser esperaba
        get = Lo que el parser encontro"""
    
    def details(self):
        return f"(Expected: {self.expected}, Get: {self.get})"
         
class TypeErrorAkon(AkonError):
    """Type error during semantic analysis.
    
    Extra attributes:
        expected_type = The type who was waiting for the semantic
        get = The type who found the semantics"""
    
    def details(self):
        return f" -> esperado: {self.expected_type}, encontrado: {self.got_type}"

class DeclarationErrorAkon(AkonError):
    """"""


class NameErrorAkon(AkonError):
    """Undeclared or out-of-scope identifier.
    
    Extra attributes: name = the name that does not exist in the scope"""
    
    def details(self):
        return f" -> '{self.name}' no esta definido"

class RuntimeErrorAkon(AkonError):
    """Error during program execution."""
    
    def details(self):
        return f" durante operacion: {self.operation}"
        
class ErrorReporter:
    def __init__(self) -> None:
        self.errors: list[AkonError] = []
        self.console = Console()
    
    def add_error(self, error: AkonError) -> None:
        self.errors.append(error)
            
    def has_errors(self) -> bool:
        return len(self.errors) > 0
            
    def display(self) -> None:
        for error in self.errors:
            self.console.print(f"[white]{error}[/]")