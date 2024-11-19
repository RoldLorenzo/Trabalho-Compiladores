from lexer.lex import Lexer

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
    """ fonte = le_arq_entrada("teste.txt")
    
    lexer = Lexer(fonte)
    lexer.lex()
    
    if len(lexer.erros) > 0:
        for e in lexer.erros:
            e.report()
            
        exit(1) """