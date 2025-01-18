from lexer.lex_token import (Token, TokenType)

class ParserError:
    def __init__(self, token: Token) -> None:
        self.token = token
    
    def report(self, mensagem: str) -> str:
        print("\033[91mErro na analise sintatica:\033[0m")
        
        if self.token.tipo == TokenType.EOF:
            return f"Erro no fim do arquivo\n{mensagem}\n\n"
        
        return f"Erro na linha {self.token.linha}: {self.token.lexema}\n{mensagem}\n\n"