import pandas as pd

df = pd.read_excel('data.xlsx')

print(df['Documento'])

df['Documento'] = df['Documento'] + "/IPVA24"

#Salvar a planilha
df.to_excel('data.xlsx', index=False)