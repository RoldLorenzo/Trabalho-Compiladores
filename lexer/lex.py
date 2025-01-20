from .lex_token import TokenType, Token, PALAVRAS_RESERVADAS
from .lex_error import LexErrorType, LexError
from typing import Optional

# Classe que vai fazer a análise lexica a partir do codigo-fonte.
# Crafting Interpreters, Robert Nystrom - Cap. 4.

class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.ocorreu_erro: bool = False
        self.linha = 1
        self.posicao = 0
        self.inicio = 0
    
    # Gera uma lista de tokens e de erros lexicos a partir do codigo-fonte.
    def lex(self) -> None :
        while not self.fim_codigo():
            self.inicio = self.posicao
            self.lex_token()

        if self.ocorreu_erro:
            exit(1)

        self.tokens.append(Token(TokenType.EOF, "", self.linha))

    # Caso o proximo lexema seja um token valido, o adiciona na lista de tokens.
    # Caso contrario, adiciona um erro lexico na lista de erros.
    def lex_token(self) -> None:
        c = self.avanca()

        match c:
            case '(':
                self.add_token(TokenType.ABRE_PARENTESES)
            case ')':
                self.add_token(TokenType.FECHA_PARENTESES)
            case '[':
                self.add_token(TokenType.ABRE_COLCHETE)
            case ']':
                self.add_token(TokenType.FECHA_COLCHETE)
            case '{':
                self.add_token(TokenType.ABRE_CHAVE)
            case '}':
                self.add_token(TokenType.FECHA_CHAVE)
            case ',':
                self.add_token(TokenType.VIRGULA)
            case '-':
                self.add_token(TokenType.MENOS)
            case '+':
                self.add_token(TokenType.MAIS)
            case '*':
                self.add_token(TokenType.ASTERISCO)
            case ';':
                self.add_token(TokenType.PONTO_VIRGULA)
            case ':':
                self.add_token(TokenType.DOIS_PONTOS)
                
            case '/':
                # Ignorando a linha comentada
                if self.match('/'):
                    self.ignora_linha()
                else:
                    self.add_token(TokenType.BARRA)
            case '!':
                self.add_token(TokenType.DIFERENTE if self.match('=') else TokenType.EXCLAMACAO)
            case '<':
                self.add_token(TokenType.MENOR_IGUAL if self.match('=') else TokenType.MENOR)
            case '>':
                self.add_token(TokenType.MAIOR_IGUAL if self.match('=') else TokenType.MAIOR)
            case '=':
                self.add_token(TokenType.IGUAL_IGUAL if self.match('=') else TokenType.IGUAL)
            
            case '&':
                if self.match('&'):
                    self.add_token(TokenType.AND)
                else:
                    self.add_error(LexErrorType.E_INESPERADO)
            case '|':
                if self.match('|'):
                    self.add_token(TokenType.OR)
                else:
                    self.add_error(LexErrorType.OU_INESPERADO)
                
            case '"':
                self.lex_string()
                
            case c if c.isdigit():
                self.lex_numero()
                
            case c if c.isalnum():
                self.lex_palavra()

            case '\n':
                self.linha += 1

            # Ignorando whitespace
            case ' ' | '\r' | '\t':
                pass

            case _:
                self.consome_seq_caracteres()
                
                self.add_error(LexErrorType.TOKEN_INESPERADO, self.source[self.inicio : self.posicao])

    # Consome uma string (o primeiro caracter '"' ja foi consumido) e
    # adiciona o token da string caso seja válida.
    # Se a string nao foi fechada, adiciona um erro a lista de erros.
    def lex_string(self) -> None:
        linha_inicio_string = self.linha
        
        while self.peek() != '"' and not self.fim_codigo():
            if self.peek() == '\n': self.linha += 1
            
            self.avanca()
        
        if self.fim_codigo():
            self.add_error(LexErrorType.STRING_INTERMINADA, linha = linha_inicio_string)
            return
        
        self.avanca()
        
        # Tirando as aspas inicial e final do lexema
        self.add_token(TokenType.STRING, self.source[self.inicio + 1 : self.posicao - 1])
    
    # Consome um numero, caso ele tenha um '.',
    # adiciona o token como float, adiciona como int caso contrario.
    #
    # Exemplos:
    # "123" -> Token(INT, "123", linha = 1)
    # "123.5" -> Token(FLOAT, "123.5", linha = 1)
    def lex_numero(self) -> None:  
        self.consome_seq_digitos()
            
        if self.peek() == '.' and self.peekNext().isdigit():
            # Consumindo o '.'
            self.avanca()
            
            # Consumindo os numeros depois do '.'
            self.consome_seq_digitos()
            
            self.add_token(TokenType.FLOAT)
            return
        
        self.add_token(TokenType.INT)
    
    def is_whitespace(self, string: str) -> bool:
        return (
            string == " " or
            string == "\n" or
            string == "\r" or
            string == "\t"
        )
    
    # Consome caracteres do codigo-fonte ate encontrar um espaco,
    # quebra de linha ou fim do codigo.
    def consome_seq_caracteres(self) -> None:
        while not self.fim_codigo() and not self.is_whitespace(self.peek()):
            self.avanca()
    
    # Consome um identificador ou palavra reservada e
    # adiciona o token correspondente.
    def lex_palavra(self) -> None:
        while self.peek().isalnum():
            self.avanca()
        
        lexema = self.source[self.inicio : self.posicao]
        
        # Verifica se eh uma palavra reservada.
        tipo_token = (PALAVRAS_RESERVADAS[lexema] 
                      if lexema in PALAVRAS_RESERVADAS 
                      else TokenType.IDENTIFICADOR)
        
        self.add_token(tipo_token)
    
    # Consome caracteres do codigo-fonte enquanto eles
    # forem numericos
    def consome_seq_digitos(self) -> None:
        while self.peek().isdigit():
            self.avanca()

    # Adiciona um token na lista de tokens.
    # Caso lexema seja None, o lexema do token sera
    # cortado do codigo-fonte entre self.inicio e self.posicao
    def add_token(self, tipo: TokenType, lexema: Optional[str] = None) -> None:        
        if lexema is None:
            lexema = self.source[self.inicio : self.posicao]

        self.tokens.append(Token(tipo, lexema, self.linha))

    def add_error(self, tipo: LexErrorType, lexema: Optional[str] = None, linha: Optional[int] = None):
        if linha is None:
            linha = self.linha
                        
        erro = LexError(tipo, lexema, linha)
        erro.report()
        
        self.ocorreu_erro = True

    # Consome um caracter do codigo-fonte e o retorna.
    def avanca(self) -> str:
        self.posicao += 1
        return self.source[self.posicao - 1]
    
    # Retorna o caracter que esta no codigo-fonte em self.posicao
    # (sem consumi-lo).
    def peek(self) -> str:
        if self.fim_codigo(): return '\0'
        return self.source[self.posicao]
    
    # Retorna o caracter que esta no codigo-fonte na proxima posicao
    # (sem consumi-lo).
    def peekNext(self) -> str:
        if self.posicao + 1 >= len(self.source): return '\0'
        return self.source[self.posicao + 1]

    # Verifica se o proximo caracter eh o esperado,
    # se for, o consome e retorna True.
    # Caso contrario, retorna False e nao o consome.
    def match(self, esperado: str) -> bool:
        if self.fim_codigo() or self.peek() != esperado:
            return False
        
        self.posicao += 1
        return True

    # Consome caracteres ate que a linha acabe.
    def ignora_linha(self) -> None:
        while self.peek() != '\n' and not self.fim_codigo():
            self.avanca()

    # Retorna True se a posicao atual chegou no fim do
    # codigo-fonte.
    def fim_codigo(self) -> bool:
        return self.posicao >= len(self.source)