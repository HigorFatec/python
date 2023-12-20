import pandas as pd

# Crie um DataFrame vazio para armazenar as informações
df_final = pd.DataFrame()


def processar_linha(nome_arquivo, linha):
    cod_banco = linha[0:3] # 341
    cod_lote = linha[3:7] # 0001
    tipo_registro = linha[7:8] # 1
    operacao = linha[8:9] # I 
    cod_servico = linha[9:11] # 03
    zeros = linha[11:13]
    layout_lote = linha[13:16]
    brancos = linha[16:17]
    cod_inscricao = linha[17:18] # 1 - CPF , 2 - CNPJ
    inscricao = linha[19:33] # N° Inscrição da empresa
    convenio = linha[33:53] # Brancos
    agencia = linha[53:58] # Zeros
    digito_v = linha[58:59] #  Branco
    conta_corrente = linha[59:71] # Zeros
    dv_conta = linha[71:72] # BRANCO
    dv_agencia = linha[72:73] #BRANCO
    nome_empresa = linha[73:103] #Nome Empresa
    brancos2 = linha[103:240] #BRANCOS
    
    dados = {
        'Cod_banco': [cod_banco],
        'Cod_Lote': [cod_lote],
        'Tipo Registro': [tipo_registro],
        'Operacao': [operacao],
        'Codigo Servico': [cod_servico],
        'Complemento Registro': [zeros],
        'Layout': [layout_lote],
        'Complemento Registro': [brancos],
        'Tipo de Inscrição': [cod_inscricao],
        'Numero da Inscricao': [inscricao],
        'Convenio': [convenio],
        'Agencia': [agencia],
        'Digito Verificador Agencia': [digito_v],
        'Conta Corrente': [conta_corrente],
        'Digito Verificador Conta': [dv_conta],
        'Digito Verificador Agencia/Conta': [dv_agencia],
        'Nome Empresa': [nome_empresa],
        'Complemento de Registro': brancos2,
    }

    global df_final
    df_atual = pd.DataFrame(dados)
    df_final = pd.concat([df_final, df_atual], ignore_index=True)

    # Salvar o DataFrame em um arquivo Excel
    #df_final.to_excel(f'{nome_arquivo}_header_lote.xlsx', index=False)

    return inscricao


def header_lote(nome_arquivo, numero_linha):
    with open(nome_arquivo, 'r') as arquivo_ret:
        for _ in range(numero_linha - 1):
            # Pular linhas até atingir a linha desejada
            arquivo_ret.readline()

        # Ler a linha desejada
        linha = arquivo_ret.readline()