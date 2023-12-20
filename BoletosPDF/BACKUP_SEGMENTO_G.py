import pandas as pd
from datetime import datetime
from boleto2 import processar_boleto


#FUNÇÃO PARA CALCULAR O DIGITOS VERIFICADORES 1,2,3
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


# Crie um DataFrame vazio para armazenar as informações
df_final = pd.DataFrame()


def processar_linha(nome_arquivo, linha, inscricao):
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
    numero_insc = linha[63:77]
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


    #CALCULANDO DIGITOS VERIFICADORES
    campo_livre1 = linha[36:41]
    campo_livre2 = linha[41:51]
    campo_livre3 = linha[51:61]

    dv = calcular_digito_verificador(f'{cod_banco2}{moeda}{campo_livre1}')
    dv2 = calcular_digito_verificador(campo_livre2)
    dv3 = calcular_digito_verificador(campo_livre3)

    Codigo_de_Barras = (f'{cod_banco2}{moeda}{campo_livre1}{dv}{campo_livre2}{dv2}{campo_livre3}{dv3}{dac}{vencimento}{valor}')


    #AGENCIA COBRADORA
    agencia = f'{ag_cobradora}-{dac2}'

    dados = {
        'Inscricao': [inscricao],
        'Codigo de Barras': [Codigo_de_Barras],
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



    #FORMATANDO A DATA DD/MM/AAAA
    data_obj = datetime.strptime(data_emissao, "%d%m%Y")
    data_emissao_formatada = data_obj.strftime("%d/%m/%Y")

    data_obj2 = datetime.strptime(vencimento_titulo, "%d%m%Y")
    data_vencimento_formatada = data_obj2.strftime("%d/%m/%Y")

    #FORMATANDO PARA FLOAT O VALOR
    valor_formatado = "{},{}".format(valor[:-2], valor[-2:])

    cnpj_gcp = "{}.{}.{}/{}-{}".format(
    inscricao[:2],
    inscricao[2:5],
    inscricao[5:8],
    inscricao[8:12],
    inscricao[12:]
    )

    cnpj_fornecedor = "{}.{}.{}/{}-{}".format(
    numero_insc[:2],
    numero_insc[2:5],
    numero_insc[5:8],
    numero_insc[8:12],
    numero_insc[12:]
    )

    dados_boleto ={
        'CNPJ GCP': [cnpj_gcp],
        'CNPJ FORNECEDOR': [cnpj_fornecedor],
        'RAZAO SOCIAL': [nome],
        'DATA EMISSAO': [data_emissao_formatada],
        'DATA VENCIMENTO': [data_vencimento_formatada],
        'VALOR': [valor_formatado],
        'DOCUMENTO': [n_documento],
        'LINHA DIGITAVEL': [Codigo_de_Barras]
    }

    global df_final
    df_atual = pd.DataFrame(dados_boleto)
    df_final = pd.concat([df_final, df_atual], ignore_index=True)
    df_final.to_excel(f'{nome_arquivo}_Boletos.xlsx', index=False)

    processar_boleto(cod_banco2, nome, n_documento, data_emissao_formatada, valor_formatado, data_vencimento_formatada, agencia, Codigo_de_Barras, carteira,data_limite, codigo_protesto,juros_mora,cnpj_gcp,especie_titulo,n_registro)


def segmento_g(nome_arquivo, numero_linha,inscricao_header_lote):
    with open(nome_arquivo, 'r') as arquivo_ret:
        for _ in range(numero_linha - 1):
            # Pular linhas até atingir a linha desejada
            arquivo_ret.readline()

        # Ler a linha desejada
        linha = arquivo_ret.readline()

        # Processar a linha
        processar_linha(nome_arquivo, linha,inscricao_header_lote)

