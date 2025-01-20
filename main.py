from lexer.lex import Lexer
from parser.parser import Parser

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
    entrada = le_arq_entrada("teste.txt")
    
    lexer = Lexer(entrada)
    lexer.lex()
    
    parser = Parser(lexer.tokens)
    parser.parse()
        
    print("Lista de declaracoes: ")
    for decl in parser.declaracoes:
        print(decl)
        print()
    print("---------")