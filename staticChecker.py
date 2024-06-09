import sys
import os
from analisadorLexico import AnalisadorLexico

class AnalisadorSintatico:
    def __init__(self, nome_arquivo):
        self.analisador_lexico = AnalisadorLexico(nome_arquivo, self)
        self.atomos = []
        self.escopo = 1

    def analisar(self):
        self.analisador_lexico.reconhecerTokens()
        self.atomos = self.analisador_lexico.simbolos
        self.analisador_lexico.gerar_relatorios()

    def get_atomos(self):
        return self.atomos
    
    def get_escopo(self):
        return self.escopo
    
    def set_escopo(self, esc):
        self.escopo = esc

def main():
    if len(sys.argv) != 2:
        print("Uso: staticChecker.py <nome_arquivo>")
        return
    
    nome_arquivo = sys.argv[1]
    nome_arquivo_completo = f"{nome_arquivo}.241"
    
    if not os.path.isfile(nome_arquivo_completo):
        print(f"Erro: O arquivo {nome_arquivo_completo} não existe.")
        return

    analisador_sintatico = AnalisadorSintatico(nome_arquivo_completo)
    analisador_sintatico.analisar()

if __name__ == "__main__":
    main()
