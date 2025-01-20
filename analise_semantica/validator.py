""" from arvores_sintaticas.declaracao import *
from arvores_sintaticas.expressao import *
from enum import Enum, auto
from dataclasses import dataclass
from lexer.lex_token import Token

class Categoria(Enum):
    FUNCAO = auto()

class Tipo(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()

class Simbolo:
    def __init__(self, token: Token):
        self.token = token

class SimboloVar(Simbolo):
    def __init__(self, token: Token, tipo: Tipo, valor: tipo_literal):
        super.__init__(token)
        self.tipo = tipo
        self.valor = valor

class SimboloFunc:
    def __init__(self, token: Token, tipo_retorno: Tipo):
        super.__init__(token)
        
class SimboloLiteral(Simbolo):
    def __init__(self, tipo: Tipo, valor: tipo_literal)

class TabelaSimbolos:
    def __init__(self):
        self.variaveis: dict[str, SimboloVar]
        self.funcoes: dict[str, SimboloFunc]

class Validator:
    def __init__(self, declaracoes: list[Declaracao]):
        self.declaracoes = declaracoes
        
    def analisa(self) -> TabelaSimbolos:
        return {"teste": Simbolo(Categoria.FUNCAO, )} """