import pandas as pd

df = pd.read_excel('IPVA.xlsx')

print(df['Documento'])

df['Documento'] = df['Documento'] + "/IPVA24"

print(df['Documento'])

#Salvar a planilha
df.to_excel('IPVA.xlsx', index=False)