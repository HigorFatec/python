import pandas as pd

# Crie um DataFrame vazio para armazenar as informações
df_final = pd.DataFrame()

def processar_linha(nome_arquivo, linha):
    cod_banco = linha[0:3]
    cod_lote = linha[4:8]
    tipo_registro = linha[7:8]
    brancos = linha[8:17]
    tipo_inscricao = linha[17:18] # 1 = CPF , 2 = CNPJ
    cnpj = linha[18:32]
    convenio = linha[32:52]
    agencia = linha[52:57]
    digito = linha[57:58]
    conta = linha[58:70]
    brancos4 = linha[70:71]
    digito_v = linha[71:72]
    nome_empresa = linha[72:102]
    nome_banco = linha[102:132]
    brancos5 = linha[132:142]
    arquivo_cod = linha[142:143]  # 1 = REMESSA , 2 = RETORNO

    #DATA_GERACAO
    data_geracao = linha[143:151]

    #HORA_GERACAO
    hora_geracao = linha[151:157]

    seq_arquivo = linha[157:163]
    layout = linha[163:166]
    brancos6 = linha[166:240]

    #print(brancos6)

    # Criar um DataFrame do pandas
    dados = {
        'Cod Banco': [cod_banco],
        'Cod Lote': [cod_lote],
        'Tipo Registro': [tipo_registro],
        'Complemento Registro': [brancos],
        'Tipo Inscrição': [tipo_inscricao],
        'CNPJ': [cnpj],
        'Convenio': [convenio],
        'Agência': [agencia],
        'Digito': [digito],
        'Conta': [conta],
        'Digito Verificador Conta': [brancos4],
        'Digito Verificador Agencia/Conta': [digito_v],
        'Nome Empresa': [nome_empresa],
        'Nome Banco': [nome_banco],
        'Complemento Registro': [brancos5],
        'Codigo do Arquivo': [arquivo_cod],
        'Data de Geração': [data_geracao],
        'Hora de Geração': [hora_geracao],
        'N° Sequencial do Arq': [seq_arquivo],
        'Densidade': [layout],
        'Complemento de Registro': [brancos6],
    }

    global df_final
    df_atual = pd.DataFrame(dados)
    df_final = pd.concat([df_final, df_atual], ignore_index=True)

    # Salvar o DataFrame em um arquivo Excel
    #df_final.to_excel(f'{nome_arquivo}_header_arquivo.xlsx', index=False)


def header_arquivo(nome_arquivo, numero_linha):
    with open(nome_arquivo, 'r') as arquivo_ret:
        for _ in range(numero_linha - 1):
            # Pular linhas até atingir a linha desejada
            arquivo_ret.readline()

        # Ler a linha desejada
        linha = arquivo_ret.readline()

        # Processar a linha
        processar_linha(nome_arquivo, linha)