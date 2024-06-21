import sys
import os
from analisadorLexico import AnalisadorLexico

class AnalisadorSintatico:
    # Constantes para mapear tokens para códigos
    TABELA_DE_PALAVRAS_E_SIMBOLOS_RESERVADOS = {
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

    # Mapeamento das palavras reservadas para os códigos correspondentes
    RESERVADAS = {k.upper(): v for k, v in TABELA_DE_PALAVRAS_E_SIMBOLOS_RESERVADOS.items()}

    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        # Inicializa o analisador léxico com o nome do arquivo e uma referência a si mesmo
        self.analisador_lexico = AnalisadorLexico(self)
        self.tabela_simbolos = {}  # Lista de símbolos reconhecidos
        self.simbolos = []
        self.escopo = 1  # Escopo inicial

    def analisar(self, buffer):
        self.analisador_lexico.carregarBuffer(buffer)
        # Executa a análise léxica para reconhecer os tokens no arquivo fonte
        self.analisador_lexico.reconhecerTokens()
        # Obtém todos os simbolos para o .LEX
        self.simbolos = self.analisador_lexico.getSimbolos()
        # Obtém a tabela de símbolos gerada pelo analisador léxico
        self.tabela_simbolos = self.analisador_lexico.getTabelaSimbolos()
        # Gera os relatórios de análise léxica e da tabela de símbolos
        self.gerar_relatorios()

    def get_escopo(self):
        return self.escopo  # Retorna o escopo atual

    def set_escopo(self, esc):
        self.escopo = esc  # Define o escopo atual
        # Método para gerar relatório léxico

    # Método para gerar relatórios léxicos e tabela de símbolos
    def gerar_relatorios(self):
        self.gerar_relatorio_lexico()  # Chama o método para gerar o relatório léxico
        self.gerar_relatorio_tabela_simbolos()  # Chama o método para gerar o relatório da tabela de símbolos
    
    def gerar_relatorio_lexico(self):
        # Remove a extensão atual se existir
        nome_base = os.path.splitext(self.nome_arquivo)[0]
        # Adiciona a nova extensão .LEX
        nome_arquivo_lex = nome_base + '.LEX'
        with open(nome_arquivo_lex, 'w') as lex_file:
            # Escreve informações de equipe no arquivo de relatório léxico
            lex_file.write("Codigo da Equipe: 04\n")
            lex_file.write("Componentes:\n")
            lex_file.write("    Amanda Bandeira Aragao Rigaud Lima; amanda.lima@aln.senaicimatec.edu.br; (71)99142-8451\n")
            lex_file.write("    Jorge Ricarte Passos Goncalves; jorge.goncalves@aln.senaicimatec.edu.br; (71)99966-5608\n")
            lex_file.write("    Matheus Freitas Pereira; matheus.pereira@aln.senaicimatec.edu.br; (71)99166-1915\n")
            lex_file.write("    Eduardo de Araujo Rodrigues; eduardo.rodrigues@aln.senaicimatec.edu.br; (71)99267-9326\n\n")
            lex_file.write(f"RELATORIO DA ANALISE LEXICA. Texto fonte analisado: {self.nome_arquivo}.\n\n")

            # Escreve informações de tokens no arquivo de relatório léxico
            for simbolo in self.simbolos:
                lex_file.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n")
                lex_file.write(f'Lexeme: {simbolo["token"]}, Codigo: {simbolo["codigo"]}, IndiceTabSimb: {simbolo["indice"]}, Linha: {simbolo["linha"]}.\n')

    # Método para gerar relatório da tabela de símbolos
    def gerar_relatorio_tabela_simbolos(self):
        # Remove a extensão atual se existir
        nome_base = os.path.splitext(self.nome_arquivo)[0]
        # Adiciona a nova extensão .TAB
        nome_arquivo_tab= nome_base + '.TAB'
        with open(nome_arquivo_tab, 'w') as tab_file:
            # Escreve informações de equipe no arquivo de relatório da tabela de símbolos
            tab_file.write("Codigo da Equipe: 04\n")
            tab_file.write("Componentes:\n")
            tab_file.write("    Amanda Bandeira Aragao Rigaud Lima; amanda.lima@aln.senaicimatec.edu.br; (71)99142-8451\n")
            tab_file.write("    Jorge Ricarte Passos Goncalves; jorge.goncalves@aln.senaicimatec.edu.br; (71)99966-5608\n")
            tab_file.write("    Matheus Freitas Pereira; matheus.pereira@aln.senaicimatec.edu.br; (71)99166-1915\n")
            tab_file.write("    Eduardo de Araujo Rodrigues; eduardo.rodrigues@aln.senaicimatec.edu.br; (71)99267-9326\n\n")
            tab_file.write(f"RELATORIO DA TABELA DE SIMBOLOS. Texto fonte analisado: {self.nome_arquivo}.\n\n")

            # Escreve informações da tabela de símbolos no arquivo de relatório da tabela de símbolos
            for indice, (lexeme, info) in enumerate(self.tabela_simbolos.items(), start=1):
                linhas = ', '.join(map(str, sorted(info['linhas'])[:5]))
                tab_file.write("-------------------------------------------------------------------------------------------------------------------------------------------------\n")
                tab_file.write(f"Entrada: {indice}, Codigo: {info['codigo']}, Lexeme: {lexeme},\n")
                tab_file.write(f"QtdCharAntesTrunc: {info['qtd_char_antes']}, QtdCharDepoisTrunc: {info['qtd_char_depois']},\n")
                tab_file.write(f"TipoSimb: {info['tipo_simb']}, Linhas: {{{linhas}}}.\n\n")
    

    # Método para carregar o conteúdo do arquivo
    def carregar_arquivo(self):
        try:
            with open(self.nome_arquivo, 'r') as arquivo:
                buffer = arquivo.read().upper()  # Lê o arquivo e filtra comentários
                return buffer
        except FileNotFoundError:
            print(f"Erro: O arquivo '{self.nome_arquivo}' não foi encontrado.")
            sys.exit(1)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            sys.exit(1)

def main():
    # Verifica se o número de argumentos está correto
    if len(sys.argv) != 2:
        print("Uso: staticChecker.py <caminho_arquivo_sem_.241>")
        return
    
    # Obtém o nome do arquivo a partir dos argumentos de linha de comando
    nome_arquivo = sys.argv[1]
    nome_arquivo_completo = f"{nome_arquivo}.241"  # Adiciona a extensão ao nome do arquivo
    
    # Verifica se o arquivo existe
    if not os.path.isfile(nome_arquivo_completo):
        print(f"Erro: O arquivo {nome_arquivo_completo} não existe.")
        return

    # Cria uma instância do analisador sintático e executa a análise
    analisador_sintatico = AnalisadorSintatico(nome_arquivo_completo)
    buffer = analisador_sintatico.carregar_arquivo()
    analisador_sintatico.analisar(buffer)

if __name__ == "__main__":
    main()