import datetime
import pandas as pd

# Crie um DataFrame vazio para armazenar as informações
df_final = pd.DataFrame()


#TRAILER_LOTE
def processar_linha(nome_arquivo, linha):
    cod_banco = linha[0:3] # 341
    cod_lote = linha[3:7]
    tipo_registro = linha[7:8]
    complemento_registro = linha[8:17]
    quantidade_registro = linha[17:23]
    valor_titulos = linha[23:41]
    quantidade_moeda = linha[41:59]
    complemento_registro2 = linha[59:240]

    dados = {
        'Cod_Banco': [cod_banco],
        'Cod_Lote': [cod_lote],
        'Tipo Registro': [tipo_registro],
        'Complemento Registro': [complemento_registro],
        'Quantidade de Registro': [quantidade_registro],
        'Valor dos Titulos': [valor_titulos],
        'Quantidade de Moeda': [quantidade_moeda],
        'Complemento de Registro': [complemento_registro2]
    }

    global df_final
    df_atual = pd.DataFrame(dados)
    df_final = pd.concat([df_final, df_atual], ignore_index=True)

    # Agora, após processar todas as linhas, salve o DataFrame final em um único arquivo Excel
    #df_final.to_excel(f'{nome_arquivo}_trailer_lote.xlsx', index=False)


def trailer_lote(nome_arquivo, numero_linha):
    with open(nome_arquivo, 'r') as arquivo_ret:
        for _ in range(numero_linha - 1):
            # Pular linhas até atingir a linha desejada
            arquivo_ret.readline()

        # Ler a linha desejada
        linha = arquivo_ret.readline()

        # Processar a linha
        processar_linha(nome_arquivo, linha)