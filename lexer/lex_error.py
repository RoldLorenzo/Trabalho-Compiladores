from enum import Enum, auto
from typing import Optional

class LexErrorType(Enum):
    TOKEN_INESPERADO = auto()
    E_INESPERADO = auto()
    OU_INESPERADO = auto()
    STRING_INTERMINADA = auto()
    
class LexError:
    def __init__(self, tipo: LexErrorType, lexema: Optional[str], linha: int) -> None:
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
    
    def __eq__(self, other) -> bool:
        if isinstance(other, LexError):
            return self.tipo == other.tipo and self.lexema == other.lexema and self.linha == other.linha
        
        return False
    
    # Printa uma mensagem customizada a partir do tipo do erro
    def report(self) -> None:
        print("\033[91mErro na analise lexica:\033[0m")
        print("Linha " + str(self.linha))
        
        match self.tipo:
            case LexErrorType.STRING_INTERMINADA:
                print("Uma string foi aberta, mas nao foi fechada.")
                
            case LexErrorType.E_INESPERADO:
                print("Eu nao esperava encontrar & aqui, voce quis dizer &&?")
            case LexErrorType.OU_INESPERADO:
                print("Eu nao esperava encontrar | aqui, voce quis dizer ||?")
            
            case LexErrorType.TOKEN_INESPERADO:
                assert self.lexema is not None
                
                print("Eu nao esperava encontrar isso: " + self.lexema)
                
        print("")