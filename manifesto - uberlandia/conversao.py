import pandas as pd
import subprocess
import pyautogui
import os

# Obtém o diretório do executável
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Caminho relativo para o arquivo Excel
caminho_excel = os.path.join(diretorio_atual, 'manifesto.xlsx')

pyautogui.alert("Bem vindo, certifique-se de que foi atualizado o arquivo 'manifesto.xlsx' \n DT - linha - codigo\n Criado por: ☯☠ Michel Lopes ☯☠")

# Carregar o arquivo Excel
excel_file = pd.read_excel(caminho_excel)

# Definir o nome do arquivo de saída
output_txt = 'saida.txt'

# Caminho relativo para o arquivo de saída
caminho_saida_txt = os.path.join(diretorio_atual, output_txt)

# Converter e salvar como arquivo de texto
with open(caminho_saida_txt, 'w') as txt_file:
    for index, row in excel_file.iterrows():
        txt_file.write(','.join(map(str, row)) + '\n')

print(f"Arquivo de texto '{caminho_saida_txt}' criado com sucesso.")
