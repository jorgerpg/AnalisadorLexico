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

    def __init__(self, nome_arquivo, analisador_sintatico):
        self.nome_arquivo = nome_arquivo

        self.valid_symbols = {'"', "'", '(', ')', ',', ':', ';', '[', ']', '{', '}', '-', '*', '/', '+', '!', '#', '<', '=', '>', '%', '?', '$'}
        self.posicao = 0
        self.buffer = ''
        self.buffer_size = 0
        self.simbolos = []
        self.tabela_simbolos = {}
        self.carregar_arquivo()
        self.linha = 1
        self.coluna = 0
        self.linhas_originais = self.buffer.splitlines()
        self.analisador_sintatico = analisador_sintatico

    def carregar_arquivo(self):
        try:
            with open(self.nome_arquivo, 'r') as arquivo:
                self.buffer = self.filtrar_comentarios(arquivo.read().upper())
                self.buffer_size = len(self.buffer)
        except FileNotFoundError:
            print(f"Erro: O arquivo '{self.nome_arquivo}' não foi encontrado.")
            sys.exit(1)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            sys.exit(1)

    def gerar_relatorios(self):
        self.gerar_relatorio_lexico()
        self.gerar_relatorio_tabela_simbolos()

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
                linhas = ', '.join(map(str, sorted(info['linhas'])[:5]))
                tab_file.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n")
                tab_file.write(f"Entrada: {indice}, Codigo: {info['codigo']}, Lexeme: {lexeme},\n")
                tab_file.write(f"QtdCharAntesTrunc: {info['qtd_char_antes']}, QtdCharDepoisTrunc: {info['qtd_char_depois']},\n")
                tab_file.write(f"TipoSimb: {info['tipo_simb']}, Linhas: {{{linhas}}}.\n\n")

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
    
    def reconhecerTokens(self):
        while self.posicao < self.buffer_size:
            if self.is_whitespace(self.buffer[self.posicao]):
                self.avancar_posicao()
                continue

            if not self.is_valid_char(self.buffer[self.posicao]):
                self.avancar_posicao()
                continue

            if self.buffer[self.posicao] == '"':
                token_info = self.reconhecer_cadeia()
                if(token_info == -1):
                    continue
            elif self.buffer[self.posicao] == "'":
                token_info = self.reconhecer_caracter()
            elif self.is_letter(self.buffer[self.posicao]):
                token_info = self.reconhecer_nome()
            elif self.is_digit(self.buffer[self.posicao]):
                token_info = self.reconhecer_numero()
            else:
                self.avancar_posicao()
                continue

            lexeme = token_info["token"]

            token_info["indice"] = self.obter_indice_simbolo(lexeme) or len(self.tabela_simbolos) + 1
            self.simbolos.append(token_info)

            if token_info["token"] not in self.RESERVADAS:
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

    def obter_indice_simbolo(self, lexeme):
        for indice, (simbolo, _) in enumerate(self.tabela_simbolos.items(), start=1):
            if simbolo == lexeme:
                return indice
        return None

    def is_whitespace(self, char):
        return char in {' ', '\t', '\n', '\r'}

    def is_letter(self, char):
        return 'A' <= char <= 'Z'

    def is_digit(self, char):
        return '0' <= char <= '9'

    def is_valid_char(self, char):
        return self.is_letter(char) or self.is_digit(char) or self.is_whitespace(char) or char in self.valid_symbols

    def avancar_posicao(self):
        self.coluna += 1
        if self.buffer[self.posicao] == '\n':
            self.linha += 1
            self.coluna = 0
        self.posicao += 1

    def reconhecer_nome(self):
        coluna_inicio = self.coluna
        nome = []

        while self.posicao < self.buffer_size and (self.is_letter(self.buffer[self.posicao]) or self.is_digit(self.buffer[self.posicao]) or not self.is_valid_char(self.buffer[self.posicao])):
            if self.is_valid_char(self.buffer[self.posicao]) or self.buffer[self.posicao] == '_':
                nome.append(self.buffer[self.posicao])
            self.avancar_posicao()

        qtd_char = len(nome)
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)
        qtd_char_antes = max(qtd_char, qtd_char_depois)

        nome = ''.join(nome)[:LIMITE_QTD_CHAR]

        if(nome.find('_') == True):
            codigo = "C07" #verificar o q fazaer
            self.analisador_sintatico.set_escopo(1)
        else:
            match self.analisador_sintatico.get_escopo():
                case 1:
                    codigo = "C07"
                case 2:
                    codigo = "C06"
                    self.analisador_sintatico.set_escopo(1)
                case 3:
                    codigo = "C05"
                    self.analisador_sintatico.set_escopo(1)
            
        if(nome == "PROGRAMA"):
            self.analisador_sintatico.set_escopo(2)
        elif(nome == "FUNCOES"):
            self.analisador_sintatico.set_escopo(3)

        return {"token": nome, 
                "linha": self.linha, 
                "coluna": coluna_inicio, 
                "tipo": "VOI",
                "codigo": codigo,
                "qtd_char_antes": qtd_char_antes,
                "qtd_char_depois": qtd_char_depois}
    
    def reconhecer_numero(self):
        inicio = self.posicao
        coluna_inicio = self.coluna

        while self.posicao < self.buffer_size:
            char = self.buffer[self.posicao]

            if self.is_digit(char):
                self.avancar_posicao()
            elif char == '.':
                self.avancar_posicao()
                return self.reconhecer_real(inicio, coluna_inicio)
            else:
                break

        qtd_char = self.posicao - inicio
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)
        qtd_char_antes = max(qtd_char, qtd_char_depois)
        
        numero =self.buffer[inicio:self.posicao][:qtd_char_depois]
        
        return {"token": numero, 
                "linha": self.linha, 
                "coluna": coluna_inicio, 
                "tipo": "INT",
                "codigo": "C03",
                "qtd_char_antes": qtd_char_antes,
                "qtd_char_depois": qtd_char_depois} 
    

    def is_valid_on_str(self, char):
        return self.is_letter(char) or self.is_digit(char) or char in {' ', '_', '.', '$'}
    
    def reconhecer_cadeia(self):
        inicio = self.posicao
        coluna_inicio = self.coluna
        self.avancar_posicao()

        cadeia_valida = True  # Flag para verificar se a cadeia é válida
        while self.posicao < self.buffer_size and self.buffer[self.posicao] != '"':
            if not self.is_valid_on_str(self.buffer[self.posicao]):
                cadeia_valida = False
            self.avancar_posicao()


        if not cadeia_valida:
            self.avancar_posicao()
            cadeia = self.buffer[inicio:self.posicao]
            return -1  # Ignorar a cadeia inteira

        qtd_char = self.posicao - inicio
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)
        qtd_char_antes = max(qtd_char, qtd_char_depois)

        if qtd_char > LIMITE_QTD_CHAR:
            cadeia = self.buffer[inicio:self.posicao][:LIMITE_QTD_CHAR-1] + '"'
            self.avancar_posicao()
        else:
            cadeia = self.buffer[inicio:self.posicao][:qtd_char_depois]

        return {
            "token": cadeia, 
            "linha": self.linha, 
            "coluna": coluna_inicio, 
            "codigo": "C01",
            "tipo": "STR",
            "qtd_char_antes": qtd_char_antes,
            "qtd_char_depois": qtd_char_depois
        }
    
    def reconhecer_caracter(self):
        self.avancar_posicao()

        if self.posicao < self.buffer_size:
            caracter = "'" + self.buffer[self.posicao] + "'"
            self.avancar_posicao()
    
            if self.posicao < self.buffer_size and self.buffer[self.posicao] == "'":
                self.avancar_posicao()
                return {"token": caracter, 
                        "linha": self.linha, 
                        "coluna": self.coluna - 1, 
                        "codigo": "C02",
                        "tipo" : "CHC",
                        "qtd_char_antes": len(caracter),
                        "qtd_char_depois": len(caracter)}
            
        return None
    
    def reconhecer_real(self, inicio, coluna_inicio):
        expoente_encontrado = False
        pos_expoente = -1

        while self.posicao < self.buffer_size:
            char = self.buffer[self.posicao]

            if self.is_digit(char):
                self.avancar_posicao()
            elif char in ('e', 'E') and not expoente_encontrado:
                expoente_encontrado = True
                self.avancar_posicao() 
                if self.posicao < self.buffer_size and self.buffer[self.posicao] in ('+', '-'):
                    self.avancar_posicao()
            else:
                break 

        qtd_char = self.posicao - inicio
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR) 
        qtd_char_antes = max(qtd_char, qtd_char_depois)

        if(qtd_char > LIMITE_QTD_CHAR):
            token = self.buffer[inicio:self.posicao][:qtd_char_depois]
            if '.' in token:
                if token.endswith('.'):
                    qtd_char_depois = qtd_char_depois - 1
                    token = self.buffer[inicio:self.posicao][:qtd_char_depois]
                    tipo_simb = "INT"
                    codigo = "C03"
                else:
                    tipo_simb = "PFO"
                    codigo = "C04"
            else:
                tipo_simb = "INT"
                codigo = "C03"
        else:
            token = self.buffer[inicio:self.posicao][:qtd_char_depois]
            if token.endswith('.'):
                qtd_char_depois = qtd_char_depois - 1
                token = self.buffer[inicio:self.posicao][:qtd_char_depois]
                tipo_simb = "INT"
                codigo = "C03"
            else:
                tipo_simb = "PFO"
                codigo = "C04"

        return {"token": token, 
                "linha": self.linha,  
                "codigo": codigo,
                "tipo": tipo_simb,
                "coluna": self.coluna - len(token),
                "qtd_char_antes": qtd_char_antes,  
                "qtd_char_depois": qtd_char_depois}
