from lexer.lex import Lexer
from parser.parser import Parser
from analise_semantica.validator import AnaliseSemantica, TabelaSimbolos
from arvores_sintaticas.declaracao import TipoLista, TipoPrimitivo

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

def printar_tabela_simbolos(tabela_simbolos: TabelaSimbolos) -> None:
    print("Tabela de Símbolos:")
    for nivel, escopo in enumerate(reversed(tabela_simbolos.escopos)):
        print(f"Escopo {len(tabela_simbolos.escopos) - nivel - 1}:")
        if not escopo:
            print("  (vazio)")
        else:
            for nome, tipo in escopo.items():
                tipo_str = (
                    tipo.interno.name if isinstance(tipo, TipoLista) else tipo.name
                )
                print(f"  {nome}: {tipo_str}")
        print("-" * 30)


if __name__ == '__main__':
    entrada = le_arq_entrada("teste.txt")
    
    lexer = Lexer(entrada)
    lexer.lex()
    
    parser = Parser(lexer.tokens)
    parser.parse()
        
    analisador = AnaliseSemantica()
    analisador.analisar(parser.declaracoes)

    print("Compilado com sucesso")
    print("Essa eh a tabela de simbolos ao final da execucao:")
    printar_tabela_simbolos(analisador.tabela_simbolos)