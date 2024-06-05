import sys
from analisadorLexico import AnalisadorLexico

class AnalisadorSintatico:
    def __init__(self, nome_arquivo):
        self.analisador_lexico = AnalisadorLexico(nome_arquivo)
        self.atomos = []

    def analisar(self):
        self.analisador_lexico.reconhecerTokens()
        self.atomos = self.analisador_lexico.simbolos
        self.analisador_lexico.gerar_relatorios()

    def get_atomos(self):
        return self.atomos

    def get_simbolos(self):
        return self.analisador_lexico.get_simbolos()

def main():
    if len(sys.argv) != 2:
        print("Uso: staticChecker.py <nome_arquivo>")
        return
    
    nome_arquivo = sys.argv[1]
    if not nome_arquivo.endswith('.241'):
        print("Erro: O arquivo deve ter a extensão .241.")
        return

    analisador_sintatico = AnalisadorSintatico(nome_arquivo)
    analisador_sintatico.analisar()

if __name__ == "__main__":
    main()
