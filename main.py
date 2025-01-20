from lexer.lex import Lexer
from parser.parser import Parser
from analise_semantica.validator import AnaliseSemantica

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
        
    analisador = AnaliseSemantica()
    analisador.analisar(parser.declaracoes)
    print(parser.declaracoes)
    print(analisador.tabela_simbolos)