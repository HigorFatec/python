import pandas as pd
import subprocess
import pyautogui
import os

# Obtém o diretório do executável
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Caminho relativo para o arquivo Excel
caminho_excel = os.path.join(diretorio_atual, 'conversao.xlsx')

pyautogui.alert("Bem vindo, certifique-se de que foi atualizado o arquivo 'conversao.xlsx'")

# Carregar o arquivo Excel
excel_file = pd.read_excel(caminho_excel)

# Definir o nome do arquivo de saída
output_txt = 'saida.txt'

# Caminho relativo para o arquivo de saída
caminho_saida_txt = os.path.join(diretorio_atual, output_txt)

# Converter e salvar como arquivo de texto
with open(caminho_saida_txt, 'w') as txt_file:
    for index, row in excel_file.iterrows():
        first_column = int(row[0])  # Converte apenas o valor da primeira coluna para inteiro
        second_column = str(row[1]).replace('.', ',')  # Substitui pontos por vírgulas na segunda coluna
        rest_of_columns = row[2:]   # Mantém as outras colunas como estão
        txt_file.write(f"{first_column},{second_column},{','.join(map(str, rest_of_columns))}\n")



pyautogui.alert("Arquivo de texto criado com sucesso.")