from lexer.lex_token import (
    Token,
    TokenType
)

# Crafting Interpreters, Robert Nystrom - Cap. 6.

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.posicao: int = 0
    
    # Retorna True se o proximo token na lista eh de algum dos tipos passados como parametro.
    # Retorna False caso contrario
    def match(self, *tipos: TokenType) -> bool:
        for tipo in tipos:
            if self.check(tipo):
                self.avanca()
                return True
        
        return False
    
    # Retorna true se o proximo token na lista eh do tipo passado por parametro.
    def check(self, tipo: TokenType) -> bool:        
        return not self.fim_tokens() and self.peek().tipo == tipo
    
    # Retorna o proximo token na lista e o consome.
    def avanca(self) -> Token:
        if not self.fim_tokens():
            self.posicao += 1
            
        return self.anterior()
    
    # Retorna True se encontrou o fim do arquivo.
    def fim_tokens(self) -> bool:
        return self.peek().tipo == TokenType.EOF
    
    # Retorna qual o proximo token na lista sem o consumir.
    def peek(self) -> Token:
        self.tokens[self.posicao]
    
    # Retorna o token que esta na ultima posicao consumida na lista.
    def anterior(self) -> Token:
        self.tokens[self.posicao - 1]