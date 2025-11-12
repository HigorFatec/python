from datetime import datetime
import time
import requests
import pandas as pd
import requests
import pandas as pd
import json
import pyodbc
import numpy as np
import schedule



def sql_server():

    # Configuração da conexão com o SQL Server
    SERVER = '177.47.20.123,1433'
    DATABASE = 'db_visual_rodopar'
    USERNAME = 'cyber'
    PASSWORD = 'bycyber'
    connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    conn = pyodbc.connect(connectionString)

    cursor = conn.cursor()

    # Ler o arquivo Excel para um DataFrame
    df = pd.read_excel('resultados.xlsx')

    total = 0

    # Mostrar as primeiras linhas para verificar o conteúdo
    # print(df.head())

    # Exemplo de substituição de NaN para valores válidos
    df['GRU_VALOR'] = df['GRU_VALOR'].fillna(0.0)
    df['RENAVAM'] = df['RENAVAM'].astype(str)
    df['GRU_VALOR'] = df['GRU_VALOR'].astype(str)

    # Converter todas as colunas para object, exceto 'GRU_ERRO'
    df.loc[:, df.columns != 'GRU_ERRO'] = df.loc[:, df.columns != 'GRU_ERRO'].apply(
        lambda col: col.astype(object).where(col.notna(), None)
    )

    # Garantir que 'GRU_ERRO' continue como BIT (0 ou 1)
    df['GRU_ERRO'] = df['GRU_ERRO'].fillna(1).astype(int)

    cursor.execute("""
        DELETE FROM WS_CRONOTACOGRAFO""")
    
    conn.commit()


    # Iterar sobre as linhas do DataFrame e inserir os dados na tabela
    for index, row in df.iterrows():
        #print(f"Inserindo linha {index}: {row.to_dict()}")  # Debug dos valores


        cursor.execute("""
            INSERT INTO WS_CRONOTACOGRAFO (
                RENAVAM, PLACA, VENCIMENTO, STATUS, EMISSAO, DOCUMENTO, DOCUMENTO_N, GRU_N, MARCA, MODELO, SERIE,
                GRU_ERRO, GRU_ERRO_MENSAGEM, GRU_PAGAMENTO, GRU_EMISSAO, GRU_VENCIMENTO, GRU_VALOR,
                DATA_PESQUISA_GRU, CERTIFICADO, GRU_URL, LINHA_DIGITAVEL, DATA_PAGAMENTO_GRU, PESQUISADO_EM
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
        """, 
        row['RENAVAM'], row['PLACA'], row['VENCIMENTO'], row['STATUS'], row['EMISSAO'], row['DOCUMENTO'], 
        row['DOCUMENTO_N'], row['GRU_N'], row['MARCA'], row['MODELO'], row['SERIE'], row['GRU_ERRO'], 
        row['GRU_ERRO_MENSAGEM'], row['GRU_PAGAMENTO'], row['GRU_EMISSAO'], row['GRU_VENCIMENTO'], 
        row['GRU_VALOR'], row['DATA_PESQUISA_GRU'], row['CERTIFICADO'], row['GRU_URL'], row['LINHA_DIGITAVEL'], 
        row['DATA_PAGAMENTO_GRU'], row['PESQUISADO_EM'])

        total = total + 1



    # Commit para salvar as alterações
    conn.commit()

    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()

    print("Dados inseridos com sucesso!")

    print("\n")
    print("\n")
    print(f"Foram feito um total de {total} inserts!")
    print("\n")
    print("\n")


def espacos_em_branco():

    df = pd.read_excel('resultados.xlsx')
    print(df)
        # Converter a coluna VENCIMENTO para formato de data
    df['VENCIMENTO_DATA'] = pd.to_datetime(df['VENCIMENTO'], dayfirst=True, errors='coerce')

    # Remover linhas com RENAVAM e SERIE nulos
    df = df.dropna(how='all')

    # Ordenar pelo maior vencimento
    df = df.sort_values(by='VENCIMENTO_DATA', ascending=False)

    # Remover duplicados, mantendo o de maior vencimento
    df = df.drop_duplicates(subset=['PLACA'], keep='first')

    df = df.drop(columns=['VENCIMENTO_DATA'])

    df.to_excel('resultados.xlsx',index=False)


