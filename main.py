from lexer.lex import *
from arvores_sintaticas.expressao import *

def le_arq_entrada(nome_arq: str) -> str:
    try:
        with open(nome_arq, 'r') as arq:
            return arq.read()
    except FileNotFoundError:
        print("Nao foi possivel abrir o arquivo no caminho especificado.")
        exit(1)
    except IOError:
        print("Um erro aconteceu enquanto o arquivo era lido.")
        exit(1) 

if __name__ == '__main__':
    expr = Binaria(
        Unaria(Token(TokenType.MENOS, "-", 1), Literal(123)),
        Token(TokenType.ASTERISCO, "*", 1),
        Agrupamento(Literal(45.67))
    )
    
    print(expr.to_str())