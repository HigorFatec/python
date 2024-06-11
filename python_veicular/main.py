import pandas as pd
from datetime import datetime

#função obter data
def get_day():
    # Obtém a data de hoje
    today = datetime.today()
    # Formata a data para o formato desejado (dia/mês/ano)
    formatted_date = today.strftime("%d/%m/%Y")
    #formatted_date = "25/04/2024"
    return formatted_date

print (get_day())

df = pd.read_excel('C:\\Users\\Usuário\\OneDrive - Cargo Polo Comercio Logistica e Transportes Eireli\\Painel Gerêncial\\6 - Base Forms ( Não Preencher Não Alterar)\\Check List _Inspeção Veicular.xlsx')
# Verifica se a data de avaliação é igual ao dia atual e a unidade é 'Ribeirão Preto'
df_filtered = df[(df['Data de Avaliação'] == get_day()) & (df['Unidade'] == 'Ribeirão Preto')]

#df_filtered = df[(df['Placas Ribeirão Preto'] == 'FPP8F94')]

if not df_filtered.empty:
    # DataFrame para armazenar os nomes das colunas com "NOK"
    df_colunas_nok = pd.DataFrame(columns=["Data de Avaliação","Placas Ribeirão Preto", "Nomes das Colunas","OBSERVAÇÕES:","Em caso de Nota abaixo de 4, justifique o motivo."])

    # Iterar sobre cada linha do DataFrame
    for index, row in df_filtered.iterrows():
        # Inicializar uma lista para armazenar os nomes das colunas com "NOK"
        colunas_nok = []
        # Iterar sobre cada coluna da linha
        for column in df.columns:
            # Verificar se o valor da célula é "NOK"
            if row[column] == "NOK":
                # Adicionar o nome da coluna à lista
                colunas_nok.append(column)


        # Criar um novo DataFrame com os dados da linha atual
        new_row = pd.DataFrame({"Data de Avaliação":[row["Data de Avaliação"]],"Placas Ribeirão Preto": [row["Placas Ribeirão Preto"]], "Nomes das Colunas": [colunas_nok], "OBSERVAÇÕES:":[row["OBSERVAÇÕES:"]], "Em caso de Nota abaixo de 4, justifique o motivo.":[row["Em caso de Nota abaixo de 4, justifique o motivo."]]})
        # Concatenar o novo DataFrame ao DataFrame principal
        df_colunas_nok = pd.concat([df_colunas_nok, new_row], ignore_index=True)

    # Renomear as colunas do DataFrame
    df_colunas_nok.rename(columns={"Data de Avaliação":"Data", "Placas Ribeirão Preto":"Placas", "Nomes das Colunas":"Defeitos", "OBSERVAÇÕES:":"OBSERVAÇÕES:", "Em caso de Nota abaixo de 4, justifique o motivo.":"Justificativa"}, inplace=True)

    df_colunas_nok['Defeitos'] = df_colunas_nok['Defeitos'].astype(str)
    df_colunas_nok['Defeitos'] = df_colunas_nok['Defeitos'].apply(lambda x: ', '.join(x))
    df_colunas_nok['Defeitos'] = df_colunas_nok['Defeitos'].str.replace('[, ]','')
    df_colunas_nok['Defeitos'] = df_colunas_nok['Defeitos'].str.replace(', ','')

   
    df_colunas_nok = df_colunas_nok.dropna(subset=['Defeitos'])

    #print(df_colunas_nok["Defeitos"])

    # Salvar o DataFrame em um arquivo Excel
    df_colunas_nok.to_excel('colunas_nok.xlsx', index=False)

    #print(df_colunas_nok)

#FPP8F94