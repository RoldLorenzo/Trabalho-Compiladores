from enum import Enum, auto
from typing import Optional

class LexErrorType(Enum):
    TOKEN_INESPERADO = auto()
    E_INESPERADO = auto()
    OU_INESPERADO = auto()
    STRING_INTERMINADA = auto()
    NUMERO_MAL_FORMADO = auto()
    
class LexError:
    def __init__(self, tipo: LexErrorType, lexema: Optional[str], linha: int) -> None:
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
    
    def __eq__(self, other) -> bool:
        if isinstance(other, LexError):
            return self.tipo == other.tipo and self.lexema == other.lexema and self.linha == other.linha
        
        return False
    
    def report(self) -> None:
        print("\033[91mErro lexico:\033[0m")
        print("Linha " + str(self.linha))
        
        match self.tipo:
            case LexErrorType.STRING_INTERMINADA:
                print("Uma string foi aberta, mas nao foi fechada.")
                
            case LexErrorType.E_INESPERADO:
                print("Eu nao esperava encontrar '&' aqui, voce quis dizer &&?")
            case LexErrorType.OU_INESPERADO:
                print("Eu nao esperava encontrar '|' aqui, voce quis dizer ||?")
                
            case LexErrorType.NUMERO_MAL_FORMADO:
                assert self.lexema is not None
                
                print(f"Esse numero foi mal formado: {self.lexema}")
                print(f"Dica: se isso for um nome, ele nao deve comecar com numeros!")
            
            case LexErrorType.TOKEN_INESPERADO:
                assert self.lexema is not None
                
                print("Eu nao esperava encontrar isso: " + self.lexema)
                
        print("")