def obter_tacografo():

    # Carregar o DataFrame a partir do arquivo Excel (ou outra fonte)
    df = pd.read_excel("resposta.xlsx", dtype={"RENAVAM": str})  # Garantir que RENAVAM seja string

    # Verificar se a coluna RENAVAM existe no DataFrame
    if "RENAVAM" not in df.columns:
        raise ValueError("A coluna 'RENAVAM' não existe no DataFrame.")

    # Definir a URL do endpoint da API
    url = "https://sistema.smartec.com.br/api/Cronotacografo"

    # Definir os headers
    headers = {
        "Content-Type": "application/json"
    }

    # Lista para armazenar os resultados
    resultados = []

    # Iterar sobre todos os RENAVAMs do DataFrame
    for renavam in df["RENAVAM"]:
        payload = {
            "Renavam": str(renavam),  # Garantir que o RENAVAM seja string
            "Tipo": "CONSULTAR",
            "Token": "QXDDhQWEy7FXJgKCv3yR39WjUYgDZTnHPxnDfuqeur5pb"  # Substitua pelo token correto
        }

        # Fazer a requisição POST
        response = requests.post(url, json=payload, headers=headers)

        # Verificar a resposta
        if response.status_code == 200:
            resposta = response.json()
            # print(f"Resposta para RENAVAM {renavam}: {resposta}")

            # Verificar se a resposta é uma lista e pegar o primeiro elemento
            if isinstance(resposta, list) and resposta:
                resposta = resposta[0]  # Pega o primeiro item da lista

            resultados.append({"RENAVAM": renavam, **resposta})  # Expandir o JSON para colunas
        else:
            print(f"Erro para RENAVAM {renavam}: {response.status_code}, {response.text}")
            resultados.append({"RENAVAM": renavam, "Erro": response.text})

    # Criar um DataFrame com os resultados
    df_resultados = pd.DataFrame(resultados)

    # Salvar os resultados em um arquivo Excel
    df_resultados.to_excel("resultados.xlsx", index=False, engine="openpyxl")

    print("Consulta finalizada! Resultados salvos em 'resultados.xlsx'.")


def obter_veiculos():
    # Defina a URL do endpoint da API
    url = "https://sistema.smartec.com.br/api/Veiculo"  # Substitua pela URL correta

    # Defina o payload com os dados necessários
    payload = {
        "Tipo": "CADASTRADOS",       # Ou "ORGAOS BANCOS" / "ATUALIZAR"
        "Token": "QXDDhQWEy7FXJgKCv3yR39WjUYgDZTnHPxnDfuqeur5pb"  # Substitua pelo seu token de autenticação
    }

    # Defina os headers, se necessário
    headers = {
        "Content-Type": "application/json"
    }

    # Faça a requisição POST
    response = requests.post(url, json=payload, headers=headers)

    # Verifique a resposta
    if response.status_code == 200:
        print("Resposta da API:", response.json())  # Caso a resposta seja JSON

        data = response.json()

        if isinstance(data, list):  # Verifica se a resposta é uma lista de dicionários
            df = pd.DataFrame(data)  # Converte para DataFrame

            # Filtrar — manter apenas os que NÃO são dos tipos abaixo
            tipos_excluir = ['AUTOMÓVEL', 'CAMINHONETE', 'CAMIONETA', 'UTILITÁRIO']
            df = df[~df['TIPO'].isin(tipos_excluir)]

            df.to_excel("resposta.xlsx", index=False)  # Salva no arquivo Excel
            print("Arquivo salvo como resposta.xlsx")
        else:
            print("A resposta da API não está no formato esperado (lista de dicionários).")
        
    else:
        print("Erro na requisição:", response.status_code, response.text)


def job():
    try:
        obter_veiculos()
        obter_tacografo()
        espacos_em_branco()
        sql_server()
        
        print(f"Executado com sucesso às {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except:
        print("Erro ao executar o job")

job()

# Agendar a tarefa diária às 8:30 AM
schedule.every().day.at("08:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
