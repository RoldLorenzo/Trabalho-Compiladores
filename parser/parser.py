from lexer.lex_token import (
    Token,
    TokenType
)
from arvores_sintaticas.expressao import *
from .parser_error import ParserError
from typing import NoReturn

# Crafting Interpreters, Robert Nystrom - Cap. 6.

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.posicao: int = 0
    
    def parse(self) -> Expressao:
        return self.expressao()
    
    def expressao(self) -> Expressao:
        return self.igualdade()
    
    def igualdade(self) -> Expressao:
        expressao = self.comparacao()
        
        while self.match(TokenType.DIFERENTE, TokenType.IGUAL_IGUAL):
            operador = self.anterior()
            direita = self.comparacao()
            expressao = Binaria(expressao, operador, direita)
            
        return expressao
    
    def comparacao(self) -> Expressao:
        expressao = self.termo()
        
        while self.match(
            TokenType.MAIOR,
            TokenType.MAIOR_IGUAL,
            TokenType.MENOR,
            TokenType.MENOR_IGUAL
        ):
            operador = self.anterior()
            direita = self.termo()
            expressao = Binaria(expressao, operador, direita)
            
        return expressao
    
    def termo(self) -> Expressao:
        expressao = self.fator()
        
        while self.match(
            TokenType.MENOS,
            TokenType.MAIS
        ):
            operador = self.anterior()
            direita = self.fator()
            expressao = Binaria(expressao, operador, direita)
            
        return expressao
    
    def fator(self) -> Expressao:
        expressao = self.unaria()
        
        while self.match(
            TokenType.ASTERISCO,
            TokenType.BARRA
        ):
            operador = self.anterior()
            direita = self.unaria()
            expressao = Binaria(expressao, operador, direita)
            
        return expressao
    
    def unaria(self) -> Expressao:
        if self.match(TokenType.EXCLAMACAO, TokenType.MENOS):
            operador = self.anterior()
            direita = self.unaria()
            return Unaria(operador, direita)
        
        return self.primaria()
    
    def primaria(self) -> Expressao:
        if self.match(TokenType.BANDIDO): return Literal(False)
        if self.match(TokenType.MOCINHO): return Literal(True)
        if self.match(TokenType.DESERTO): return Literal(None)
        if self.match(TokenType.STRING): return Literal(self.anterior().lexema)
        
        if self.match(TokenType.INT): 
            return Literal(int(self.anterior().lexema))
        if self.match(TokenType.FLOAT): 
            return Literal(float(self.anterior().lexema))
        
        if self.match(TokenType.ABRE_PARENTESES):
            expressao = self.expressao()
            self.espera(TokenType.FECHA_PARENTESES, "Esperado ')' apos essa expressao")
            return Agrupamento(expressao)
        
        self.erro("Eu esperava uma expressao aqui")
        
    def erro(self, mensagem: str) -> NoReturn:
        erro = ParserError(self.peek())
        print(erro.report(mensagem))
        exit(1)
    
    def espera(self, tipo: TokenType, mensagem: str) -> Token:
        if self.check(tipo): return self.avanca()
        
        self.erro(mensagem)
    
    def sincroniza(self) -> None:
        self.avanca()
        
        while not self.fim_tokens():
            if self.anterior().tipo == TokenType.PONTO_VIRGULA:
                return
            
            if self.peek().tipo in {
                TokenType.BANG,
                TokenType.MISS,
                TokenType.CAVALGANDO,
                TokenType.XERIFE,
                TokenType.PROCURADO,
                TokenType.VORTA,
                TokenType.DESERTO,
                TokenType.MOCINHO,
                TokenType.BANDIDO,
                TokenType.ATIRE,
            }: 
                return
            
            self.avanca()
    
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
        return self.tokens[self.posicao]
    
    # Retorna o token que esta na ultima posicao consumida na lista.
    def anterior(self) -> Token:
        return self.tokens[self.posicao - 1]