from lexer.lex_token import Token
from .expressao import *
from typing import Optional

from enum import Enum, auto
from dataclasses import dataclass

class TipoPrimitivo(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()
    
@dataclass
class TipoLista:
    interno: TipoPrimitivo
    
Tipo = TipoLista | TipoPrimitivo

@dataclass
class Parametro:
    nome: Token
    tipo: Tipo

class Declaracao:
    pass

class Bloco(Declaracao):
    def __init__(self, statements: list[Declaracao]) -> None:
        self.statements = statements

class Expr(Declaracao):
    def __init__(self, expressao: Expressao) -> None:
       self.expressao = expressao

class If(Declaracao):
    def __init__(self, condicao: Expressao, then_branch: Declaracao, else_branch: Optional[Declaracao]):
        self.condicao = condicao
        self.then_branch = then_branch
        self.else_branch = else_branch

class Print(Declaracao):
    def __init__(self, expressao: Expressao) -> None:
       self.expressao = expressao

class Return(Declaracao):
    def __init__(self, token: Token, valor: Optional[Expressao]):
        self.token = token
        self.valor = valor

class Funcao(Declaracao):
    def __init__(self, nome: Token, params: list[Parametro], corpo: list[Declaracao], tipo_retorno: Tipo):
        self.nome = nome
        self.params = params
        self.corpo = corpo

class Var(Declaracao):
    def __init__(self, nome: Token, inicializador: Optional[Expressao], tipo: Tipo) -> None:
       self.nome = nome
       self.inicializador = inicializador
       self.tipo = tipo
       
class While(Declaracao):
    def __init__(self, condicao: Expressao, corpo: Optional[Declaracao]) -> None:
        self.condicao = condicao
        self.corpo = corpo