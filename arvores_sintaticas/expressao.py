from __future__ import annotations
from lexer.lex_token import Token, TokenType

# Crafting Interpreters, Robert Nystrom - Cap. 5.

TipoLiteral = int | float | str | bool | None

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

class Atribuicao(Expressao):
    def __init__(self, nome: Token, valor: Expressao) -> None:
        self.nome = nome
        self.valor = valor
        
    def to_str(self):
        return self.coloca_parenteses("atribuicao " + self.nome.lexema, self.valor)

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

class Logica(Expressao):
    def __init__(self, esquerda: Expressao, operador: Token, direita: Expressao) -> None:
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita
        
    def to_str(self) -> str:
        return self.coloca_parenteses(self.operador.lexema, self.esquerda, self.direita)

class Literal(Expressao):
    def __init__(self, valor: TipoLiteral, tipo: TokenType) -> None:
        self.valor = valor
        self.tipo = tipo
    
    def to_str(self) -> str:
        return str(self.valor)

class Lista(Expressao):
    def __init__(self, valores: list[Expressao]) -> None:
        self.valores = valores
        
    def to_str(self) -> str:
        contents = "["
        for (i, v) in enumerate(self.valores):
            contents += v.to_str()
            
            if i < len(self.valores) - 1:
                contents += ", "
            
        contents += "]"
        
        return contents

class Chamada(Expressao):
    def __init__(self, chamado: Expressao, paren: Token, argumentos: list[Expressao]):
        self.chamado = chamado
        self.paren = paren
        self.argumentos = argumentos
        
    def to_str(self):
        return self.coloca_parenteses("chamada", self.chamado)

class Agrupamento(Expressao):
    def __init__(self, expressao: Expressao) -> None:
        self.expressao = expressao
        
    def to_str(self) -> str:
        return self.coloca_parenteses("grupo", self.expressao)
    
class Variavel(Expressao):
    def __init__(self, nome: Token) -> None:
        self.nome = nome
        
    def to_str(self):
        return self.nome.lexema