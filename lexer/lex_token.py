from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # Tokens de um caracter
    ABRE_PARENTESES = auto()
    FECHA_PARENTESES = auto()
    ABRE_COLCHETE = auto()
    FECHA_COLCHETE = auto()
    ABRE_CHAVE = auto()
    FECHA_CHAVE = auto()
    VIRGULA = auto()
    PONTO = auto()
    MENOS = auto()
    MAIS = auto()
    ASTERISCO = auto()
    PONTO_VIRGULA = auto()
    BARRA = auto()

    # Tokens que podem ter mais de um caracter
    EXCLAMACAO = auto()
    DIFERENTE = auto()
    IGUAL = auto()
    IGUAL_IGUAL = auto()
    MAIOR = auto()
    MAIOR_IGUAL = auto()
    MENOR = auto()
    MENOR_IGUAL = auto()
    AND = auto()
    OR = auto()

    # Literais
    IDENTIFICADOR = auto()
    STRING = auto()
    INT = auto()
    FLOAT = auto()

    # Palavras reservadas
    BANG = auto() # if
    MISS = auto() # else
    CAVALGANDO = auto() # while
    XERIFE = auto() # let
    PROCURADO = auto() # fn
    VORTA = auto() # return
    DESERTO = auto() # NULL
    MOCINHO = auto() # True
    BANDIDO = auto() # False
    ATIRE = auto() # print

    # Fim do arquivo
    EOF = auto()

PALAVRAS_RESERVADAS = {
    'bang': TokenType.BANG,
    'miss': TokenType.MISS,
    'cavalgando': TokenType.CAVALGANDO,
    'xerife': TokenType.XERIFE,
    'procurado': TokenType.PROCURADO,
    'vorta': TokenType.VORTA,
    'deserto': TokenType.DESERTO,
    'mocinho': TokenType.MOCINHO,
    'bandido': TokenType.BANDIDO,
    'atire': TokenType.ATIRE,
}

@dataclass(repr=True, eq=True)
class Token:
    tipo: TokenType
    lexema: str
    linha: int