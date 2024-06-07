import pandas as pd
import subprocess
import pyautogui
import os

# Obtém o diretório do executável
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Caminho relativo para o arquivo Excel
caminho_excel = os.path.join(diretorio_atual, 'licenciamento2.xlsx')

pyautogui.alert("Bem vindo, certifique-se de que foi atualizado o arquivo 'manifesto.xlsx' \n DT - linha - codigo\n Criado por: ☯☠ HigorMachado ☯☠")

# Carregar o arquivo Excel
excel_file = pd.read_excel(caminho_excel)


excel_file['VENCIMENTO'] = pd.to_datetime(excel_file['VENCIMENTO'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')

# excel_file['VENCIMENTO.1'] = pd.to_datetime(excel_file['VENCIMENTO.1'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')

# excel_file['VENCIMENTO.2'] = pd.to_datetime(excel_file['VENCIMENTO.2'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')

# excel_file['VENCIMENTO.3'] = pd.to_datetime(excel_file['VENCIMENTO.3'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')

# excel_file['VENCIMENTO.4'] = pd.to_datetime(excel_file['VENCIMENTO.4'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')




# Definir o nome do arquivo de saída
output_txt = 'saida.txt'

# Caminho relativo para o arquivo de saída
caminho_saida_txt = os.path.join(diretorio_atual, output_txt)

# Converter e salvar como arquivo de texto
with open(caminho_saida_txt, 'w') as txt_file:
    for index, row in excel_file.iterrows():
        txt_file.write(';'.join(map(str, row)) + '\n')

print(f"Arquivo de texto '{caminho_saida_txt}' criado com sucesso.")