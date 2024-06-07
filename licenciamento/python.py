import pandas as pd

df = pd.read_excel('licenciamento2.xlsx')

# print(df['Documento'])

df['Documento'] = df['Documento'] + "/LIC24"

print(df['Documento'])

#df['Placas'] = df['Documento'].str.split('/').str[0]


# #Salvar a planilha
df.to_excel('licenciamento2.xlsx', index=False)