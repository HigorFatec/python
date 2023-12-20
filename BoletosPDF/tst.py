import pandas as pd


df = pd.read_excel('Boletos.xlsx')

df_filtrado = df[(df['CONFERE'] == 'ERRO') & (df['LANCADO RODOPAR'] == 'OK')]

# Reinicia os índices
df_filtrado = df_filtrado.reset_index(drop=True)

df_filtrado['Indice'] = df_filtrado.index

print(df_filtrado)

# Solicita ao usuário que insira o índice da linha
indice_linha = int(input("Digite o índice da linha que deseja executar: "))

# Verifica se o índice é válido
if indice_linha < 0 or indice_linha >= len(df_filtrado):
    print("Índice inválido. Saindo do programa.")
    exit()
    
# Obtém a linha específica do DataFrame
linha_selecionada = df_filtrado.iloc[indice_linha]

print (linha_selecionada)

cod_rodopar = linha_selecionada['COD. RODOPAR']

print (cod_rodopar)