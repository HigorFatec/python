from datetime import datetime
import pandas as pd

with open('VS04123C.ret', 'r') as arquivo_ret:
    linha = arquivo_ret.readline()
    linha2 = arquivo_ret.readline()

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
data_obj = datetime.strptime(data_geracao, '%d%m%Y')
data_formatada = data_obj.strftime('%d/%m/%Y')

#HORA_GERACAO
hora_geracao = linha[151:157]
hora_obj = datetime.strptime(hora_geracao, '%H%M%S')
hora_formatada = hora_obj.strftime('%H:%M:%S')

seq_arquivo = linha[157:163]
layout = linha[163:166]
brancos6 = linha[166:240]

#print(brancos6)

# Criar um DataFrame do pandas
dados = {
    'Cod Banco': [cod_banco],
    'Cod Lote': [cod_lote],
    'Tipo Registro': [tipo_registro],
    'Tipo Inscrição': [tipo_inscricao],
    'CNPJ': [cnpj],
    'Convenio': [convenio],
    'Agência': [agencia],
    'Digito': [digito],
    'Conta': [conta],
    'Digito Verificador': [digito_v],
    'Nome Empresa': [nome_empresa],
    'Nome Banco': [nome_banco],
    'Codigo do Arquivo': [arquivo_cod],
    'Data de Geração': [data_formatada],
    'Hora de Geração': [hora_formatada],
    'N° Sequencial do Arq': [seq_arquivo],
    'Densidade': [layout],
}

df = pd.DataFrame(dados)


cod_banco = linha2[0:3] # 341
cod_lote = linha2[3:7] # 0001
tipo_registro = linha2[7:8] # 1
operacao = linha2[8:9] # I 
cod_servico = linha2[9:11] # 03
zeros = linha2[11:13]
layout_lote = linha2[13:16]
brancos = linha2[16:17]
cod_inscricao = linha2[17:18] # 1 - CPF , 2 - CNPJ
inscricao = linha2[18:33] # N° Inscrição da empresa
convenio = linha2[33:53] # Brancos
agencia = linha2[53:58] # Zeros
digito_v = linha2[58:59] #  Branco
conta_corrente = linha2[59:71] # Zeros
dv_conta = linha2[71:72] # BRANCO
dv_agencia = linha2[72:73] #BRANCO
nome_empresa = linha2[73:103] #Nome Empresa
brancos2 = linha2[103:240] #BRANCOS

dados2 = {
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
df2 = pd.DataFrame(dados2)

# Salvar o DataFrame em um arquivo Excel
df2.to_excel('DDA-Dados.xlsx', sheet_name='header_lote', index=False)

# Salvar ambos os DataFrames em um arquivo Excel com duas folhas
with pd.ExcelWriter('DDA-Dados.xlsx') as writer:
    df.to_excel(writer, sheet_name='header_arq', index=False)
    df2.to_excel(writer, sheet_name='header_lote', index=False)

    
print(brancos)
