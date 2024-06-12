import sys
import re

LIMITE_QTD_CHAR = 30

class AnalisadorLexico:
    ATOMOS = {
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

    RESERVADAS = {k.upper(): v for k, v in ATOMOS.items()}

    # Método de inicialização da classe AnalisadorLexico
    def __init__(self, nome_arquivo, analisador_sintatico):
        # Inicializa os atributos da classe
        self.nome_arquivo = nome_arquivo
        self.posicao = 0
        self.buffer = ''
        self.buffer_size = 0
        self.simbolos = []
        self.tabela_simbolos = {}
        self.carregar_arquivo()  # Chama o método para carregar o arquivo
        self.linha = 1
        self.coluna = 0
        self.linhas_originais = self.buffer.splitlines()  # Divide o texto em linhas
        self.analisador_sintatico = analisador_sintatico

    # Método para carregar o conteúdo do arquivo
    def carregar_arquivo(self):
        try:
            with open(self.nome_arquivo, 'r') as arquivo:
                self.buffer = self.filtrar_comentarios(arquivo.read().upper())  # Lê o arquivo e filtra comentários
                self.buffer_size = len(self.buffer)  # Calcula o tamanho do buffer
        except FileNotFoundError:
            print(f"Erro: O arquivo '{self.nome_arquivo}' não foi encontrado.")
            sys.exit(1)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            sys.exit(1)

    # Método para gerar relatórios léxicos e tabela de símbolos
    def gerar_relatorios(self):
        self.gerar_relatorio_lexico()  # Chama o método para gerar o relatório léxico
        self.gerar_relatorio_tabela_simbolos()  # Chama o método para gerar o relatório da tabela de símbolos

    # Método para gerar relatório léxico
    def gerar_relatorio_lexico(self):
        with open(self.nome_arquivo + '.LEX', 'w') as lex_file:
            # Escreve informações de equipe no arquivo de relatório léxico
            lex_file.write("Codigo da Equipe: 04\n")
            lex_file.write("Componentes:\n")
            lex_file.write("    Amanda Bandeira Aragao Rigaud Lima; amanda.lima@aln.senaicimatec.edu.br; (71)99142-8451\n")
            lex_file.write("    Jorge Ricarte Passos Goncalves; jorge.goncalves@aln.senaicimatec.edu.br; (71)99966-5608\n")
            lex_file.write("    Matheus Freitas Pereira; matheus.pereira@aln.senaicimatec.edu.br; (71)99267-9326\n")
            lex_file.write("    Eduardo de Araujo Rodrigues; eduardo.rodrigues@aln.senaicimatec.edu.br; (71)99166-1915\n\n")
            lex_file.write(f"RELATORIO DA ANALISE LEXICA. Texto fonte analisado: {self.nome_arquivo}.\n\n")

            # Escreve informações de tokens no arquivo de relatório léxico
            for simbolo in self.simbolos:
                lex_file.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n")
                lex_file.write(f'Lexeme: {simbolo["token"]}, Codigo: {simbolo["codigo"]}, IndiceTabSimb: {simbolo["indice"]}, Linha: {simbolo["linha"]}.\n')

    # Método para gerar relatório da tabela de símbolos
    def gerar_relatorio_tabela_simbolos(self):
        with open(self.nome_arquivo + '.TAB', 'w') as tab_file:
            # Escreve informações de equipe no arquivo de relatório da tabela de símbolos
            tab_file.write("Codigo da Equipe: 04\n")
            tab_file.write("Componentes:\n")
            tab_file.write("    Amanda Bandeira Aragao Rigaud Lima; amanda.lima@aln.senaicimatec.edu.br; (71)99142-8451\n")
            tab_file.write("    Jorge Ricarte Passos Goncalves; jorge.goncalves@aln.senaicimatec.edu.br; (71)99966-5608\n")
            tab_file.write("    Matheus Freitas Pereira; matheus.pereira@aln.senaicimatec.edu.br; (71)99267-9326\n")
            tab_file.write("    Eduardo de Araujo Rodrigues; eduardo.rodrigues@aln.senaicimatec.edu.br; (71)99166-1915\n\n")
            tab_file.write(f"RELATORIO DA TABELA DE SIMBOLOS. Texto fonte analisado: {self.nome_arquivo}.\n\n")

            # Escreve informações da tabela de símbolos no arquivo de relatório da tabela de símbolos
            for indice, (lexeme, info) in enumerate(self.tabela_simbolos.items(), start=1):
                linhas = ', '.join(map(str, sorted(info['linhas'])[:5]))
                tab_file.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n")
                tab_file.write(f"Entrada: {indice}, Codigo: {info['codigo']}, Lexeme: {lexeme},\n")
                tab_file.write(f"QtdCharAntesTrunc: {info['qtd_char_antes']}, QtdCharDepoisTrunc: {info['qtd_char_depois']},\n")
                tab_file.write(f"TipoSimb: {info['tipo_simb']}, Linhas: {{{linhas}}}.\n\n")

    # Método para filtrar comentários do texto
    def filtrar_comentarios(self, texto):
        while True:
            bloco_comentario_inicio = texto.find('/*')
            bloco_comentario_fim = texto.find('*/', bloco_comentario_inicio + 2)
            if bloco_comentario_inicio == -1:
                break
            if bloco_comentario_fim == -1:
                bloco_comentario_fim = len(texto)
            comentario_bloco = texto[bloco_comentario_inicio:bloco_comentario_fim + 2]
            texto = texto.replace(comentario_bloco, ' ' * len(comentario_bloco), 1)

        texto = re.sub(r'//.*', lambda m: ' ' * (len(m.group(0))), texto)
        return texto
    
    # Método para reconhecer tokens no texto
    def reconhecerTokens(self):
        # Percorre o texto enquanto a posição atual for menor que o tamanho do buffer
        while self.posicao < self.buffer_size:
            # Ignora espaços em branco
            if self.is_whitespace(self.buffer[self.posicao]):
                self.avancar_posicao()  # Move para a próxima posição
                continue

            # Verifica se o caractere atual é uma aspas dupla, indicando uma cadeia de caracteres
            if self.buffer[self.posicao] == '"':
                token_info = self.reconhecer_cadeia()  # Chama o método para reconhecer cadeias de caracteres
                if(token_info == -1):  # Se o retorno indicar erro, continua para o próximo caractere
                    continue
            # Verifica se o caractere atual é uma aspas simples, indicando um caractere
            elif self.buffer[self.posicao] == "'":
                token_info = self.reconhecer_caracter()  # Chama o método para reconhecer caracteres
                if(token_info == -1):  # Se o retorno indicar erro, continua para o próximo caractere
                    continue
            # Verifica se o caractere atual é uma letra
            elif self.is_letter(self.buffer[self.posicao]):
                token_info = self.reconhecer_nome()  # Chama o método para reconhecer nomes
            # Verifica se o caractere atual é um dígito
            elif self.is_digit(self.buffer[self.posicao]):
                token_info = self.reconhecer_numero()  # Chama o método para reconhecer números
            elif self.is_operador(self.buffer[self.posicao]):
                token_info = self.reconhecer_operando()
            else:
                self.avancar_posicao()  # Move para a próxima posição
                continue

            lexeme = token_info["token"]  # Obtém o lexema do token

            # Se o token não for uma palavra reservada, adiciona à tabela de símbolos
            if token_info["token"] not in self.RESERVADAS:
                # Adiciona informações sobre o token à lista de símbolos
                token_info["indice"] = self.obter_indice_simbolo(lexeme) or len(self.tabela_simbolos) + 1
                self.simbolos.append(token_info)

                if lexeme not in self.tabela_simbolos:
                    self.tabela_simbolos[lexeme] = {
                        "codigo": token_info["codigo"],
                        "qtd_char_antes":  token_info["qtd_char_antes"],
                        "qtd_char_depois":  token_info["qtd_char_depois"],
                        "tipo_simb": token_info["tipo"],
                        "linhas": {token_info["linha"]}
                    }
                else:
                    self.tabela_simbolos[lexeme]["linhas"].add(token_info["linha"])
            else:
                token_info["codigo"] = self.RESERVADAS.get(lexeme, None)
                # Adiciona informações sobre o token à lista de símbolos
                token_info["indice"] = self.obter_indice_simbolo(lexeme) or len(self.tabela_simbolos) + 1
                self.simbolos.append(token_info)
                

    # Método para obter o índice de um símbolo na tabela de símbolos
    def obter_indice_simbolo(self, lexeme):
        for indice, (simbolo, _) in enumerate(self.tabela_simbolos.items(), start=1):
            if simbolo == lexeme:
                return indice
        return None
    
    def is_operador(self, char):
        return char in  { '(', ')', ',', ':', ';', '[', ']', '{', '}', '-', '*', '/', '+', '!', '#', '<', '=', '>', '%', '?'}

    # Método para verificar se um caractere é um espaço em branco
    def is_whitespace(self, char):
        return char in {' ', '\t', '\n', '\r'}

    # Método para verificar se um caractere é uma letra
    def is_letter(self, char):
        return 'A' <= char <= 'Z'

    # Método para verificar se um caractere é um dígito
    def is_digit(self, char):
        return '0' <= char <= '9'

    # Método para avançar para a próxima posição no texto
    def avancar_posicao(self):
        if self.buffer[self.posicao] == '\n':
            self.linha += 1
        self.posicao += 1

    def reconhecer_operando(self):
        inicio = self.posicao
        operador = self.buffer[self.posicao]
        self.avancar_posicao()

        if self.posicao < self.buffer_size and operador in {':', '!', '<', '>', '='}: 
            if(self.buffer[self.posicao] == '='):
                self.avancar_posicao()
                operador = self.buffer[inicio:self.posicao]

        return {"token": operador, 
                "linha": self.linha,
                "tipo": "-",  # Tipo do token (no caso, caractere)
                "qtd_char_antes": len(operador),  # Quantidade de caracteres (um caractere)
                "qtd_char_depois": len(operador)}  # Quantidade de caracteres depois do truncamento (um caractere)


    # Método para verificar se um caractere é válido
    def is_valid_nome(self, char):
        return self.is_letter(char) or self.is_digit(char) or char == '-'
    
    def reconhecer_nome(self):
        nome = []  # Lista para armazenar os caracteres do nome

        # Loop para percorrer o texto enquanto houver caracteres válidos para um nome
        while self.posicao < self.buffer_size and (self.is_letter(self.buffer[self.posicao]) or self.is_digit(self.buffer[self.posicao])):
            # Adiciona o caractere atual ao nome se for válido ou um underscore
            if self.is_valid_nome(self.buffer[self.posicao]):
                nome.append(self.buffer[self.posicao])
            self.avancar_posicao()  # Avança para o próximo caractere

        qtd_char = len(nome)  # Calcula a quantidade de caracteres no nome
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)  # Limita a quantidade de caracteres depois do truncamento
        qtd_char_antes = max(qtd_char, qtd_char_depois)  # Limita a quantidade de caracteres antes do truncamento

        nome = ''.join(nome)[:LIMITE_QTD_CHAR]  # Junta os caracteres do nome em uma string e limita o tamanho

        # Verifica se o nome contém underscore para determinar o código do token e o escopo
        if(nome.find('_') == True):
            codigo = "C07"  # Código para variável local
            self.analisador_sintatico.set_escopo(1)  # Define o escopo como 1
        else:
            # Determina o código do token e ajusta o escopo com base no contexto sintático
            match self.analisador_sintatico.get_escopo():
                case 1:
                    codigo = "C07"  # Variável local
                case 2:
                    codigo = "C06"  # Nome do programa
                    self.analisador_sintatico.set_escopo(1)  # Reseta o escopo para 1 após identificar o nome do programa
                case 3:
                    codigo = "C05"  # Nome da função
                    self.analisador_sintatico.set_escopo(1)  # Reseta o escopo para 1 após identificar o nome da função

        # Verifica se o nome é "PROGRAMA" ou "FUNCOES" para ajustar o escopo
        if(nome == "PROGRAMA"):
            self.analisador_sintatico.set_escopo(2)  # Define o escopo como 2 para identificar a definição do programa
        elif(nome == "FUNCOES"):
            self.analisador_sintatico.set_escopo(3)  # Define o escopo como 3 para identificar a definição de funções

        # Retorna um dicionário com as informações do token
        return {"token": nome, 
                "linha": self.linha, 
                "tipo": "VOI",  # Tipo do token (no caso, identificador)
                "codigo": codigo,  # Código do token
                "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes do truncamento
                "qtd_char_depois": qtd_char_depois}  # Quantidade de caracteres depois do truncamento

    def reconhecer_numero(self):
        inicio = self.posicao  # Guarda a posição inicial do número

        # Loop para percorrer o texto enquanto houver dígitos
        while self.posicao < self.buffer_size:
            char = self.buffer[self.posicao]

            if self.is_digit(char):
                self.avancar_posicao()  # Avança para o próximo caractere
            elif char == '.':
                self.avancar_posicao()
                return self.reconhecer_real(inicio)  # Chama a função para reconhecer números reais se encontrar um ponto
            else:
                break

        qtd_char = self.posicao - inicio  # Calcula a quantidade de caracteres no número
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)  # Limita a quantidade de caracteres depois do truncamento
        qtd_char_antes = max(qtd_char, qtd_char_depois)  # Limita a quantidade de caracteres antes do truncamento
        
        numero =self.buffer[inicio:self.posicao][:qtd_char_depois]  # Extrai o número do texto e limita o tamanho

        # Retorna um dicionário com as informações do token
        return {"token": numero, 
                "linha": self.linha, 
                "tipo": "INT",  # Tipo do token (no caso, número inteiro)
                "codigo": "C03",  # Código do token
                "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes do truncamento
                "qtd_char_depois": qtd_char_depois}  # Quantidade de caracteres depois do truncamento}

    def is_valid_on_str(self, char):
        # Verifica se o caractere é uma letra, um dígito, espaço em branco, underscore, ponto ou cifrão
        return self.is_letter(char) or self.is_digit(char) or char in {' ', '_', '.', '$'}

    def reconhecer_cadeia(self):
        inicio = self.posicao  # Guarda a posição inicial da cadeia
        coluna_inicio = self.coluna  # Guarda a coluna inicial da cadeia
        self.avancar_posicao()  # Avança para o próximo caractere (após a aspas dupla)

        cadeia_valida = True  # Flag para verificar se a cadeia é válida
        while self.posicao < self.buffer_size and self.buffer[self.posicao] != '"':
            if not self.is_valid_on_str(self.buffer[self.posicao]):
                cadeia_valida = False  # Se o caractere não é válido, a cadeia é marcada como inválida
            self.avancar_posicao()  # Avança para o próximo caractere

        # Verifica se a cadeia é válida ou não
        if not cadeia_valida:
            self.avancar_posicao()  # Avança para o próximo caractere (após a aspas dupla final)
            cadeia = self.buffer[inicio:self.posicao]  # Extrai a cadeia do texto
            return -1  # Retorna -1 para indicar que a cadeia é inválida e deve ser ignorada

        # Calcula a quantidade de caracteres na cadeia
        qtd_char = self.posicao - inicio
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)  # Limita a quantidade de caracteres depois do truncamento
        qtd_char_antes = max(qtd_char, qtd_char_depois)  # Limita a quantidade de caracteres antes do truncamento

        # Extrai a cadeia do texto e limita o tamanho
        if qtd_char > LIMITE_QTD_CHAR:
            cadeia = self.buffer[inicio:self.posicao][:LIMITE_QTD_CHAR-1] + '"'  # Adiciona uma aspas dupla no final
            self.avancar_posicao()  # Avança para o próximo caractere (após a aspas dupla truncada)
        else:
            cadeia = self.buffer[inicio:self.posicao][:qtd_char_depois]  # Extrai a cadeia completa

        # Retorna um dicionário com as informações do token
        return {
            "token": cadeia, 
            "linha": self.linha, 
            "coluna": coluna_inicio, 
            "codigo": "C01",  # Código para cadeia de caracteres
            "tipo": "STR",  # Tipo do token (no caso, string)
            "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes do truncamento
            "qtd_char_depois": qtd_char_depois  # Quantidade de caracteres depois do truncamento
        }

    def reconhecer_caracter(self):
        inicio = self.posicao  # Guarda a posição inicial da cadeia
        self.avancar_posicao()  # Avança para o próximo caractere (após a aspas simples inicial)

        while self.posicao < self.buffer_size:
            if self.buffer[self.posicao] == "'" or self.buffer[self.posicao] == '\n':
                break
            if not self.is_letter(self.buffer[self.posicao]):
                self.avancar_posicao()  # Avança para o próximo caractere
                return -1
            self.avancar_posicao()  # Avança para o próximo caractere

        self.avancar_posicao()  # Avança para o próximo caractere
        caracter = self.buffer[inicio:self.posicao]
        if (len(caracter) > 3 or not (self.is_letter(caracter[1]) and caracter[2] == "'")):
            return -1
        
        return {"token": caracter, 
                "linha": self.linha, 
                "coluna": self.coluna - 1,  # Ajusta a coluna para o início do caractere
                "codigo": "C02",  # Código para caractere
                "tipo": "CHC",  # Tipo do token (no caso, caractere)
                "qtd_char_antes": len(caracter),  # Quantidade de caracteres (um caractere)
                "qtd_char_depois": len(caracter)}  # Quantidade de caracteres depois do truncamento (um caractere)

    def reconhecer_real(self, inicio):
        expoente_encontrado = False  # Flag para indicar se um expoente foi encontrado

        # Loop para percorrer o texto enquanto houver dígitos ou um ponto (parte decimal)
        while self.posicao < self.buffer_size:
            char = self.buffer[self.posicao]

            if self.is_digit(char):
                self.avancar_posicao()  # Avança para o próximo caractere
            elif char in ('e', 'E') and not expoente_encontrado:
                expoente_encontrado = True  # Marca que um expoente foi encontrado
                self.avancar_posicao()  # Avança para o próximo caractere
                if self.posicao < self.buffer_size and self.buffer[self.posicao] in ('+', '-'):
                    self.avancar_posicao()  # Avança para o próximo caractere se for um sinal após o expoente
            else:
                break  # Sai do loop se o caractere não for um dígito, ponto ou parte do expoente

        # Calcula a quantidade de caracteres na representação do número real
        qtd_char = self.posicao - inicio
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)  # Limita a quantidade de caracteres depois do truncamento
        qtd_char_antes = max(qtd_char, qtd_char_depois)  # Limita a quantidade de caracteres antes do truncamento

        # Extrai a representação do número real do texto e limita o tamanho
        if qtd_char > LIMITE_QTD_CHAR:
            token = self.buffer[inicio:self.posicao][:qtd_char_depois]  # Extrai o número real truncado
            # Verifica se o número real truncado contém um ponto decimal e ajusta o tipo do símbolo
            if '.' in token:
                if token.endswith('.'):  # Se o ponto decimal estiver no final, o número é inteiro
                    qtd_char_depois = qtd_char_depois - 1  # Ajusta a quantidade de caracteres depois do truncamento
                    token = self.buffer[inicio:self.posicao][:qtd_char_depois]  # Extrai o número inteiro
                    tipo_simb = "INT"  # Define o tipo do símbolo como inteiro
                    codigo = "C03"  # Define o código para números inteiros
                else:
                    tipo_simb = "PFO"  # Se o ponto decimal não estiver no final, o número é real
                    codigo = "C04"  # Define o código para números reais
            else:
                tipo_simb = "INT"  # Se não houver ponto decimal, o número é inteiro
                codigo = "C03"  # Define o código para números inteiros
        else:
            token = self.buffer[inicio:self.posicao][:qtd_char_depois]  # Extrai o número real completo
            # Verifica se o número real completo contém um ponto decimal e ajusta o tipo do símbolo
            if token.endswith('.'):
                qtd_char_depois = qtd_char_depois - 1  # Ajusta a quantidade de caracteres depois do truncamento
                token = self.buffer[inicio:self.posicao][:qtd_char_depois]  # Extrai o número inteiro
                tipo_simb = "INT"  # Define o tipo do símbolo como inteiro
                codigo = "C03"  # Define o código para números inteiros
            else:
                tipo_simb = "PFO"  # Se não houver ponto decimal, o número é real
                codigo = "C04"  # Define o código para números reais

        # Retorna um dicionário com as informações do token
        return {"token": token, 
                "linha": self.linha,  
                "codigo": codigo,  # Código correspondente ao tipo do número (inteiro ou real)
                "tipo": tipo_simb,  # Tipo do token (inteiro ou real)
                "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes do truncamento
                "qtd_char_depois": qtd_char_depois}  # Quantidade de caracteres depois do truncamento
