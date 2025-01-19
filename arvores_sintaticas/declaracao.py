from lexer.lex_token import Token
from .expressao import Expressao
from typing import Optional

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
       
class Var(Declaracao):
    def __init__(self, nome: Token, inicializador: Optional[Expressao]) -> None:
       self.nome = nome
       self.inicializador = inicializador
       
class While(Declaracao):
    def __init__(self, condicao: Expressao, corpo: Declaracao) -> None:
        self.condicao = condicao
        self.corpo = corpo