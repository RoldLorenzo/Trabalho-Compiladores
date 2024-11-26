from lexer.lex_token import Token

class ParserError:
    def __init__(self, token: Token) -> None:
        self.token = token
    
    def report(self, mensagem: str) -> str:
        return f"Error at {self.token.linha}: {self.token.lexema}\n{mensagem}\n\n"