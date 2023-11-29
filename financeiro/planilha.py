import pandas as pd
import os

# Supondo que df, df_gnre e df_cgp têm as colunas 'CNPJ', 'SERIE', 'FILIAL', respectivamente
df = pd.read_excel('Lacamento GNRE.xlsx', sheet_name='FILIAL')
df_gnre = pd.read_excel('Controle GNRE Dadazio.xlsx', sheet_name='GNRE PAGAS')
df_cgp = pd.read_excel('Controle GNRE Cargo Polo.xlsx', sheet_name='GNRE PAGAS')

# Concatenar df_gnre e df_cgp
df_concatenado = pd.concat([df_gnre, df_cgp], ignore_index=True).dropna()

# Selecionar colunas relevantes de df_concatenado
df_resultado = df_concatenado[['CNPJ Contribuinte', 'Período','Nº Documento' ,'Série', 'Valor Total']]

# Remova a formatação dos CNPJs em ambas as colunas
df_resultado['CNPJ Contribuinte'] = df_resultado['CNPJ Contribuinte'].str.replace(r'\D', '', regex=True)
df['CNPJ'] = df['CNPJ'].astype(str).str.replace(r'\D', '', regex=True)


# Mesclar df_resultado com df para obter a coluna 'FILIAL'
df_resultado = pd.merge(df_resultado, df[['CNPJ', 'SERIE', 'FILIAL']], left_on=['CNPJ Contribuinte', 'Série'], right_on=['CNPJ', 'SERIE'], how='left')

# Renomear a coluna 'FILIAL' resultante para 'FILIAL_RESULTADO'
df_resultado = df_resultado.rename(columns={'FILIAL': 'FILIAL_RESULTADO'})

# Remover as colunas temporárias 'CNPJ' e 'SERIE' adicionadas pela mesclagem
df_resultado = df_resultado.drop(['CNPJ', 'SERIE'], axis=1)

df_resultado['Nº Documento'] = df_resultado['Nº Documento'].astype(int)
df_resultado['Série'] = df_resultado['Série'].astype(int)

df_resultado['Valor Total'] = df_resultado['Valor Total'].astype(str)
df_resultado['Valor Total'] = df_resultado['Valor Total'].str.replace('.', ',')

#CRIANDO COLUNA PARA RETIRAR BUGS
#df_resultado['TIRAR_ESPACO'] = '0'

#removendo os espaços em branco (' ')
df_resultado = df_resultado.applymap(lambda x: x.strip() if isinstance(x, str) else x)


#print(df_gnre.columns)

# Para imprimir o DataFrame resultante
print(df_resultado)

# Para salvar o DataFrame resultante em um arquivo Excel
df_resultado.to_excel('resultado.xlsx', index=False)


#######################  TXT ########################################
# Obtém o diretório do executável
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Definir o nome do arquivo de saída
output_txt = 'saida.txt'

# Caminho relativo para o arquivo de saída
caminho_saida_txt = os.path.join(diretorio_atual, output_txt)

# Converter e salvar como arquivo de texto
with open(caminho_saida_txt, 'w') as txt_file:
    for index, row in df_resultado.iterrows():
        txt_file.write(';'.join(map(str, row)) + '\n')
        
######################## FIIM ##########################################
