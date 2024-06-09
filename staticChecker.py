import sys
import os
from analisadorLexico import AnalisadorLexico

class AnalisadorSintatico:
    def __init__(self, nome_arquivo):
        # Inicializa o analisador léxico com o nome do arquivo e uma referência a si mesmo
        self.analisador_lexico = AnalisadorLexico(nome_arquivo, self)
        self.simbolos = []  # Lista de símbolos reconhecidos
        self.escopo = 1  # Escopo inicial

    def analisar(self):
        # Executa a análise léxica para reconhecer os tokens no arquivo fonte
        self.analisador_lexico.reconhecerTokens()
        # Obtém a tabela de símbolos gerada pelo analisador léxico
        self.simbolos = self.analisador_lexico.tabela_simbolos
        # Gera os relatórios de análise léxica e da tabela de símbolos
        self.analisador_lexico.gerar_relatorios()

    def get_escopo(self):
        return self.escopo  # Retorna o escopo atual

    def set_escopo(self, esc):
        self.escopo = esc  # Define o escopo atual

def main():
    # Verifica se o número de argumentos está correto
    if len(sys.argv) != 2:
        print("Uso: staticChecker.py <nome_arquivo>")
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
    analisador_sintatico.analisar()

if __name__ == "__main__":
    main()