from lexer.lex_token import Token
from .expressao import *
from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass

# TODO: Melhorar a representacao das declaracoes.

class TipoPrimitivo(Enum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()
    
@dataclass
class TipoLista:
    interno: TipoPrimitivo
    
Tipo = TipoLista | TipoPrimitivo

@dataclass(repr=True)
class Parametro:
    nome: Token
    tipo: Tipo

class Declaracao:
    pass

class Bloco(Declaracao):
    def __init__(self, statements: list[Declaracao]) -> None:
        self.statements = statements
        
    def __repr__(self):
        return f"Bloco(statements=[{', '.join(repr(stmt) for stmt in self.statements)}])"

class Expr(Declaracao):
    def __init__(self, expressao: Expressao) -> None:
       self.expressao = expressao
    
    def __repr__(self):
        return f"Expr(expressao={self.expressao.to_str()})"

class If(Declaracao):
    def __init__(self, condicao: Expressao, then_branch: Declaracao, else_branch: Optional[Declaracao]):
        self.condicao = condicao
        self.then_branch = then_branch
        self.else_branch = else_branch
        
    def __repr__(self):
        else_branch_repr = repr(self.else_branch) if self.else_branch else 'None'
        return (f"If(condicao={repr(self.condicao)}, "
                f"then_branch={repr(self.then_branch)}, "
                f"else_branch={else_branch_repr})")

class Print(Declaracao):
    def __init__(self, expressao: Expressao) -> None:
       self.expressao = expressao
       
    def __repr__(self):
        return f"Print(expressao={self.expressao.to_str()})"

class Return(Declaracao):
    def __init__(self, token: Token, valor: Optional[Expressao]):
        self.token = token
        self.valor = valor
        
    def __repr__(self):
        valor_repr = repr(self.valor) if self.valor else 'None'
        return f"Return(token={repr(self.token)}, valor={valor_repr})"

class Funcao(Declaracao):
    def __init__(self, nome: Token, params: list[Parametro], corpo: list[Declaracao], tipo_retorno: Tipo):
        self.nome = nome
        self.params = params
        self.corpo = corpo
        self.tipo_retorno = tipo_retorno
        
    def __repr__(self):
        params_repr = ', '.join(repr(param) for param in self.params)
        corpo_repr = ', '.join(repr(stmt) for stmt in self.corpo)
        return (f"Funcao(nome={repr(self.nome)}, params=[{params_repr}], "
                f"corpo=[{corpo_repr}], tipo_retorno={repr(self.tipo_retorno)})")

class Var(Declaracao):
    def __init__(self, nome: Token, inicializador: Optional[Expressao], tipo: Tipo) -> None:
       self.nome = nome
       self.inicializador = inicializador
       self.tipo = tipo
       
    def __repr__(self):
        inicializador_repr = self.inicializador.to_str() if self.inicializador else 'None'
        return f"Var(nome={repr(self.nome)}, inicializador={inicializador_repr}, tipo={repr(self.tipo)})"
       
class While(Declaracao):
    def __init__(self, condicao: Expressao, corpo: Optional[Declaracao]) -> None:
        self.condicao = condicao
        self.corpo = corpo
        
    def __repr__(self):
        corpo_repr = repr(self.corpo) if self.corpo else 'None'
        return f"While(condicao={self.condicao.to_str()}, corpo={corpo_repr})"