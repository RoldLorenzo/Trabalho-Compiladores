from lexer.lex_token import Token

tipo_literal = int | float | str | bool

class Expressao:
   pass

class Binaria(Expressao):
    def __init__(self, esquerda: Expressao, operador: Token, direita: Expressao):
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita

class Unaria(Expressao):
    def __init__(self, operador: Token, direita: Expressao):
        self.operador = operador
        self.direita = direita

class Literal(Expressao):
    def __init__(self, valor: tipo_literal):
        self.valor = valor

class Agrupamento(Expressao):
    def __init__(self, expressao: Expressao):
        self.expressao = expressao