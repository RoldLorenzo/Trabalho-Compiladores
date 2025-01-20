from .lex import Lexer
from .lex_token import Token, TokenType
from .lex_error import LexError, LexErrorType

import unittest

class LexTests(unittest.TestCase):
    def teste_lex(self):
        fonte = r"""
// comentario
([{}]),-+*;/:
! != = == > >= < <= && ||
ola
"string"
123
123.5
bang miss cavalgando xerife procurado vorta deserto mocinho bandido atire BANG Miss
int float string bool lista
        """
        
        lex = Lexer(fonte)
        lex.lex()
        
        self.assertEqual(
            lex.tokens,
            [
                Token(TokenType.ABRE_PARENTESES, "(", 3),
                Token(TokenType.ABRE_COLCHETE, "[", 3),
                Token(TokenType.ABRE_CHAVE, "{", 3),
                Token(TokenType.FECHA_CHAVE, "}", 3),
                Token(TokenType.FECHA_COLCHETE, "]", 3),
                Token(TokenType.FECHA_PARENTESES, ")", 3),
                Token(TokenType.VIRGULA, ",", 3),
                Token(TokenType.MENOS, "-", 3),
                Token(TokenType.MAIS, "+", 3),
                Token(TokenType.ASTERISCO, "*", 3),
                Token(TokenType.PONTO_VIRGULA, ";", 3),
                Token(TokenType.BARRA, "/", 3),
                Token(TokenType.DOIS_PONTOS, ":", 3),
                Token(TokenType.EXCLAMACAO, "!", 4),
                Token(TokenType.DIFERENTE, "!=", 4),
                Token(TokenType.IGUAL, "=", 4),
                Token(TokenType.IGUAL_IGUAL, "==", 4),
                Token(TokenType.MAIOR, ">", 4),
                Token(TokenType.MAIOR_IGUAL, ">=", 4),
                Token(TokenType.MENOR, "<", 4),
                Token(TokenType.MENOR_IGUAL, "<=", 4),
                Token(TokenType.AND, "&&", 4),
                Token(TokenType.OR, "||", 4),
                Token(TokenType.IDENTIFICADOR, "ola", 5),
                Token(TokenType.STRING, "string", 6),
                Token(TokenType.INT, "123", 7),
                Token(TokenType.FLOAT, "123.5", 8),
                Token(TokenType.BANG, "bang", 9),
                Token(TokenType.MISS, "miss", 9),
                Token(TokenType.CAVALGANDO, "cavalgando", 9),
                Token(TokenType.XERIFE, "xerife", 9),
                Token(TokenType.PROCURADO, "procurado", 9),
                Token(TokenType.VORTA, "vorta", 9),
                Token(TokenType.DESERTO, "deserto", 9),
                Token(TokenType.MOCINHO, "mocinho", 9),
                Token(TokenType.BANDIDO, "bandido", 9),
                Token(TokenType.ATIRE, "atire", 9),
                Token(TokenType.IDENTIFICADOR, "BANG", 9),
                Token(TokenType.IDENTIFICADOR, "Miss", 9),
                Token(TokenType.INT, "int", 10),
                Token(TokenType.FLOAT, "float", 10),
                Token(TokenType.STRING, "string", 10),
                Token(TokenType.BOOL, "bool", 10),
                Token(TokenType.LISTA, "lista", 10),
                Token(TokenType.EOF, "", 11),
            ]
        )