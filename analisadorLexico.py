import sys
import re

class AnalisadorLexico:
    ATOMOS = { # Dicionário que mapeia palavras-chave e símbolos especiais para códigos de átomos
        "cadeia": "A01", "caracter": "A02", "declaracoes": "A03", "enquanto": "A04",
        "false": "A05", "fimDeclaracoes": "A06", "fimEnquanto": "A07", "fimFunc": "A08",
        "fimFuncoes": "A09", "fimPrograma": "A10", "fimSe": "A11", "funcoes": "A12",
        "imprime": "A13", "inteiro": "A14", "logico": "A15", "pausa": "A16", "programa": "A17",
        "real": "A18", "retorna": "A19", "se": "A20", "senao": "A21", "tipoFunc": "A22",
        "tipoParam": "A23", "tipoVar": "A24", "true": "A25", "vazio": "A26",
        "%": "B01", "(": "B02", ")": "B03", ",": "B04", ":": "B05", ":=": "B06",
        ";": "B07", "?": "B08", "[": "B09", "]": "B10", "{": "B11", "}": "B12",
        "-": "B13", "*": "B14", "/": "B15", "+": "B16", "!=": "B17", "#": "B17",
        "<": "B18", "<=": "B19", "==": "B20", ">": "B21", ">=":"B22",
        "consCadeia": "C01", "consCaracter": "C02", "consInteiro": "C03", "consReal": "C04",
        "nomFuncao": "C05", "nomPrograma": "C06", "variavel": "C07",
    }

    RESERVADAS = {k.upper(): v for k, v in ATOMOS.items()}  # Mapeamento de palavras reservadas em maiúsculas

    # Inicializa o analisador léxico, carregando o arquivo, inicializa algumas variáveis
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo

        self.valid_symbols = {'"', "'", '(', ')', ',', ':', ';', '[', ']', '{', '}', '-', '*', '/', '+', '!', '#', '<', '=', '>', '%', '?', '_', '$'}
        self.posicao = 0
        self.buffer = ''
        self.simbolos = []
        self.tabela_simbolos = {}
        self.carregar_arquivo()
        self.linha = 1
        self.coluna = 0
        self.linhas_originais = self.buffer.splitlines()
        # Divide o texto do arquivo em linhas para uso posterior

    # Carrega o conteúdo do arquivo, converte para maiúsculas e remove comentários
    def carregar_arquivo(self):
        try:
            with open(self.nome_arquivo, 'r') as arquivo:
                self.buffer = self.filtrar_comentarios(arquivo.read().upper())  # Converte todo o conteúdo para maiúsculas e filtra comentários
        except FileNotFoundError:
            print(f"Erro: O arquivo '{self.nome_arquivo}' não foi encontrado.")
            sys.exit(1)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            sys.exit(1)

    # Gera os relatórios léxico e de tabela de símbolos
    def gerar_relatorios(self):
        self.gerar_relatorio_lexico()
        self.gerar_relatorio_tabela_simbolos()

    # Gera o relatório léxico, escrevendo as informações em um arquivo .LEX
    def gerar_relatorio_lexico(self):
        with open(self.nome_arquivo + '.LEX', 'w') as lex_file:
            lex_file.write("Codigo da Equipe: 04\n")
            lex_file.write("Componentes:\n")
            lex_file.write("    Amanda Bandeira Aragao Rigaud Lima; amanda.lima@aln.senaicimatec.edu.br; (71)99142-8451\n")
            lex_file.write("    Jorge Ricarte Passos Goncalves; jorge.goncalves@aln.senaicimatec.edu.br; (71)99966-5608\n")
            lex_file.write("    Matheus Freitas Pereira; matheus.pereira@aln.senaicimatec.edu.br; (71)99267-9326\n")
            lex_file.write("    Eduardo de Araujo Rodrigues; eduardo.rodrigues@aln.senaicimatec.edu.br; (71)99166-1915\n\n")
            lex_file.write(f"RELATORIO DA ANALISE LEXICA. Texto fonte analisado: {self.nome_arquivo}.\n\n")

            for simbolo in self.simbolos:
                lex_file.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n")
                lex_file.write(f'Lexeme: {simbolo["token"]}, Codigo: {simbolo["codigo"]}, IndiceTabSimb: {simbolo["indice"]}, Linha: {simbolo["linha"]}.\n')

    # Gera o relatório da tabela de símbolos, escrevendo as informações em um arquivo .TAB
    def gerar_relatorio_tabela_simbolos(self):
        with open(self.nome_arquivo + '.TAB', 'w') as tab_file:
            tab_file.write("Codigo da Equipe: 04\n")
            tab_file.write("Componentes:\n")
            tab_file.write("    Amanda Bandeira Aragao Rigaud Lima; amanda.lima@aln.senaicimatec.edu.br; (71)99142-8451\n")
            tab_file.write("    Jorge Ricarte Passos Goncalves; jorge.goncalves@aln.senaicimatec.edu.br; (71)99966-5608\n")
            tab_file.write("    Matheus Freitas Pereira; matheus.pereira@aln.senaicimatec.edu.br; (71)99267-9326\n")
            tab_file.write("    Eduardo de Araujo Rodrigues; eduardo.rodrigues@aln.senaicimatec.edu.br; (71)99166-1915\n\n")
            tab_file.write(f"RELATORIO DA TABELA DE SIMBOLOS. Texto fonte analisado: {self.nome_arquivo}.\n\n")

            for indice, (lexeme, info) in enumerate(self.tabela_simbolos.items(), start=1):
                linhas = ', '.join(map(str, sorted(info['linhas'])[:5]))  # Limitar a 5 primeiras linhas
                tab_file.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n")
                tab_file.write(f"Entrada: {indice}, Codigo: {info['codigo']}, Lexeme: {lexeme},\n")
                tab_file.write(f"QtdCharAntesTrunc: {info['qtd_char_antes']}, QtdCharDepoisTrunc: {info['qtd_char_depois']},\n")
                tab_file.write(f"TipoSimb: {info['tipo_simb']}, Linhas: {{{linhas}}}.\n\n")

    def filtrar_comentarios(self, texto):
        # Substitui comentários de bloco por espaços em branco, preservando quebras de linha
        while True:
            bloco_comentario_inicio = texto.find('/*')
            bloco_comentario_fim = texto.find('*/', bloco_comentario_inicio + 2)
            if bloco_comentario_inicio == -1:
                break
            if bloco_comentario_fim == -1:
                # Se não houver fechamento do comentário de bloco, consideramos tudo até o fim do arquivo como comentário
                bloco_comentario_fim = len(texto)
            comentario_bloco = texto[bloco_comentario_inicio:bloco_comentario_fim + 2]
            texto = texto.replace(comentario_bloco, ' ' * len(comentario_bloco), 1)

        # Substitui comentários de linha por espaços em branco, preservando quebras de linha
        texto = re.sub(r'//.*', lambda m: ' ' * (len(m.group(0))), texto)
        return texto
    
    def reconhecerTokens(self):
        # Loop enquanto a posição atual for menor que o comprimento do buffer (texto do arquivo)
        while self.posicao < len(self.buffer):
            # Ignora espaços em branco
            if self.is_whitespace(self.buffer[self.posicao]):
                self.avancar_posicao()
                continue

            # Ignora caracteres inválidos
            if not self.is_valid_char(self.buffer[self.posicao]):
                self.avancar_posicao()
                continue

            # Verifica se o caractere atual é uma aspas dupla (")
            if self.buffer[self.posicao] == '"':
                # Reconhece uma cadeia (string) e classifica como tal
                token_info = self.reconhecer_cadeia()

            # Verifica se o caractere atual é uma aspas simples (')
            elif self.buffer[self.posicao] == "'":
                # Reconhece um caractere e classifica como tal
                token_info = self.reconhecer_caracter()

            # Verifica se o caractere atual é uma letra
            elif self.is_letter(self.buffer[self.posicao]):
                # Reconhece um nome (possivelmente uma palavra reservada) e classifica
                token_info = self.reconhecer_nome()
                token_info["codigo"] = "C07"  # Define o código correspondente
                token_info["tipo"] = "VOI"  # Determina o tipo do símbolo

            # Verifica se o caractere atual é um dígito
            elif self.is_digit(self.buffer[self.posicao]):
                # Tenta reconhecer um número inteiro, caso encontre "." tenta reconhecer um numero real
                token_info = self.reconhecer_numero()  # Reconhece um número inteiro
                    

            else:
                # Ignora outros caracteres e avança para o próximo
                self.avancar_posicao()
                continue

            # Obtém informações sobre o lexema atual
            lexeme = token_info["token"]

            # Obtém o índice do símbolo na tabela de símbolos ou adiciona um novo
            token_info["indice"] = self.obter_indice_simbolo(lexeme) or len(self.tabela_simbolos) + 1
            self.simbolos.append(token_info)  # Adiciona as informações do símbolo à lista de símbolos

            if token_info["token"].upper() not in self.RESERVADAS:
                # Adiciona ou atualiza informações sobre o lexema na tabela de símbolos
                if lexeme not in self.tabela_simbolos:
                    self.tabela_simbolos[lexeme] = {
                        "codigo": token_info["codigo"],
                        "qtd_char_antes":  token_info["qtd_char_antes"],
                        "qtd_char_depois":  token_info["qtd_char_depois"],
                        "tipo_simb": token_info["tipo"],
                        "linhas": {token_info["linha"]}  # Armazena as linhas onde o lexema ocorre
                    }
                else:
                    # Se o lexema já existe na tabela, apenas atualiza as informações das linhas
                    self.tabela_simbolos[lexeme]["linhas"].add(token_info["linha"])

    def obter_indice_simbolo(self, lexeme):
        # Obtém o índice do símbolo na tabela de símbolos
        for indice, (simbolo, _) in enumerate(self.tabela_simbolos.items(), start=1):
            if simbolo == lexeme:
                return indice  # Retorna o índice se o lexema já estiver na tabela de símbolos
        return None  # Retorna None se o lexema não estiver na tabela de símbolos

    def is_whitespace(self, char):
        # Verifica se o caractere é um espaço em branco
        return char in {' ', '\t', '\n', '\r'}

    def is_letter(self, char):
        # Verifica se o caractere é uma letra
        return 'A' <= char <= 'Z'

    def is_digit(self, char):
        # Verifica se o caractere é um dígito
        return '0' <= char <= '9'

    def is_valid_char(self, char):
        # Verifica se o caractere é válido para um símbolo léxico
        return self.is_letter(char) or self.is_digit(char) or self.is_whitespace(char) or char in self.valid_symbols

    def avancar_posicao(self):
        # Avança a posição atual no buffer de texto
        if self.posicao < len(self.buffer):
            if self.buffer[self.posicao] == '\n':
                self.linha += 1  # Incrementa o número da linha ao encontrar uma quebra de linha
                self.coluna = 0
            else:
                self.coluna += 1  # Incrementa o número da coluna
            self.posicao += 1  # Avança para o próximo caractere no buffer de texto

    def reconhecer_nome(self):
        # Reconhece um nome (identificador) no texto
        inicio = self.posicao
        coluna_inicio = self.coluna  # Guarda a coluna inicial do nome
        nome = []

        # Loop para reconhecer o nome até encontrar um caractere inválido
        while self.posicao < len(self.buffer) and (self.is_letter(self.buffer[self.posicao]) or self.is_digit(self.buffer[self.posicao]) or not self.is_valid_char(self.buffer[self.posicao])):
            if self.is_valid_char(self.buffer[self.posicao]):
                nome.append(self.buffer[self.posicao])
            self.avancar_posicao()  # Avança para o próximo caractere

        # Considera as aspas duplas na contagem de caracteres
        qtd_char = self.posicao - inicio
        qtd_char_depois = min(qtd_char, 30)  # Limita a 30 caracteres
        qtd_char_antes = max(qtd_char, qtd_char_depois)

        nome = ''.join(nome)[:30]  # Limita o nome a 30 caracteres
        return {"token": nome, 
                "linha": self.linha, 
                "coluna": coluna_inicio, 
                "codigo": "C07",  # Retorna o número com informações adicionais (linha, coluna, código)
                "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes de truncar
                "qtd_char_depois": qtd_char_depois}  # Retorna a cadeia com informações adicionais (linha, coluna, código, quantidade de caracteres)


    def reconhecer_numero(self):
        # Reconhece um número inteiro no texto
        inicio = self.posicao
        coluna_inicio = self.coluna
        ponto_encontrado = False  # Flag para indicar se um ponto foi encontrado

        # Loop para reconhecer o número até encontrar um caractere não numérico
        while self.posicao < len(self.buffer):
            char = self.buffer[self.posicao]

            if self.is_digit(char):
                self.avancar_posicao()  # Avança para o próximo caractere
            elif char == '.' and not ponto_encontrado:
                ponto_encontrado = True
                self.avancar_posicao()  # Avança para o próximo caractere
                # Começa a procurar um número real
                return self.reconhecer_real(inicio, coluna_inicio)
            else:
                break  # Se encontrar um caractere inválido, sai do loop

        # Considera as aspas duplas na contagem de caracteres
        qtd_char = self.posicao - inicio
        qtd_char_depois = min(qtd_char, 30)  # Limita a 30 caracteres
        qtd_char_antes = max(qtd_char, qtd_char_depois)
        
        numero = self.buffer[inicio:self.posicao][:30]  # Obtém o número reconhecido
        
        return {"token": numero, 
                "linha": self.linha, 
                "coluna": coluna_inicio, 
                "tipo": "INT",
                "codigo": "C03",  # Retorna o número com informações adicionais (linha, coluna, código)
                "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes de truncar
                "qtd_char_depois": qtd_char_depois}  # Retorna a cadeia com informações adicionais (linha, coluna, código, quantidade de caracteres)
        
    def reconhecer_cadeia(self):
        # Reconhece uma cadeia (string) delimitada por aspas duplas no texto
        inicio = self.posicao
        coluna_inicio = self.coluna
        self.avancar_posicao()  # Pula o primeiro caractere de aspas duplas

        # Loop para reconhecer a cadeia até encontrar o próximo caractere de aspas duplas
        while self.posicao < len(self.buffer) and self.buffer[self.posicao] != '"':
            self.avancar_posicao()  # Avança para o próximo caractere

        self.avancar_posicao()  # Pulka o char de aspas duplas

        # Considera as aspas duplas na contagem de caracteres
        qtd_char = self.posicao - inicio
        qtd_char_depois = min(qtd_char, 30)  # Limita a 30 caracteres
        qtd_char_antes = max(qtd_char, qtd_char_depois)

        if(qtd_char > 30):
            # Obtém a cadeia limitada a 28 caracteres entre as aspas
            cadeia = self.buffer[inicio:self.posicao][:29] + '"'
        else:
            # Obtém a cadeia limitada a 28 caracteres entre as aspas
            cadeia = self.buffer[inicio:self.posicao][:qtd_char_depois]

        return {"token": cadeia, 
                "linha": self.linha, 
                "coluna": coluna_inicio, 
                "codigo": "C01",  # Define o código para cadeia
                "tipo" : "STR",
                "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes de truncar
                "qtd_char_depois": qtd_char_depois}  # Retorna a cadeia com informações adicionais (linha, coluna, código, quantidade de caracteres)

    def reconhecer_caracter(self):
        # Reconhece um caractere delimitado por aspas simples no texto
        self.avancar_posicao()  # Pula o primeiro caractere de aspas simples

        if self.posicao < len(self.buffer):
            caracter = "'" + self.buffer[self.posicao] + "'"  # Adiciona as aspas simples ao redor do caractere
            self.avancar_posicao()  # Pula o caractere reconhecido
    
            if self.posicao < len(self.buffer) and self.buffer[self.posicao] == "'":
                self.avancar_posicao()  # Pula o último caractere de aspas simples
                return {"token": caracter, 
                        "linha": self.linha, 
                        "coluna": self.coluna - 1, 
                        "codigo": "C02",  # Define o código para cadeia
                        "tipo" : "CHC",
                        "qtd_char_antes": len(caracter),  # Quantidade de caracteres antes de truncar
                        "qtd_char_depois": len(caracter)}
            
        return None  # Retorna None se não for possível reconhecer um caractere válido
    
    def reconhecer_real(self, inicio, coluna_inicio):
        # Reconhece um número real (com ponto flutuante) no texto
        expoente_encontrado = False
        pos_expoente = -1

        while self.posicao < len(self.buffer):
            char = self.buffer[self.posicao]

            if self.is_digit(char):
                self.avancar_posicao()  # Avança para o próximo caractere
            elif char in ('e', 'E') and not expoente_encontrado:
                expoente_encontrado = True
                self.avancar_posicao()  # Avança para o próximo caractere
                if self.posicao < len(self.buffer) and self.buffer[self.posicao] in ('+', '-'):
                    self.avancar_posicao()  # Avança para o próximo caractere
            else:
                break  # Se encontrar um caractere inválido, sai do loop


        # Considera as aspas duplas na contagem de caracteres
        qtd_char = self.posicao - inicio
        qtd_char_depois = min(qtd_char, 30)  # Limita a 30 caracteres
        qtd_char_antes = max(qtd_char, qtd_char_depois)

        if(qtd_char > 30):
            token = self.buffer[inicio:self.posicao][:30]
            if '.' in token:
                tipo_simb = "PFO"  # Define o tipo do símbolo como número real
                codigo = "C04"  # Define o código para número real
            else:
                tipo_simb = "INT"  # Define o tipo do símbolo como número inteiro
                codigo = "C03"  # Define o código para número inteiro

            # analise do token
        else:
            token = self.buffer[inicio:self.posicao][:qtd_char_depois]  # Obtém o número reconhecido
            tipo_simb = "PFO"  # Define o tipo do símbolo como número real
            codigo = "C04"  # Define o código para número real

        return {"token": token, 
                "linha": self.linha,  
                "codigo": codigo,
                "tipo": tipo_simb,
                "coluna": self.coluna - len(token),
                "qtd_char_antes": qtd_char_antes,  
                "qtd_char_depois": qtd_char_depois}
