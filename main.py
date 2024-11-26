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
    
    if len(lexer.erros) > 0:
        for e in lexer.erros:
            e.report()
            
        exit(1)
        
    parser = Parser(lexer.tokens)
    expr = parser.parse()
    
    print(expr.to_str())