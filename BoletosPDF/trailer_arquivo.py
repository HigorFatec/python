import datetime
import pandas as pd

#SEGMENTO H

# Crie um DataFrame vazio para armazenar as informações
df_final = pd.DataFrame()

def processar_linha(nome_arquivo, linha):
    cod_banco = linha[0:3] # 341
    cod_lote = linha[3:7]
    registro = linha[7:8]
    complemento_registro = linha[8:17]
    quantidade_lotes = linha[17:23]
    total_registros = linha[23:29]
    complemento_registro2 = linha[29:240]
    segmento = registro

    dados = {
        'Cod_Banco': [cod_banco],
        'Cod_Lote': [cod_lote],
        'Registro': [registro],
        'Complemento Registro': [complemento_registro],
        'Quantidade Lotes do Arquivo': [quantidade_lotes],
        'Total de Registros': [total_registros],
        'Complemento Registro 2': [complemento_registro2]

    }


    global df_final
    df_atual = pd.DataFrame(dados)
    df_final = pd.concat([df_final, df_atual], ignore_index=True)

    #df_final.to_excel(f'{nome_arquivo}_trailer_arquivo.xlsx',index=False)


def trailer_arquivo(nome_arquivo, numero_linha):
    with open(nome_arquivo, 'r') as arquivo_ret:
        for _ in range(numero_linha - 1):
            # Pular linhas até atingir a linha desejada
            arquivo_ret.readline()

        # Ler a linha desejada
        linha = arquivo_ret.readline()

        # Processar a linha
        processar_linha(nome_arquivo, linha)

