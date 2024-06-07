import pandas as pd

# Criar um DataFrame de exemplo
df = pd.read_excel('erro.xlsx')

# Garantir que a coluna tenha 11 caracteres, preenchendo com "0" à esquerda se necessário
df['RENAVAM'] = df['RENAVAM'].astype(str).str.zfill(11)

# Exibir o DataFrame resultante
print(df['RENAVAM'])


df.to_excel('erro2.xlsx', index=False)