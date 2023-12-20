import pandas as pd

def calcular_digito_verificador(numero):
    # Converte o número para uma lista de dígitos invertida
    digitos = [int(d) for d in str(numero)][::-1]

    # Inicializa a variável que armazenará a soma dos produtos
    soma = 0

    # Itera sobre os dígitos, aplicando os pesos sequencialmente da direita para a esquerda
    for i, digito in enumerate(digitos):
        peso = 2 if i % 2 == 0 else 1
        produto = digito * peso
        soma += produto if produto < 10 else produto - 9

    # Calcula o dígito verificador
    digito_verificador = (10 - (soma % 10)) % 10

     # Retorna 0 se o resultado do módulo for 0
    return 0 if digito_verificador == 0 else digito_verificador


with open('VS04123A.ret', 'r') as arquivo_ret:
    linha = arquivo_ret.readline()
    linha = arquivo_ret.readline()
    linha = arquivo_ret.readline()

cod_banco = linha[0:3] # 341
cod_lote = linha[3:7] # 0001
tipo_registro = linha[7:8] # 3
n_registro = linha[8:13] # 00001
segmento = linha[13:14] # G
brancos = linha[14:15] # complemento de registro
cod_mov = linha[15:17] # 01
cod_banco2 = linha[17:20] # 341
moeda = linha[20:21] #9
dac = linha[21:22] #5
vencimento = linha[22:26] #9558
valor = linha[26:36]
campo_livre = linha[36:61] # codigo de barras
cod_inscricao = linha[61:62] # 2 - CNPJ
numero_insc = linha[62:77]
nome = linha[77:107] # NOME DO CEDENTE
vencimento_titulo= linha[107:115] # DATA DE VENCIMENTO
valor_titulo = linha[115:130] # valor nonimal do titulo
moeda_qtd = linha[130:145]
cod_moeda = linha[145:147]
n_documento = linha[147:162]
ag_cobradora = linha[162:167] # agencia onde o titulo será cobrado
dac2 = linha[167:168] # DÍGITO VERIFICADOR DA AGÊNCIA COBRADORA
praca = linha[168:178] # BRANCOS
carteira = linha[178:179] # Modalidade de carteira
especie_titulo = linha[179:181]
data_emissao = linha[181:189] # Data de emissão do titulo
juros_mora = linha[189:204] # Juros de mora por dia de atraso
cod_desconto = linha[204:205] # codigo do 1° desconto
data_desconto = linha[205:213] # data limite do 1° desconto
valor_desconto = linha[213:228] # valor/percentual do 1° desconto
codigo_protesto = linha[228:229] # codigo para protesto
prazo_desconto = linha[229:231] # prazo para desconto
data_limite = linha[231:239] # data limite para pagamento
cod_juro_mora = linha[239:240] # codigo de juros de mora

campo_livre1 = linha[36:41]
campo_livre2 = linha[41:51]
campo_livre3 = linha[51:61]

codigo_barras2 = linha[41:47]
codigo_barras3 = linha[47:61]

dados = {
    'Cod_Banco': [cod_banco],
    'Cod_Lote': [cod_lote],
    'Tipo_Registro': [tipo_registro],
    'Numero_Registro': [n_registro],
    'Segmento': [segmento],
    'Complemento de Registro': [brancos],
    'Codigo de Movimento': [cod_mov],
    'Cod_Banco2': [cod_banco2],
    'Moeda': [moeda],
    'Digito Verificador(DAC)': [dac],
    'Fator_Vencimento': [vencimento],
    'Valor impresso no cod.barras': [valor],
    'Campo Livre cod.barras': [campo_livre],
    'Codigo Inscrição': [cod_inscricao],
    'Numero Inscricao do Cedente': [numero_insc],
    'Nome do Cedente': [nome],
    'Data de Vencimento do titulo': [vencimento_titulo],
    'Valor nonimal do titulo': [valor_titulo],
    'Quantidade de Moeda': [moeda_qtd],
    'Codigo da Moeda': [cod_moeda],
    'N° Documento': [n_documento],
    'Agencia Cobradora': [ag_cobradora],
    'Digito Verificador da Agencia Cobradora': [dac2],
    'Praça Cobradora': [praca],
    'Modalidade da Carteira': [carteira],
    'Especie do Titulo': [especie_titulo],
    'Data de Emissao do Titulo': [data_emissao],
    'Juros de Mora por Dias de Atraso': [juros_mora],
    'Codigo do 1° Desconto': [cod_desconto],
    'Data do 1° Desconto': [data_desconto],
    'Valor do 1° Desconto': [valor_desconto],
    'Codigo para Protesto': [codigo_protesto],
    'Prazo para Protesto': [prazo_desconto],
    'Data Limite para Pagamento': [data_limite],
    'Codigo do Juros de Mora': [cod_juro_mora],
}

print(f'CODIGO DE BARRAS: {campo_livre}')
print(f'CODIGO DE BARRAS 1: {campo_livre1}')
print(f'CODIGO DE BARRAS 2: {campo_livre2}')
print(f'CODIGO DE BARRAS 3: {campo_livre3}')
print(f'codigo_de_barras2: {codigo_barras2}')
print(f'codigo_de_barras_3:{codigo_barras3}')

dv = calcular_digito_verificador(f'{cod_banco2}{moeda}{campo_livre1}')

print(f'Dv 1: {dv}') # PRINTANDO O CALCULO DO PRIMEIRO DIGITO VERIFICADOR 


dv2 = calcular_digito_verificador(campo_livre2)

print(f'Dv 2: {dv2}')


dv3 = calcular_digito_verificador(campo_livre3)
print(f'Dv 3: {dv3}')

print(f'CODIGO BARRAS: {cod_banco2}{moeda}{dac}{vencimento}{valor}{campo_livre1}{codigo_barras2}{codigo_barras3}')

print(f'LINHA GERADA:   {cod_banco2}{moeda}{campo_livre1}{dv}{campo_livre2}{dv2}{campo_livre3}{dv3}{dac}{vencimento}{valor}')

print('LINHA ESPERADA: 74891123130258270710170725051026595480000029800')
#VALOR DO PRINT: 748911231302582707107072505102595480000029800
#VALOR ESPERADO: 74891123130258270710170725051026595480000029800

