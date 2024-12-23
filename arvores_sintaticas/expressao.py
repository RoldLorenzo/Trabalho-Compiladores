from __future__ import annotations
from lexer.lex_token import Token

tipo_literal = int | float | str | bool | None

class Expressao:
    # Como essa eh uma classe abstrata, esse metodo nunca deve ser usado diretamente.
    def to_str(self) -> str:
        return ""
        
    def coloca_parenteses(self, nome: str, *expressoes: Expressao) -> str:
        resultado = f"({nome}"
        
        for expressao in expressoes:
            resultado += " "
            resultado += expressao.to_str()
        
        resultado += ")"
        
        return resultado

class Binaria(Expressao):
    def __init__(self, esquerda: Expressao, operador: Token, direita: Expressao) -> None:
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita
        
    def to_str(self) -> str:
        return self.coloca_parenteses(self.operador.lexema, self.esquerda, self.direita)

class Unaria(Expressao):
    def __init__(self, operador: Token, direita: Expressao) -> None:
        self.operador = operador
        self.direita = direita
    
    def to_str(self) -> str:
        return self.coloca_parenteses(self.operador.lexema, self.direita)

class Literal(Expressao):
    def __init__(self, valor: tipo_literal) -> None:
        self.valor = valor
    
    def to_str(self) -> str:
        return str(self.valor)

class Agrupamento(Expressao):
    def __init__(self, expressao: Expressao) -> None:
        self.expressao = expressao
        
    def to_str(self) -> str:
        return self.coloca_parenteses("grupo", self.expressao)