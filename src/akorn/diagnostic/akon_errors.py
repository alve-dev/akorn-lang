class ErrorReporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
    
    def add_error(self, error: str) -> None:
        self.errors.append(error)
            
    def has_errors(self) -> bool:
        return len(self.errors) > 0
    
    def clear_list_error(self) -> None:
        self.errors.clear()
            
    def display(self) -> None:
        for error in self.errors:
            print(f"{error}")