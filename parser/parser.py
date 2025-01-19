from lexer.lex_token import (
    Token,
    TokenType
)
from arvores_sintaticas.expressao import *
from arvores_sintaticas.declaracao import *
from .parser_error import ParserError
from typing import Optional, NoReturn

# Crafting Interpreters, Robert Nystrom - Caps. 6 - 8.

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.posicao: int = 0
        self.ocorreu_erro = False
        self.declaracoes: list[Declaracao] = []
    
    def parse(self) -> None:
        while not self.fim_tokens():
            declaracao = self.declaracao()
            
            if declaracao is not None:
                self.declaracoes.append(declaracao)
                
        if self.ocorreu_erro:
            exit(1)
    
    def declaracao(self) -> Optional[Declaracao]:
        try:
            if self.match(TokenType.XERIFE): return self.declaracao_variavel()
            
            return self.statement()
        except ParserError as e:
            e.report()
            
            self.sincroniza()
            return None
    
    def declaracao_variavel(self) -> Declaracao:
        nome: Token = self.espera(TokenType.IDENTIFICADOR, "Eu esperava um nome aqui.")
        
        inicializador: Optional[Expressao] = None
        
        if self.match(TokenType.IGUAL):
            inicializador = self.expressao()
            
        self.espera(TokenType.PONTO_VIRGULA, "Eu esperava encontrar ';' depois da declaracao da variavel.")
        return Var(nome, inicializador)
    
    def statement(self) -> Declaracao:
        if self.match(TokenType.BANG):
            return self.statement_if()
        
        if self.match(TokenType.CAVALGANDO):
            return self.statement_while()
        
        if self.match(TokenType.ATIRE):
            return self.statement_print()
        
        if self.match(TokenType.ABRE_CHAVE):
            return Bloco(self.bloco())
        
        return self.statement_expressao()
    
    def statement_if(self) -> Declaracao:
        self.espera(TokenType.ABRE_PARENTESES, "Eu esperava '(' apos um if.")
        condicao: Expressao = self.expressao()
        self.espera(TokenType.FECHA_PARENTESES, "Eu esperava ')' apos uma condicao.")
        
        then_branch: Declaracao = self.statement()
        else_branch: Optional[Declaracao] = None
        
        if self.match(TokenType.MISS):
            else_branch = self.statement()
            
        return If(condicao, then_branch, else_branch)
    
    def statement_while(self) -> Declaracao:
        self.espera(TokenType.ABRE_PARENTESES, "Eu esperava '(' apos um while.")
        condicao: Expressao = self.expressao()
        self.espera(TokenType.FECHA_PARENTESES, "Eu esperava ')' apos uma condicao.")
        
        corpo: Declaracao = self.declaracao()
        
        return While(condicao, corpo)
    
    def statement_print(self) -> Declaracao:
        valor: Expressao = self.expressao()
        
        self.espera(TokenType.PONTO_VIRGULA, "Eu esperava encontrar ';' depois do valor.")
        
        return Print(valor)
    
    def bloco(self) -> list[Declaracao]:
        declaracoes = []
        
        while not self.check(TokenType.FECHA_CHAVE) and not self.fim_tokens():
            declaracao = self.declaracao()
            
            if declaracao is not None:
                declaracoes.append(declaracao)
                
        self.espera(TokenType.FECHA_CHAVE, "Eu esperava '}' aqui.")
        return declaracoes
        
    def statement_expressao(self) -> Declaracao:
        expressao: Expressao = self.expressao()
        
        self.espera(TokenType.PONTO_VIRGULA, "Eu esperava encontrar ';' depois dessa expressao.")
        
        return Expr(expressao)
    
    def expressao(self) -> Expressao:
        return self.atribuicao()
    
    def atribuicao(self) -> Expressao:
        expressao: Expressao = self.ou()
        
        if self.match(TokenType.IGUAL):
            igual: Token = self.anterior()
            valor: Expressao = self.atribuicao()
            
            if isinstance(expressao, Variavel):
                nome: Token = expressao.nome
                return Atribuicao(nome, valor)
            
            self.erro("Isso nao e uma atribuicao valida.", igual)
            
        return expressao
    
    def ou(self) -> Expressao:
        expressao: Expressao = self.e()
        
        while self.match(TokenType.OR):
            operador: Token = self.anterior()
            direita: Expressao = self.e()
            expressao = Logica(expressao, operador, direita)
            
        return expressao
    
    def e(self) -> Expressao:
        expressao: Expressao = self.igualdade()
        
        while self.match(TokenType.AND):
            operador: Token = self.anterior()
            direita: Expressao = self.igualdade()
            expressao = Logica(expressao, operador, direita)
            
        return expressao
    
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
        
        if self.match(TokenType.IDENTIFICADOR):
            return Variavel(self.anterior())
        
        if self.match(TokenType.ABRE_PARENTESES):
            expressao = self.expressao()
            self.espera(TokenType.FECHA_PARENTESES, "Esperado ')' apos essa expressao")
            return Agrupamento(expressao)
        
        self.erro("Eu esperava uma expressao aqui")
        
    def erro(self, mensagem: str, token: Optional[Token] = None) -> NoReturn:
        self.ocorreu_erro = True
        
        if token is None:
            token = self.peek()
                
        raise ParserError(token, mensagem)
    
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
    
    # Retorna o proximo token caso ele seja do tipo esperado.
    # Adiciona um erro com a mensagem passada por parametro caso contrario.
    def espera(self, tipo: TokenType, mensagem: str) -> Token:
        if self.check(tipo): return self.avanca()
        
        self.erro(mensagem)
    
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