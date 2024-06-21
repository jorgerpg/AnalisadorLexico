# Compilador
https://github.com/jorgerpg/AnalisadorLexico

## Descrição
Este projeto é um compilador simples implementado em Python, composto por dois componentes principais: um analisador léxico e um analisador sintático. No entanto, neste projeto, desenvolvido para a disciplina de compiladores, apenas o analisador léxico foi implementado. A gramática utilizada para o analisador léxico pode ser encontrada no repositório.

## Funcionalidades
- **Analisador Léxico:** Reconhece tokens no arquivo fonte e gera uma tabela de símbolos.
- **Analisador Sintático:** Utiliza a saída do analisador léxico para realizar análise sintática do código.

## Como usar
1. Certifique-se de ter o Python instalado em seu sistema.

2. Execute o script `staticChecker.py`, passando o nome do arquivo sem especificar a extensão (.241) como argumento. Por exemplo:

 Por exemplo:

    ``` 
    python staticChecker.py caminho_para_arquivo
    ```

 Ou utilize o executavel:
 
    ```
    staticChecker.exe caminho_para_arquivo
    ```

3. O analisador realizará a análise léxica e sintática do arquivo especificado, gerando os arquivos `.LEX` e `.TAB` no mesmo diretório do arquivo analisado.

## Requisitos
- Python 3

## Estrutura do Projeto
- `staticChecker.py`: Ponto de entrada do programa. Recebe o nome do arquivo como argumento de linha de comando e inicia a análise. Também contém a implementação do analisador sintático.
- `analisadorLexico.py`: Implementação do analisador léxico.

## Contribuições
Contribuições são bem-vindas! Se encontrar problemas ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.