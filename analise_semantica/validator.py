from arvores_sintaticas.declaracao import *
from arvores_sintaticas.expressao import *
from lexer.lex_token import TokenType
from dataclasses import dataclass

class Ambiente:
    def __init__(self):
        self.variaveis: dict[str, Var]
        self.funcoes: dict[str, Funcao]

@dataclass
class Simbolo:
    lexema: str
    tipo_token: TokenType
    tipo: Optional[Tipo]
    valor: Optional[Expressao]

class Validator:
    def __init__(self, declaracoes: list[Declaracao]):
        self.declaracoes = declaracoes