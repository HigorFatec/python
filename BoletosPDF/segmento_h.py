from datetime import datetime
import pandas as pd
import datetime

# Crie um DataFrame vazio para armazenar as informações
df_final = pd.DataFrame()

#SEGMENTO H
def processar_linha(nome_arquivo, linha):
    cod_banco = linha[0:3] # 341
    cod_lote = linha[3:7] # 0001
    tipo_registro = linha[7:8] # 3
    n_registro = linha[8:13]
    segmento = linha[13:14]
    complemento_registro = linha[14:15]
    movimento = linha[15:17]
    codigo_sacador = linha[17:18]
    insc_numero = linha[18:33]
    sacador = linha[33:73]
    cod_2desconto = linha[73:74]
    data_2desconto = linha[74:82]
    valor_2desconto = linha[82:97]

    cod_3desconto = linha[97:98]
    data_3desconto = linha[98:106]
    valor_3desconto = linha[106:121]

    cod_multa = linha[121:122]
    data_multa = linha[122:130]
    multa = linha[130:145]
    abatimento = linha[145:160]
    instrucao_1 = linha[160:200]
    instrucao_2 = linha[200:240]

    dados = {
        'Cod_Banco': [cod_banco],
        'Cod_Lote': [cod_lote],
        'Tipo_Registro': [tipo_registro],
        'Numero Registro': [n_registro],
        'Segmento': [segmento],
        'Complemento Registro': [complemento_registro],
        'Cod_Movimento': [movimento],
        'Tipo de Inscrição do Sacador': [codigo_sacador],
        'N° de Inscrição do Sacador' : [insc_numero],
        'Nome do Sacador': [sacador],
        'Codigo do 2° Desconto': [cod_2desconto],
        'Data do 2° Desconto': [data_2desconto],
        'Valor do 2° Desconto': [valor_2desconto],
        'Codigo do 3° Desconto': [cod_3desconto],
        'Data do 3° Desconto': [data_3desconto],
        'Valor do 3° Desconto': [valor_3desconto],
        'Codigo da Multa': [cod_multa],
        'Data da Multa': [data_multa],
        'Valor/Percentual da Multa': [multa],
        'Valor abatido a ser Concedido': [abatimento],
        'INSTRUCAO 1': [instrucao_1],
        'INSTRUCAO 2': [instrucao_2],
    }

    global df_final
    df_atual = pd.DataFrame(dados)
    df_final = pd.concat([df_final, df_atual], ignore_index=True)

    #df_final.to_excel(f'{nome_arquivo}_Segmento_H.xlsx', index=False)

def segmento_h(nome_arquivo, numero_linha):
    with open(nome_arquivo, 'r') as arquivo_ret:
        for _ in range(numero_linha - 1):
            # Pular linhas até atingir a linha desejada
            arquivo_ret.readline()

        # Ler a linha desejada
        linha = arquivo_ret.readline()

        # Processar a linha
        processar_linha(nome_arquivo, linha)