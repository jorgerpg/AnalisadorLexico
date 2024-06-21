import sys
import re

LIMITE_QTD_CHAR = 30

class AnalisadorLexico:
    # Método de inicialização da classe AnalisadorLexico
    def __init__(self, analisador_sintatico):
        # Inicializa os atributos da classe
        self.posicao = 0
        self.buffer = ''
        self.buffer_size = 0
        self.simbolos = []
        self.tabela_simbolos = {}
        self.linha = 1
        self.coluna = 0
        self.linhas_originais = self.buffer.splitlines()  # Divide o texto em linhas
        self.analisador_sintatico = analisador_sintatico

    # Método para carregar o conteúdo do arquivo
    def carregarBuffer(self, buffer):
                self.buffer = buffer # Lê o buffer e filtra comentários
                self.buffer_size = len(self.buffer)  # Calcula o tamanho do buffer
    
    # Obtém todos os simbolos identificados
    def getSimbolos(self):
        return self.simbolos
    
    # Obtém a tabela de simbolos
    def getTabelaSimbolos(self):
        return self.tabela_simbolos

    # Método para reconhecer tokens no texto
    def reconhecerTokens(self):
        # Percorre o texto enquanto a posição atual for menor que o tamanho do buffer
        while self.posicao < self.buffer_size:
            # Ignora espaços em branco
            if self.is_whitespace(self.buffer[self.posicao]):
                self.avancar_posicao()  # Move para a próxima posição
                continue
            
            if self.buffer[self.posicao] == '/':
                self.filtrar_comentarios()
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
            elif self.is_letter(self.buffer[self.posicao]) or self.buffer[self.posicao] == '_':
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
            if token_info["token"] not in self.analisador_sintatico.RESERVADAS:
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
                token_info["codigo"] = self.analisador_sintatico.RESERVADAS.get(lexeme, None)
                # Adiciona informações sobre o token à lista de símbolos
                token_info["indice"] = '-'
                self.simbolos.append(token_info)

    # Método para filtrar os comentarios
    def filtrar_comentarios(self):
        inicio = self.posicao
        #Verifica o proximo char
        self.avancar_posicao()

        if(self.buffer[self.posicao] == '/'):
            while self.posicao < self.buffer_size and self.buffer[self.posicao] != '\n': 
                self.avancar_posicao()
        
        if(self.buffer[self.posicao] == '*'):
            while self.posicao < self.buffer_size and self.buffer[self.posicao:self.posicao+2] != '*/': 
                self.avancar_posicao()
            self.avancar_posicao()
            self.avancar_posicao()

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
        if self.posicao == self.buffer_size:
            return
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

    # Método para verificar se um caractere é válido como na linguagem
    def is_valid_char(self, char):
        # Conjunto de caracteres válidos
        valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$ .%():;?[]{}-*/+!=#<>")
        return char in valid_chars

    # Método para verificar se um caractere é válido como nome
    def is_valid_nome(self, char):
        return self.is_letter(char) or self.is_digit(char)
    
    # Função para verificar se um caractere é válido na linguagem, mas não como parte de um nome
    def is_valid_in_language_not_in_nome(self, char):
        # Conjunto de caracteres válidos
        not_valid_chars = set("$ .%():;?[]{}-*/+!=#<>")
        return char in not_valid_chars

    def reconhecer_nome(self):
        Posinicial = self.posicao
        escopo = self.analisador_sintatico.get_escopo()
        nome = []  # Lista para armazenar os caracteres do nome

        if self.is_letter(self.buffer[Posinicial]) and escopo != 1:
            # Loop para percorrer o texto enquanto houver caracteres válidos para um nome
            while self.posicao < self.buffer_size and not (self.is_valid_in_language_not_in_nome(self.buffer[self.posicao]) or self.buffer[self.posicao] == '_' or self.buffer[self.posicao] == '\n'):
                if self.is_valid_nome(self.buffer[self.posicao]):
                    nome.append(self.buffer[self.posicao])
                    self.avancar_posicao()  # Avança para o próximo caractere
                elif not self.is_valid_char(self.buffer[self.posicao]):
                    self.avancar_posicao()  # Avança para o próximo caractere
                else:
                    break
        else:
            # Loop para percorrer o texto enquanto houver caracteres válidos para uma string
            while self.posicao < self.buffer_size and not (self.is_valid_in_language_not_in_nome(self.buffer[self.posicao]) or self.buffer[self.posicao] == '\n'):
                if (self.is_valid_nome(self.buffer[self.posicao]) or self.buffer[self.posicao] == '_'):
                    nome.append(self.buffer[self.posicao])
                    self.avancar_posicao()  # Avança para o próximo caractere
                elif not self.is_valid_char(self.buffer[self.posicao]):
                    self.avancar_posicao()  # Avança para o próximo caractere
                else:
                    break
        
        qtd_char = len(nome)  # Calcula a quantidade de caracteres no nome
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)  # Limita a quantidade de caracteres depois do truncamento
        qtd_char_antes = max(qtd_char, qtd_char_depois)  # Limita a quantidade de caracteres antes do truncamento

        nome = ''.join(nome)[:LIMITE_QTD_CHAR]  # Junta os caracteres do nome em uma string e limita o tamanho

        # Verifica se o nome contém underscore para determinar o código do token e o escopo
        if '_' in nome:
            codigo = "C07"  # Código para variável local
        else:
            # Determina o código do token e ajusta o escopo com base no contexto sintático
            match escopo:
                case 1:
                    codigo = "C07"  # Variável local
                case 2:
                    codigo = "C06"  # Nome do programa
                    self.analisador_sintatico.set_escopo(1)  # Reseta o escopo para 1 após identificar o nome do programa
                case 3:
                    codigo = "C05"  # Nome da função
                    self.analisador_sintatico.set_escopo(1)  # Reseta o escopo para 1 após identificar o nome da função

        # Verifica se o nome é "PROGRAMA" ou "FUNCOES" para ajustar o escopo
        if nome == "PROGRAMA":
            self.analisador_sintatico.set_escopo(2)  # Define o escopo como 2 para identificar a definição do programa
        elif nome == "FUNCOES":
            self.analisador_sintatico.set_escopo(3)  # Define o escopo como 3 para identificar a definição de funções

        # Retorna um dicionário com as informações do token
        return {
            "token": nome, 
            "linha": self.linha, 
            "tipo": "VOI",  # Tipo do token (no caso, identificador)
            "codigo": codigo,  # Código do token
            "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes do truncamento
            "qtd_char_depois": qtd_char_depois  # Quantidade de caracteres depois do truncamento
        }
    
    # Função para verificar se um caractere é válido na linguagem, mas não como parte de uma str
    def is_valid_on_str(self, char):
        # Conjunto de caracteres válidos
        valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$ .")
        return char in valid_chars
    
    def reconhecer_cadeia(self):
        cadeia = []  # Lista para armazenar os caracteres do nome
        inicio = self.posicao  # Guarda a posição inicial da cadeia
        cadeia.append(self.buffer[self.posicao])
        self.avancar_posicao()  # Avança para o próximo caractere (após a aspas dupla)

        cadeia_valida = True  # Flag para verificar se a cadeia é válida

        while self.posicao < self.buffer_size and self.buffer[self.posicao] != '"':
            if not self.is_valid_char(self.buffer[self.posicao]):
                self.avancar_posicao()  # Avança para o próximo caractere
            elif not self.is_valid_on_str(self.buffer[self.posicao]):
                # Se o caractere não é válido, a cadeia é marcada como inválida
                cadeia_valida = False
                cadeia.append(self.buffer[self.posicao])
                self.avancar_posicao()  # Avança para o próximo caractere
            else:
                # Caractere válido dentro da cadeia, adiciona à lista
                cadeia.append(self.buffer[self.posicao])
                self.avancar_posicao()  # Avança para o próximo caractere

        cadeia.append(self.buffer[self.posicao])
        self.avancar_posicao()  # Avança para o próximo caractere (após a aspas dupla final)

        # Verifica se a cadeia é válida ou não
        if not cadeia_valida:
            cadeia = self.buffer[inicio:self.posicao]  # Extrai a cadeia do texto
            return -1  # Retorna -1 para indicar que a cadeia é inválida e deve ser ignorada


        qtd_char = len(cadeia)  # Calcula a quantidade de caracteres no cadeia
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)  # Limita a quantidade de caracteres depois do truncamento
        qtd_char_antes = max(qtd_char, qtd_char_depois)  # Limita a quantidade de caracteres antes do truncamento

        cadeia = ''.join(cadeia)[:LIMITE_QTD_CHAR]  # Junta os caracteres do nome em uma string e limita o tamanho

        # Extrai a cadeia do texto e limita o tamanho
        if qtd_char > LIMITE_QTD_CHAR:
            cadeia = ''.join(cadeia)[:LIMITE_QTD_CHAR-1] + '"'  # Adiciona uma aspas dupla no final

        # Retorna um dicionário com as informações do token
        return {
            "token": cadeia, 
            "linha": self.linha,
            "codigo": "C01",  # Código para cadeia de caracteres
            "tipo": "STR",  # Tipo do token (no caso, string)
            "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes do truncamento
            "qtd_char_depois": qtd_char_depois  # Quantidade de caracteres depois do truncamento
        }

    def reconhecer_caracter(self):
        inicio = self.posicao  # Guarda a posição inicial da cadeia
        self.avancar_posicao()  # Avança para o próximo caractere (após a aspas simples inicial)

        while self.posicao < self.buffer_size:
            if self.buffer[self.posicao] == "'":
                break
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

    # Função para verificar se um caractere é válido na linguagem, mas não como parte de um nome
    def is_valid_in_language_not_in_numero(self, char):
        # Conjunto de caracteres válidos
        not_valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ_$ %():;?[]{}-*/+!=#<>")
        return char in not_valid_chars
    
    def reconhecer_numero(self):
        numero = []  # Lista para armazenar os caracteres do numero

        # Loop para percorrer o texto enquanto houver dígitos
        while self.posicao < self.buffer_size and self.buffer[self.posicao] != '\n':
            char = self.buffer[self.posicao]

            if self.is_digit(char):
                numero.append(self.buffer[self.posicao])
                self.avancar_posicao()  # Avança para o próximo caractere
            elif char == '.':
                numero.append(self.buffer[self.posicao])
                self.avancar_posicao()
                return self.reconhecer_real(numero)  # Chama a função para reconhecer números reais se encontrar um ponto
            elif not self.is_valid_in_language_not_in_numero(char):
                self.avancar_posicao()
            else:
                break
        
        qtd_char = len(numero)  # Calcula a quantidade de caracteres no nome
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)  # Limita a quantidade de caracteres depois do truncamento
        qtd_char_antes = max(qtd_char, qtd_char_depois)  # Limita a quantidade de caracteres antes do truncamento

        numero = ''.join(numero)[:LIMITE_QTD_CHAR]  # Junta os caracteres do nome em uma string e limita o tamanho

        # Retorna um dicionário com as informações do token
        return {"token": numero, 
                "linha": self.linha, 
                "tipo": "INT",  # Tipo do token (no caso, número inteiro)
                "codigo": "C03",  # Código do token
                "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes do truncamento
                "qtd_char_depois": qtd_char_depois}  # Quantidade de caracteres depois do truncamento}
       
    # Função para verificar se um caractere é válido na linguagem, mas não como parte de um nome
    def is_valid_in_language_not_in_real(self, char):
        # Conjunto de caracteres válidos
        not_valid_chars = set("ABCDFGHIJKLMNOPQRSTUVWXYZ_$ %():;?[]{}*/!=#<>")
        return char in not_valid_chars
    
    def reconhecer_real(self, numero):
        expoente_encontrado = False  # Flag para indicar se um expoente foi encontrado

        # Loop para percorrer o texto enquanto houver dígitos ou um ponto (parte decimal)
        while self.posicao < self.buffer_size and self.buffer[self.posicao] != '\n':
            char = self.buffer[self.posicao]

            if self.is_digit(char):
                numero.append(self.buffer[self.posicao])
                self.avancar_posicao()  # Avança para o próximo caractere
            elif char in ('E') and not expoente_encontrado:
                expoente_encontrado = True  # Marca que um expoente foi encontrado
                numero.append(self.buffer[self.posicao])
                self.avancar_posicao()  # Avança para o próximo caractere
                if self.posicao < self.buffer_size and self.buffer[self.posicao] in ('+', '-'):
                    numero.append(self.buffer[self.posicao])
                    self.avancar_posicao()  # Avança para o próximo caractere se for um sinal após o expoente
            elif not self.is_valid_in_language_not_in_real(char):
                self.avancar_posicao()
            else:
                break  # Sai do loop se o caractere não for um dígito, ponto ou parte do expoente

        
        qtd_char = len(numero)  # Calcula a quantidade de caracteres no nome
        qtd_char_depois = min(qtd_char, LIMITE_QTD_CHAR)  # Limita a quantidade de caracteres depois do truncamento
        qtd_char_antes = max(qtd_char, qtd_char_depois)  # Limita a quantidade de caracteres antes do truncamento

        numero = ''.join(numero)[:LIMITE_QTD_CHAR]  # Junta os caracteres do nome em uma string e limita o tamanho

        # Extrai a representação do número real do texto e limita o tamanho
        if qtd_char > LIMITE_QTD_CHAR:
            # Verifica se o número real truncado contém um ponto decimal e ajusta o tipo do símbolo
            if '.' in numero:
                if numero.endswith('.'):  # Se o ponto decimal estiver no final, o número é inteiro
                    qtd_char_depois = qtd_char_depois - 1  # Ajusta a quantidade de caracteres depois do truncamento
                    numero = numero[:qtd_char_depois]  # Extrai o número inteiro
                    tipo_simb = "INT"  # Define o tipo do símbolo como inteiro
                    codigo = "C03"  # Define o código para números inteiros
                else:
                    tipo_simb = "PFO"  # Se o ponto decimal não estiver no final, o número é real
                    codigo = "C04"  # Define o código para números reais
            else:
                tipo_simb = "INT"  # Se não houver ponto decimal, o número é inteiro
                codigo = "C03"  # Define o código para números inteiros
        else:
            numero = numero[:qtd_char_depois]  # Extrai o número real completo
            # Verifica se o número real completo contém um ponto decimal e ajusta o tipo do símbolo
            if numero.endswith('.'):
                qtd_char_depois = qtd_char_depois - 1  # Ajusta a quantidade de caracteres depois do truncamento
                numero = numero[:qtd_char_depois]  # Extrai o número inteiro
                tipo_simb = "INT"  # Define o tipo do símbolo como inteiro
                codigo = "C03"  # Define o código para números inteiros
            else:
                tipo_simb = "PFO"  # Se não houver ponto decimal, o número é real
                codigo = "C04"  # Define o código para números reais

        # Retorna um dicionário com as informações do token
        return {"token": numero, 
                "linha": self.linha,  
                "codigo": codigo,  # Código correspondente ao tipo do número (inteiro ou real)
                "tipo": tipo_simb,  # Tipo do token (inteiro ou real)
                "qtd_char_antes": qtd_char_antes,  # Quantidade de caracteres antes do truncamento
                "qtd_char_depois": qtd_char_depois}  # Quantidade de caracteres depois do truncamento
