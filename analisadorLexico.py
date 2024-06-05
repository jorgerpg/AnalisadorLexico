import sys

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
        "-": "B13", "*": "B14", "/": "B15", "+": "B16", "!=": "B17", "#": "B18",
        "<": "B19", "<=": "B20", "==": "B21", ">": "B22", ">=":"B23",
        "consCadeia": "C01", "consCaracter": "C02", "consInteiro": "C03", "consReal": "C04",
        "nomFuncao": "C05", "nomPrograma": "C06", "variavel": "C07",
        #"subMáquina1": "D01", "subMáquina2": "D02", "subMáquina3": "D03" ????
    }

    RESERVADAS = {k.upper(): v for k, v in ATOMOS.items()}

    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.posicao = 0
        self.buffer = ''
        self.simbolos = []
        self.tabela_simbolos = {}
        self.carregar_arquivo()
        self.linha = 1
        self.coluna = 0

    def carregar_arquivo(self):
        try:
            with open(self.nome_arquivo, 'r') as arquivo:
                self.buffer = arquivo.read().upper()  # Converte todo o conteúdo para maiúsculas
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
                lex_file.write(f'Lexeme: {simbolo["token"]}, Codigo: {simbolo["codigo"]}, IndiceTabSimb: 1, Linha: {simbolo["linha"]}.\n')

    def gerar_relatorio_tabela_simbolos(self):
        with open(self.nome_arquivo + '.TAB', 'w') as tab_file:
            tab_file.write("Codigo da Equipe: 04\n")
            tab_file.write("Componentes:\n")
            tab_file.write("    Amanda Bandeira Aragao Rigaud Lima; amanda.lima@aln.senaicimatec.edu.br; (71)99142-8451\n")
            tab_file.write("    Jorge Ricarte Passos Goncalves; jorge.goncalves@aln.senaicimatec.edu.br; (71)99966-5608\n")
            tab_file.write("    Matheus Freitas Pereira; matheus.pereira@aln.senaicimatec.edu.br; (71)99267-9326\n")
            tab_file.write("    Eduardo de Araujo Rodrigues; eduardo.rodrigues@aln.senaicimatec.edu.br; (71)99166-1915\n\n")
            tab_file.write(f"RELATORIO DA TABELA DE SIMBOLOS. Texto fonte analisado: {self.nome_arquivo}.\n\n")

            entrada = 1
            for lexeme, info in self.tabela_simbolos.items():
                linhas = ', '.join(map(str, sorted(info['linhas'])))
                tab_file.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n")
                tab_file.write(f"Entrada: {entrada}, Codigo: {info['codigo']}, Lexeme: {lexeme},\n")
                tab_file.write(f"QtdCharAntesTrunc: {info['qtd_char_antes']}, QtdCharDepoisTrunc: {info['qtd_char_depois']},\n")
                tab_file.write(f"TipoSimb: {info['tipo_simb']}, Linhas: {{{linhas}}}.\n\n")
                entrada += 1

    def verificar_reservada(self, token):
        return self.RESERVADAS.get(token, None)
    
    def reconhecerTokens(self):
        while self.posicao < len(self.buffer):
            char = self.buffer[self.posicao]

            if self.is_whitespace(char):
                self.avancar_posicao()
                continue

            token = None
            if self.is_letter(char):
                token = self.reconhecer_nome()
            elif self.is_digit(char):
                token = self.reconhecer_numero()
            elif char == '"':
                token = self.reconhecer_cadeia()
            elif char == "'":
                token = self.reconhecer_caracter()
            # Adicione outras regras conforme necessário

            if token:
                reservada = self.verificar_reservada(token['token'])
                if reservada:
                    token['codigo'] = reservada
                self.simbolos.append(token)
                self.adicionar_tabela_simbolos(token)
            else:
                self.avancar_posicao()

    def adicionar_tabela_simbolos(self, token):
        lexeme = token['token']
        if lexeme not in self.tabela_simbolos:
            self.tabela_simbolos[lexeme] = {
                'codigo': token['codigo'],
                'qtd_char_antes': len(lexeme),
                'qtd_char_depois': len(lexeme),
                'tipo_simb': '-',
                'linhas': set()
            }
        self.tabela_simbolos[lexeme]['linhas'].add(token['linha'])

    def is_whitespace(self, char):
        return char in ' \t\n\r'

    def is_letter(self, char):
        return 'A' <= char <= 'Z'

    def is_digit(self, char):
        return char.isdigit()

    def avancar_posicao(self):
        if self.buffer[self.posicao] == '\n':
            self.linha += 1
            self.coluna = 0
        else:
            self.coluna += 1
        self.posicao += 1

    def reconhecer_nome(self):
        inicio = self.posicao
        coluna_inicio = self.coluna
        while self.posicao < len(self.buffer) and (self.is_letter(self.buffer[self.posicao]) or self.is_digit(self.buffer[self.posicao])):
            self.avancar_posicao()
        nome = self.buffer[inicio:self.posicao]
        return {"token": nome, "linha": self.linha, "coluna": coluna_inicio, "codigo": "C07"}

    def reconhecer_numero(self):
        inicio = self.posicao
        coluna_inicio = self.coluna
        while self.posicao < len(self.buffer) and self.is_digit(self.buffer[self.posicao]):
            self.avancar_posicao()
        numero = self.buffer[inicio:self.posicao]
        return {"token": numero, "linha": self.linha, "coluna": coluna_inicio, "codigo":  "C03"}

    def reconhecer_cadeia(self):
        self.avancar_posicao()  # Pular o primeiro "
        inicio = self.posicao
        coluna_inicio = self.coluna
        while self.posicao < len(self.buffer) and self.buffer[self.posicao] != '"':
            self.avancar_posicao()
        cadeia = self.buffer[inicio:self.posicao]
        self.avancar_posicao()  # Pular o último "
        return {"token": cadeia, "linha": self.linha, "coluna": coluna_inicio, "codigo": "C01"}

    def reconhecer_caracter(self):
        self.avancar_posicao()  # Pular o primeiro '
        if self.posicao < len(self.buffer):
            caracter = self.buffer[self.posicao]
            self.avancar_posicao()  # Pular o caracter
            if self.posicao < len(self.buffer) and self.buffer[self.posicao] == "'":
                self.avancar_posicao()  # Pular o último '
                return {"token": caracter, "linha": self.linha, "coluna": self.coluna - 1, "codigo": "C02"}
        return None  # Caso o formato seja inválido