from lexer.lex_token import (Token, TokenType)

class ParserError(Exception):
    def __init__(self, token: Token, mensagem: str) -> None:
        self.token = token
        self.mensagem = mensagem
    
    def report(self) -> None:
        print("\033[91mErro na analise sintatica:\033[0m")
        
        if self.token.tipo == TokenType.EOF:
            print(f"Erro no fim do arquivo\n{self.mensagem}\n\n")
        else:
            print(f"Erro na linha {self.token.linha}: {self.token.lexema}\n{self.mensagem}\n\n")