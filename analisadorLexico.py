import sys
import re

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
    }

    RESERVADAS = {k.upper(): v for k, v in ATOMOS.items()}

    TIPOS = {
        "A01": "STR", "A02": "CHC", "A03": "declaracoes", "A05": "BOO",
        "A14": "INT", "A18": "PFO", "A25": "BOO", "A26": "VOI",
        "C01": "STR", "C02": "CHC", "C03": "INT", "C04": "PFO", 
        "C05": "STR", "C06": "STR", "C07": "STR",
    }

    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.posicao = 0
        self.buffer = ''
        self.simbolos = []
        self.tabela_simbolos = {}
        self.carregar_arquivo()
        self.linha = 1
        self.coluna = 0
        self.linhas_originais = self.buffer.splitlines()

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
        while self.posicao < len(self.buffer):
            if self.is_whitespace(self.buffer[self.posicao]):
                self.avancar_posicao()
                continue

            if not self.is_valid_char(self.buffer[self.posicao]):
                self.avancar_posicao()
                continue

            if self.buffer[self.posicao] == '"':
                token_info = self.reconhecer_cadeia()
                token_info["codigo"] = "C01"
                tipo_simb = "STR"
            elif self.buffer[self.posicao] == "'":
                token_info = self.reconhecer_caracter()
                token_info["codigo"] = "C02"
                tipo_simb = "CHC"
            elif self.is_letter(self.buffer[self.posicao]):
                token_info = self.reconhecer_nome()
                codigo = self.RESERVADAS.get(token_info["token"], "C07")
                token_info["codigo"] = codigo
                tipo_simb = self.determinar_tipo(codigo)
            elif self.is_digit(self.buffer[self.posicao]):
                token_info = self.reconhecer_real()  # Chama a nova função para reconhecer números reais
                if token_info is None:
                    token_info = self.reconhecer_numero()
                    token_info["codigo"] = "C03"
                    tipo_simb = "INT"
                else:
                    token_info["codigo"] = "C04"
                    tipo_simb = "PFO"
            else:
                self.avancar_posicao()
                continue

            lexeme = token_info["token"]
            qtd_char_antes = len(lexeme)
            qtd_char_depois = min(qtd_char_antes, 30)

            token_info["indice"] = self.obter_indice_simbolo(lexeme) or len(self.tabela_simbolos) + 1
            self.simbolos.append(token_info)

            if lexeme not in self.tabela_simbolos:
                self.tabela_simbolos[lexeme] = {
                    "codigo": token_info["codigo"],
                    "qtd_char_antes": qtd_char_antes,
                    "qtd_char_depois": qtd_char_depois,
                    "tipo_simb": tipo_simb,
                    "linhas": {token_info["linha"]}
                }
            else:
                self.tabela_simbolos[lexeme]["linhas"].add(token_info["linha"])
                
    def determinar_tipo(self, codigo):
        return self.TIPOS.get(codigo, "-")

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
        return self.is_letter(char) or self.is_digit(char) or self.is_whitespace(char) or char in {'"', "'", '(', ')', ',', ':', ';', '[', ']', '{', '}', '-', '*', '/', '+', '!', '#', '<', '=', '>', '%', '?'}

    def avancar_posicao(self):
        if self.posicao < len(self.buffer):
            if self.buffer[self.posicao] == '\n':
                self.linha += 1
                self.coluna = 0
            else:
                self.coluna += 1
            self.posicao += 1

    def reconhecer_nome(self):
        coluna_inicio = self.coluna
        nome = []

        while self.posicao < len(self.buffer) and (self.is_letter(self.buffer[self.posicao]) or self.is_digit(self.buffer[self.posicao]) or not self.is_valid_char(self.buffer[self.posicao])):
            if self.is_valid_char(self.buffer[self.posicao]):
                nome.append(self.buffer[self.posicao])
            self.avancar_posicao()

        nome = ''.join(nome)[:30]  # Limita a 30 caracteres
        return {"token": nome, 
                "linha": self.linha, 
                "coluna": coluna_inicio, 
                "codigo": "C07"}

    def reconhecer_numero(self):
        inicio = self.posicao
        coluna_inicio = self.coluna
        while self.posicao < len(self.buffer) and self.is_digit(self.buffer[self.posicao]):
            self.avancar_posicao()
        numero = self.buffer[inicio:self.posicao]
        return {"token": numero, 
                "linha": self.linha, 
                "coluna": coluna_inicio, 
                "codigo": "C03"}

    def reconhecer_cadeia(self):
        self.avancar_posicao()  # Pular o primeiro "
        inicio = self.posicao
        coluna_inicio = self.coluna
        while self.posicao < len(self.buffer) and self.buffer[self.posicao] != '"':
            self.avancar_posicao()
        cadeia = self.buffer[inicio:self.posicao][:30]  # Limita a 30 caracteres
        self.avancar_posicao()  # Pular o último "
        return {"token": cadeia, 
                "linha": self.linha, 
                "coluna": coluna_inicio, 
                "codigo": "C01"}

    def reconhecer_caracter(self):
        self.avancar_posicao()  # Pular o primeiro '
        if self.posicao < len(self.buffer):
            caracter = self.buffer[self.posicao]
            self.avancar_posicao()  # Pular o caracter
            if self.posicao < len(self.buffer) and self.buffer[self.posicao] == "'":
                self.avancar_posicao()  # Pular o último '
                return {"token": caracter, 
                        "linha": self.linha, 
                        "coluna": self.coluna - 1, 
                        "codigo": "C02"}
        return None
    

    def reconhecer_real(self):
        inicio = self.posicao
        ponto_encontrado = False
        expoente_encontrado = False
        pos_expoente = -1

        while self.posicao < len(self.buffer):
            char = self.buffer[self.posicao]
            if self.is_digit(char):
                self.avancar_posicao()
            elif char == '.' and not ponto_encontrado:
                ponto_encontrado = True
                self.avancar_posicao()
            elif char in ('e', 'E') and not expoente_encontrado:
                expoente_encontrado = True
                self.avancar_posicao()
                if self.posicao < len(self.buffer) and self.buffer[self.posicao] in ('+', '-'):
                    self.avancar_posicao()
                pos_expoente = self.posicao
            else:
                break

        if ponto_encontrado:
            token = self.buffer[inicio:self.posicao]
            if expoente_encontrado and pos_expoente < self.posicao:
                return {
                    "token": token,
                    "linha": self.linha,
                    "coluna": self.coluna - len(token)
                }
            elif not expoente_encontrado:
                return {
                    "token": token,
                    "linha": self.linha,
                    "coluna": self.coluna - len(token)
                }

        self.posicao = inicio
        return None