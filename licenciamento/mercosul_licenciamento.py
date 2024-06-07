import pandas as pd

# Criando um DataFrame de exemplo
df = pd.read_excel('licenciamento2.xlsx')

# Função para transformar placas para o formato Mercosul
def substituir_quinto_caractere(digito):
    substituicoes = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E', '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J'}
    return substituicoes.get(digito, digito)

def transformar_para_mercosul(placa):
    if pd.notna(placa) and isinstance(placa, str) and len(placa) == 7 and placa[4].isnumeric():
        # Substitui o quinto caractere de acordo com a regra fornecida
        return placa[:4] + substituir_quinto_caractere(placa[4]) + placa[5:]
    elif len(placa) == 8 and placa[:3].isalpha() and placa[3:].isnumeric():
        return f'{placa[:3]}-{placa[3:]}'
    return placa  # Retorna a placa original se a transformação não puder ser aplicada

# Aplicando a função à coluna 'Placas'
df['Placas'] = df['Documento'].apply(transformar_para_mercosul)

#Salvar a planilha
df.to_excel('licenciamento2.xlsx', index=False)

# Exibindo o DataFrame resultante
print(df)
