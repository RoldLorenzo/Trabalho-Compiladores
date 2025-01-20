from arvores_sintaticas.declaracao import *
from arvores_sintaticas.expressao import *
from lexer.lex_token import TokenType

class TabelaSimbolos:
    def __init__(self):
        self.escopos = [{}]  # Uma pilha de dicionários.
    
    def inserir(self, nome: str, tipo: Tipo):
        if nome in self.escopos[-1]:
            raise Exception(f"Erro: Variável '{nome}' já declarada neste escopo.")
        self.escopos[-1][nome] = tipo

    def buscar(self, nome: str) -> Tipo:
        for escopo in reversed(self.escopos):
            if nome in escopo:
                return escopo[nome]
        raise Exception(f"Erro: Variável '{nome}' não declarada.")

    def novo_escopo(self):
        self.escopos.append({})

    def remover_escopo(self):
        self.escopos.pop()

class AnaliseSemantica:
    def __init__(self):
        self.tabela_simbolos = TabelaSimbolos()
        self.tipo_retorno_atual = None

    def analisar(self, declaracoes: list[Declaracao]):
        for declaracao in declaracoes:
            #try:
            self.visitar_declaracao(declaracao)
            """ except Exception as e:
                print("\033[91mErro na analise semantica:\033[0m")
                print(e)
                exit(1) """

    def visitar_declaracao(self, declaracao: Declaracao):
        if isinstance(declaracao, Var):
            self.visitar_var(declaracao)
        elif isinstance(declaracao, Funcao):
            self.visitar_funcao(declaracao)
        elif isinstance(declaracao, Bloco):
            self.visitar_bloco(declaracao)
        elif isinstance(declaracao, If):
            self.visitar_if(declaracao)
        elif isinstance(declaracao, While):
            self.visitar_while(declaracao)
        elif isinstance(declaracao, Return):
            self.visitar_return(declaracao)
        elif isinstance(declaracao, Print):
            self.visitar_print(declaracao)
        elif isinstance(declaracao, Expr):
            self.visitar_expressao(declaracao.expressao)
        else:
            raise Exception(f"Tipo de declaracao desconhecido: {type(declaracao)}")

    def visitar_var(self, var: Var):
        # Verificar o tipo do inicializador.
        if var.inicializador:
            tipo_inicializador = self.visitar_expressao(var.inicializador)
            
            if tipo_inicializador != var.tipo:
                raise Exception(f"Erro: Tipo incompatível na declaração da variável '{var.nome.lexema}'. "
                                f"Esperado: {var.tipo}, encontrado: {tipo_inicializador}")
        self.tabela_simbolos.inserir(var.nome.lexema, var.tipo)

    def visitar_funcao(self, funcao: Funcao):
        self.tabela_simbolos.inserir(funcao.nome.lexema, funcao.tipo_retorno)
        self.tabela_simbolos.novo_escopo()

        # Definir o tipo de retorno atual
        tipo_retorno_anterior = self.tipo_retorno_atual
        self.tipo_retorno_atual = funcao.tipo_retorno

        for parametro in funcao.params:
            self.tabela_simbolos.inserir(parametro.nome.lexema, parametro.tipo)
        for declaracao in funcao.corpo:
            self.visitar_declaracao(declaracao)

        # Restaurar o tipo de retorno ao final
        self.tipo_retorno_atual = tipo_retorno_anterior
        self.tabela_simbolos.remover_escopo()
        
    def visitar_bloco(self, bloco: Bloco):
        self.tabela_simbolos.novo_escopo()
        for declaracao in bloco.statements:
            self.visitar_declaracao(declaracao)
        self.tabela_simbolos.remover_escopo()

    def visitar_if(self, if_stmt: If):
        tipo_condicao = self.visitar_expressao(if_stmt.condicao)
        if tipo_condicao != TipoPrimitivo.BOOL:
            raise Exception("Erro: A condição de um 'if' deve ser do tipo BOOL.")
        self.visitar_declaracao(if_stmt.then_branch)
        if if_stmt.else_branch:
            self.visitar_declaracao(if_stmt.else_branch)

    def visitar_while(self, while_stmt: While):
        tipo_condicao = self.visitar_expressao(while_stmt.condicao)
        if tipo_condicao != TipoPrimitivo.BOOL:
            raise Exception("Erro: A condição de um 'while' deve ser do tipo BOOL.")
        
        if while_stmt.corpo is not None:
            self.visitar_declaracao(while_stmt.corpo)

    def visitar_return(self, retorno: Return):
        assert self.tipo_retorno_atual is not None
        
        if retorno.valor:
            # Obter o tipo da expressão retornada
            tipo_valor = self.visitar_expressao(retorno.valor)
            
            # Verificar compatibilidade
            if tipo_valor != self.tipo_retorno_atual:
                raise Exception(
                    f"Erro: Tipo de retorno incompatível. Esperado: {self.tipo_retorno_atual}, encontrado: {tipo_valor}."
                )
        else:
            # Caso seja um 'return;' sem valor, o tipo esperado deve ser NULL
            if self.tipo_retorno_atual != TipoPrimitivo.NULL:
                raise Exception(
                    "Erro: Retorno vazio em uma função que espera um valor."
                )

    def visitar_print(self, print_stmt: Print):
        self.visitar_expressao(print_stmt.expressao)

    def visitar_expressao(self, expressao: Expressao) -> Tipo:
        if isinstance(expressao, Literal):
            return self.visitar_literal(expressao)
        elif isinstance(expressao, Variavel):
            return self.visitar_variavel(expressao)
        elif isinstance(expressao, Binaria):
            return self.visitar_binaria(expressao)
        elif isinstance(expressao, Unaria):
            return self.visitar_unaria(expressao)
        elif isinstance(expressao, Logica):
            return self.visitar_logica(expressao)
        elif isinstance(expressao, Lista):
            return self.visitar_lista(expressao)
        elif isinstance(expressao, Agrupamento):
            return self.visitar_agrupamento(expressao)
        elif isinstance(expressao, Atribuicao):
            return self.visitar_atribuicao(expressao)
        elif isinstance(expressao, Chamada):
            return self.visitar_chamada(expressao)
        else:
            raise Exception(f"Expressão desconhecida: {type(expressao).__name__}")

    def visitar_literal(self, literal: Literal) -> Tipo:
        # Retorna o tipo literal correspondente
        if literal.tipo == TokenType.INT:
            return TipoPrimitivo.INT
        elif literal.tipo == TokenType.FLOAT:
            return TipoPrimitivo.FLOAT
        elif literal.tipo == TokenType.STRING:
            return TipoPrimitivo.STRING
        elif literal.tipo == TokenType.BOOL:
            return TipoPrimitivo.BOOL
        elif literal.tipo == TokenType.DESERTO:
            return TipoPrimitivo.NULL
        else:
            raise Exception(f"Tipo literal desconhecido: {literal.tipo}")

    def visitar_variavel(self, variavel: Variavel) -> Tipo:
        # Busca o tipo da variável na tabela de símbolos
        tipo = self.tabela_simbolos.buscar(variavel.nome.lexema)
        if tipo is None:
            raise Exception(f"Erro: Variável '{variavel.nome.lexema}' não declarada.")
        return tipo

    def visitar_binaria(self, binaria: Binaria) -> Tipo:
        tipo_esquerda = self.visitar_expressao(binaria.esquerda)
        tipo_direita = self.visitar_expressao(binaria.direita)
        
        if tipo_esquerda != tipo_direita:
            raise Exception(f"Erro: Tipos incompatíveis na operação binária: {tipo_esquerda} e {tipo_direita}.")
        
        # Exemplo simplificado: as operações aritméticas retornam o mesmo tipo
        if binaria.operador.tipo in {TokenType.MAIS, TokenType.MENOS, TokenType.ASTERISCO, TokenType.BARRA}:
            if tipo_esquerda not in {TipoPrimitivo.INT, TipoPrimitivo.FLOAT}:
                raise Exception(f"Erro: Operação inválida para tipo {tipo_esquerda}.")
            return TipoPrimitivo.FLOAT
        
        # Operações lógicas retornam BOOL
        if binaria.operador.tipo in {
                TokenType.AND,
                TokenType.OR,
            }:
            if tipo_esquerda != TipoPrimitivo.BOOL:
                raise Exception("Erro: Operação lógica requer operandos do tipo BOOL.")
            return TipoPrimitivo.BOOL
        
        if binaria.operador.tipo in {
            TokenType.MENOR,
            TokenType.MENOR_IGUAL,
            TokenType.MAIOR, 
            TokenType.MAIOR_IGUAL, 
            TokenType.DIFERENTE, 
            TokenType.IGUAL_IGUAL
        }: 
            if tipo_esquerda != TipoPrimitivo.INT and tipo_esquerda != TipoPrimitivo.FLOAT:
                raise Exception("Erro: Comparacoes requerem operandos numericos.")
            return TipoPrimitivo.BOOL
        
        raise Exception(f"Operador binário desconhecido: {binaria.operador.tipo}")

    def visitar_unaria(self, unaria: Unaria) -> Tipo:
        tipo_direita = self.visitar_expressao(unaria.direita)
        
        # Exemplo: operador '-' só é válido para números
        if unaria.operador.tipo == TokenType.MENOS:
            if tipo_direita not in {TipoPrimitivo.INT, TipoPrimitivo.FLOAT}:
                raise Exception(f"Erro: Operador '-' inválido para tipo {tipo_direita}.")
            return tipo_direita
        
        # Exemplo: operador '!' só é válido para BOOL
        if unaria.operador.tipo == TokenType.EXCLAMACAO:
            if tipo_direita != TipoPrimitivo.BOOL:
                raise Exception(f"Erro: Operador '!' inválido para tipo {tipo_direita}.")
            return TipoPrimitivo.BOOL
        
        raise Exception(f"Operador unário desconhecido: {unaria.operador.tipo}")

    def visitar_logica(self, logica: Logica) -> Tipo:
        tipo_esquerda = self.visitar_expressao(logica.esquerda)
        tipo_direita = self.visitar_expressao(logica.direita)
        
        if tipo_esquerda != TipoPrimitivo.BOOL or tipo_direita != TipoPrimitivo.BOOL:
            raise Exception("Erro: Operação lógica requer operandos do tipo BOOL.")
        
        return TipoPrimitivo.BOOL

    def visitar_lista(self, lista: Lista) -> Tipo:
        tipos_elementos = [self.visitar_expressao(elemento) for elemento in lista.valores]
        
        # Garantir que todos os elementos têm o mesmo tipo
        primeiro_tipo = tipos_elementos[0] if tipos_elementos else TipoPrimitivo.NULL
        for tipo in tipos_elementos:
            if tipo != primeiro_tipo:
                raise Exception("Erro: Lista contem elementos de tipos diferentes.")
        
        if isinstance(primeiro_tipo, TipoLista):
            raise Exception("Erro: Listas encadeadas nao sao permitidas.")
        
        return TipoLista(primeiro_tipo)

    def visitar_agrupamento(self, agrupamento: Agrupamento) -> Tipo:
        return self.visitar_expressao(agrupamento.expressao)

    def visitar_atribuicao(self, atribuicao: Atribuicao) -> Tipo:
        tipo_valor = self.visitar_expressao(atribuicao.valor)
        tipo_variavel = self.visitar_variavel(self.tabela_simbolos.buscar(atribuicao.nome))
        
        if tipo_valor != tipo_variavel:
            raise Exception(f"Erro: Atribuição incompatível. Esperado: {tipo_variavel}, encontrado: {tipo_valor}.")
        
        return tipo_variavel

    def visitar_chamada(self, chamada: Chamada) -> Tipo:
        tipo_funcao = self.visitar_expressao(chamada.chamado)
        
        # aqui, deveriam ser validados o numero e tipo dos argumentos, se a funcao existe...
        
        return tipo_funcao
