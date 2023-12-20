# This Python file uses the following encoding: utf-8
"""
Grupo SELCO
Programa para emissão de boleto bancário via PDF
Dependência: reportlab, rlbarcode, python-devel
Por: Armando Roque Ferreira Pinto
Inicio: 22/09/2006 Término 25/09/2006

Medidas expressas em mm (milimetros)

Agradecimentos ao Luciano Pacheco da lista Python-Brasil por ter visto o erro do método image no Canvas.

Para inscrever na lista envie um e-mail para
python-br-subscribe@yahoogroups.com.br
e confirme a inscrição com o e-mail

Atualizações
Autor    Data       Descrição
Armando  25/09/2006 

"""

# imports
from reportlab.graphics import renderPDF
from reportlab.graphics import shapes
from reportlab.graphics.shapes import *
from reportlab.graphics.shapes import Image, Drawing
from reportlab.graphics.barcode.common import *

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

from reportlab.pdfgen.canvas import Canvas

from reportlab.platypus import Paragraph, Frame

import string
import pandas as pd
from datetime import datetime
import os

# Constantes
# Formulário
FONTE_FORM='Helvetica'
FONTE_FORM_TAM=6

FONTE_FORM_TAM_ID=10

FONTE_DADOS='Times-Roman'
FONTE_DADOS_TAM=10


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



def processar_boleto(cod_banco2, nome, n_documento, data_emissao_formatada, valor_formatado, data_vencimento_formatada, agencia, Codigo_de_Barras, carteira,data_limite, codigo_protesto,juros_mora,cnpj_gcp,especie_titulo,n_registro,cod_barras):
  #Global Banco, empresa e cedente (Default Banco do Brasil)
  banco=cod_banco2
  localpagamento='Pague este título preferencialmente nas agências do '
  cedente= nome
  telefone_empresa='(16)3512-2350'
  sacado='GRUPO CARGO POLO'
  endereco='R. Armando Tarozo, 25, 25'
  endereco1= cnpj_gcp

  #Boleto
  documento= n_documento
  emissao= data_emissao_formatada
  valor= valor_formatado
  vencimento= data_vencimento_formatada

  aceite='S'
  especiedoc='DM'
  especiemon='R$'

  agencia= agencia

  carteira= carteira
  nossonumero= n_registro

  valorexpresso='Valores expressos em Real(is)'
  juros=f'Especie do Titulo: {especie_titulo}'
  observacao1=f'Juros de mora por dias de Atraso: {juros_mora}'
  observacao2=f'Código protesto: {codigo_protesto}'
  observacao3=f'Data limite para pagamento: {data_limite}'

  usobanco=''
  linhadigitavel= Codigo_de_Barras
  codigobarra=cod_barras
  

  formboleto(banco, documento, emissao, valor_formatado, data_vencimento_formatada, agencia, linhadigitavel, carteira,telefone_empresa,sacado,endereco,endereco1,valor,vencimento,cedente,especiedoc,aceite,especiemon,nossonumero,valorexpresso,juros,observacao1,observacao2,observacao3,codigobarra,localpagamento,usobanco)

def formboleto(banco, n_documento, data_emissao_formatada, valor_formatado, data_vencimento_formatada, agencia, Codigo_de_Barras, carteira,telefone_empresa,sacado,endereco,endereco1,valor,vencimento,cedente,especiedoc,aceite,especiemon,nossonumero,valorexpresso,juros,observacao1,observacao2,observacao3,codigobarra,localpagamento,usobanco):

  vencimento = data_vencimento_formatada
  valor = valor_formatado
  emissao = data_emissao_formatada
  documento = n_documento
  linhadigitavel = Codigo_de_Barras

  boleto=Canvas(f'BOLETO/boleto{codigobarra}.pdf')
  
  # Logomarca da empresa
  boleto.drawImage(image='./BOLETO/logos/empresa.jpeg', x=7*mm, y=280*mm, width=30*mm, height=11*mm)
  
  boleto.setStrokeColor(colors.black)
  boleto.setLineWidth(0.1)
  boleto.setFont('Helvetica-Bold',14)
  #global localpagamento, usobanco, impressora
  
  
  if banco=='237':
    # bradesco
    boleto.drawImage(image='./BOLETO/logos/bancobradesco.jpg',x=160*mm, y=280*mm, width=25*mm, height=8*mm)
    
    # imagem do recido do sacado
    boleto.drawImage(image='./BOLETO/logos/bancobradesco.jpg',x=7*mm, y=229*mm, width=25*mm, height=8*mm)
    
    # imagem do banco na ficha de compensação
    boleto.drawImage(image='./BOLETO/logos/bancobradesco.jpg',x=7*mm, y=112*mm, width=25*mm, height=8*mm)
    
    # codigo do banco
    boleto.drawString(43*mm, 229*mm, '237-9')
    boleto.drawString(43*mm, 112*mm, '237-9')
    
    localpagamento+='Banco BRADESCO S/A'
    
    usobanco='269'
    #LINHADIGITAVEL='2379.264712 90600.000336 23007.514005 5 33070000011402'
    #CODIGOBARRA='23795330700000114022647190600000332300751400'
  
  elif banco=='422':
    # safra
    boleto.drawImage(image='./BOLETO/logos/bancosafra.jpg',x=160*mm, y=275*mm, width=32*mm, height=7*mm)
    
    # imagem do recido do sacado
    boleto.drawImage(image='./BOLETO/logos/bancosafra.jpg',x=7*mm, y=229*mm, width=30*mm, height=6*mm)
    
    # imagem do banco na ficha de compensação
    boleto.drawImage(image='./BOLETO/logos/bancosafra.jpg',x=7*mm, y=112*mm, width=30*mm, height=6*mm)
    
    # codigo do banco
    boleto.drawString(43*mm, 229*mm, '422-7')
    boleto.drawString(43*mm, 112*mm, '422-7')
  
    localpagamento+='Banco SAFRA'

  elif banco =='341':
     boleto.drawImage(image='./BOLETO/logos/bancodoitau.jpg',x=160*mm, y=280*mm, width=25*mm,height= 10*mm)

     boleto.drawImage(image='./BOLETO/logos/bancodoitau.jpg',x=7*mm,y=229*mm,width=25*mm,height=10*mm)

     boleto.drawImage(image='./BOLETO/logos/bancodoitau.jpg',x=7*mm, y=112*mm,width=25*mm, height=10*mm)

     # codigo do banco
     boleto.drawString(43*mm, 229*mm, '422-7')
     boleto.drawString(43*mm, 112*mm, '422-7')
  
     localpagamento+='Banco ITAU'

  elif banco == '001':    
    # banco do brasil para default
    # imagem do canhoto
    boleto.drawImage(image='./BOLETO/logos/bancodobrasil.jpg',x=160*mm, y=280*mm, width=30*mm, height=5*mm)
    
    # imagem do recido do sacado
    boleto.drawImage(image='./BOLETO/logos/bancodobrasil.jpg',x=7*mm, y=229*mm, width=30*mm, height=5*mm)
    
    # imagem do banco na ficha de compensação
    boleto.drawImage(image='./BOLETO/logos/bancodobrasil.jpg',x=7*mm, y=112*mm, width=30*mm, height=5*mm)
    
    # codigo do banco
    boleto.drawString(43*mm, 229*mm, '001-9')
    boleto.drawString(43*mm, 112*mm, '001-9')
    localpagamento+='Banco do BRASIL S/A'

  else:
    boleto.drawImage(image='./BOLETO/logos/anonimo.jpg',x=160*mm, y=280*mm, width=30*mm, height=5*mm)
    
    # imagem do recido do sacado
    boleto.drawImage(image='./BOLETO/logos/anonimo.jpg',x=7*mm, y=229*mm, width=30*mm, height=5*mm)
    
    # imagem do banco na ficha de compensação
    boleto.drawImage(image='./BOLETO/logos/anonimo.jpg',x=7*mm, y=112*mm, width=30*mm, height=5*mm)
    
    # codigo do banco
    boleto.drawString(43*mm, 229*mm, '000-0')
    boleto.drawString(43*mm, 112*mm, '000-0')
    localpagamento+='Banco Não Identificação'

  # telefone da empresa
  boleto.setFont('Helvetica-Bold', 12)
  boleto.drawString(7*mm, 275*mm, telefone_empresa)
  
  
  ###############
  #RETICULAS DO VENCIMENTO E DO VALOR 
  #           (NÃO RETIRAR DAQUI SENÃO SOBREPORÁ O VALOR E O VENCIMENTO)
  
  # Recibo do sacado
  # retícula com cinza (Vencimento)
  boleto.setFillColor(colors.lightgrey)
  boleto.setStrokeColor(colors.white)
  boleto.rect(158*mm, 220*mm, 42*mm, 8*mm, stroke=1, fill=1)
  # retícula com cinza (Valor do documento)
  boleto.rect(158*mm, 196*mm, 42*mm, 8*mm, stroke=1, fill=1)
  
  # Ficha de compensação
  # retícula com cinza (Vencimento)
  boleto.setFillColor(colors.lightgrey)
  boleto.setStrokeColor(colors.lightgrey)
  boleto.rect(158*mm, 103*mm, 42*mm, 8*mm, stroke=1, fill=1)
  # retícula com cinza (Valor do documento)
  boleto.rect(158*mm, 79*mm, 42*mm, 8*mm, stroke=1, fill=1)
  
  # Término das retículas cinza
  ################
  
  boleto.setStrokeColor(colors.black)
  boleto.setFillColor(colors.black)
  
  # Recibo de entrega
  boleto.setFont(FONTE_FORM, FONTE_FORM_TAM)
  boleto.drawString(7*mm, 270*mm, 'Sacado:')
  boleto.drawString(7*mm, 266*mm, 'Endereço:')
  boleto.drawString(7*mm, 258*mm, 'Documento:')
  boleto.drawString(7*mm, 254*mm, 'Emissão:')
  boleto.drawString(7*mm, 250*mm, 'Data:')
  boleto.drawString(80*mm, 258*mm, 'Valor:')
  boleto.drawString(80*mm, 254*mm, 'Vencimento:')
  boleto.drawString(80*mm, 250*mm, 'Assinatura: _______________________________')
  
  boleto.drawString(7*mm, 217*mm, 'Data do documento')
  boleto.drawString(41*mm, 217*mm, 'No. do documento')
  boleto.drawString(71*mm, 217*mm, 'Espécie doc')
  boleto.drawString(91*mm, 217*mm, 'Aceite')
  boleto.drawString(114*mm, 217*mm, 'Data do processamento')
  boleto.drawString(160*mm, 217*mm, 'Agência/Código do cedente')
  boleto.drawString(7*mm, 209*mm, 'Uso do banco')
  boleto.drawString(7*mm, 225*mm, 'Cedente')
  boleto.drawString(160*mm, 225*mm, 'Vencimento')
  boleto.drawString(41*mm, 209*mm, 'Carteira')
  boleto.drawString(56*mm, 209*mm, 'Espécie')
  boleto.drawString(71*mm, 209*mm, 'Quantidade')
  boleto.drawString(71*mm, 205*mm, '')
  
  boleto.drawString(123*mm, 206*mm, 'x')
  
  boleto.drawString(124*mm, 209*mm, 'Valor')
  boleto.drawString(124*mm, 205*mm, '')
  boleto.drawString(160*mm, 209*mm, 'Nosso número')
  boleto.drawString(160*mm, 201*mm, '(=) Valor do documento')
  boleto.drawString(160*mm, 193*mm, '(-) Desconto/Abatimento')
  boleto.drawString(160*mm, 185*mm, '(-) Outras deduções')
  boleto.drawString(160*mm, 177*mm, '(+) Mora/Multa')
  boleto.drawString(160*mm, 169*mm, '(+) Outros acréscimos')
  boleto.drawString(160*mm, 161*mm, '(=) Valor cobrado')
  boleto.drawString(7*mm, 154*mm, 'Sacado')
  boleto.drawString(7*mm, 140*mm, 'Sacador/avalista')
  boleto.drawString(135*mm, 140*mm, 'Código de baixa')
  boleto.drawString(161*mm, 134*mm, 'Autenticação mecânica')
  
  boleto.setFont(FONTE_DADOS, FONTE_DADOS_TAM)
  boleto.drawString(20*mm, 270*mm, sacado)
  boleto.drawString(20*mm, 266*mm, endereco)
  boleto.drawString(20*mm, 262*mm, endereco1)
  boleto.drawString(20*mm, 258*mm, documento)
  boleto.drawString(20*mm, 254*mm, emissao)
  boleto.drawString(96*mm, 258*mm, valor)
  boleto.drawString(96*mm, 254*mm, vencimento)
  
  boleto.drawString(7*mm, 221*mm, cedente)
  boleto.drawString(180*mm, 221*mm, vencimento)
  boleto.drawString(7*mm, 213*mm, emissao)
  boleto.drawString(41*mm, 213*mm, documento)
  boleto.drawString(71*mm, 213*mm, especiedoc)
  boleto.drawString(91*mm, 213*mm, aceite)
  boleto.drawString(114*mm, 213*mm, emissao)
  boleto.drawString(160*mm, 213*mm, agencia)
  boleto.drawString(7*mm, 205*mm, usobanco)
  boleto.drawString(41*mm, 205*mm, carteira)
  boleto.drawString(56*mm, 205*mm, especiemon)
  boleto.drawString(160*mm, 189*mm, '')
  boleto.drawString(160*mm, 205*mm, nossonumero)
  boleto.drawString(20*mm, 197*mm, valorexpresso)
  boleto.drawString(177*mm, 197*mm, valor)
  boleto.drawString(20*mm, 185*mm, juros)
  boleto.drawString(160*mm, 181*mm, '')
  boleto.drawString(20*mm, 177*mm, observacao1)
  boleto.drawString(20*mm, 171*mm, observacao2)
  boleto.drawString(20*mm, 164*mm, observacao3)
  boleto.drawString(160*mm, 173*mm, '')
  boleto.drawString(160*mm, 165*mm, '')
  boleto.drawString(160*mm, 157*mm, '')
  boleto.drawString(7*mm, 151*mm, sacado)
  boleto.drawString(7*mm, 147*mm, endereco)
  boleto.drawString(7*mm, 144*mm, endereco1)
  
  # linha dividindo o canhoto
  boleto.setStrokeColor(colors.gray)
  boleto.line(0, 240*mm, 210*mm, 240*mm)
  # linha dividindo o recibo do sacado e ficha de compensação
  boleto.line(0, 122*mm, 210*mm, 122*mm)
  
  boleto.setStrokeColor(colors.black)
  boleto.setFillColor(colors.black)
  
  # abaixo da logo do banco
  boleto.line(7*mm, 228*mm, 200*mm, 228*mm)
  # separadores cedente, data do documento e uso do banco
  boleto.line(7*mm, 220*mm, 200*mm, 220*mm)
  boleto.line(7*mm, 212*mm, 200*mm, 212*mm)
  boleto.line(7*mm, 204*mm, 200*mm, 204*mm)
  # separador do número do banco
  boleto.line(42*mm, 228*mm, 42*mm, 234*mm)
  boleto.line(56*mm, 228*mm, 56*mm, 234*mm)
  
  # separador coluna cedente e vencimento
  boleto.line(158*mm, 228*mm, 158*mm, 156*mm)
  
  # separadores do bloco acima
  boleto.line(40*mm, 204*mm, 40*mm, 220*mm)
  boleto.line(55*mm, 204*mm, 55*mm, 212*mm)
  boleto.line(70*mm, 204*mm, 70*mm, 220*mm)
  boleto.line(90*mm, 212*mm, 90*mm, 220*mm)
  boleto.line(113*mm, 212*mm, 113*mm, 220*mm)
  boleto.line(123*mm, 204*mm, 123*mm, 212*mm)
  
  # separador em branco da quantidade e valor
  boleto.setStrokeColor(colors.white)
  boleto.line(123*mm, 205*mm, 123*mm, 208*mm)
  boleto.setStrokeColor(colors.black)
  
  boleto.line(158*mm, 196*mm, 200*mm, 196*mm)
  boleto.line(158*mm, 188*mm, 200*mm, 188*mm)
  boleto.line(158*mm, 180*mm, 200*mm, 180*mm)
  boleto.line(158*mm, 172*mm, 200*mm, 172*mm)
  boleto.line(158*mm, 164*mm, 200*mm, 164*mm)
  boleto.line(7*mm, 156*mm, 200*mm, 156*mm)
  
  # Divisor Recibo sacado e autenticação mecânica
  boleto.line(7*mm, 139*mm, 200*mm, 139*mm)
  boleto.line(144*mm, 126*mm, 144*mm, 133*mm)
  boleto.line(144*mm, 133*mm, 200*mm, 133*mm)
  boleto.line(200*mm, 126*mm, 200*mm, 133*mm)
  
  
  # Ficha de compensação
  boleto.setFont(FONTE_FORM, FONTE_FORM_TAM)
  boleto.drawString(7*mm, 108*mm, 'Local de pagamento')
  boleto.drawString(160*mm, 108*mm, 'Vencimento')
  boleto.drawString(7*mm, 100*mm, 'Cedente')
  boleto.drawString(7*mm, 92*mm, 'Data do documento')
  boleto.drawString(41*mm, 92*mm, 'No. do documento')
  boleto.drawString(71*mm, 92*mm, 'Espécie doc')
  boleto.drawString(91*mm, 92*mm, 'Aceite')
  boleto.drawString(114*mm, 92*mm, 'Data do processamento')
  boleto.drawString(160*mm, 100*mm, 'Agência/Código do cedente')
  boleto.drawString(7*mm, 84*mm, 'Uso do banco')
  boleto.drawString(41*mm, 84*mm, 'Carteira')
  boleto.drawString(56*mm, 84*mm, 'Espécie')
  boleto.drawString(71*mm, 84*mm, 'Quantidade')
  boleto.drawString(123*mm, 81*mm, 'x')
  boleto.drawString(124*mm, 84*mm, 'Valor')
  boleto.drawString(160*mm, 92*mm, 'Nosso número')
  boleto.drawString(160*mm, 84*mm, '(=) Valor do documento')
  boleto.drawString(160*mm, 76*mm, '(-) Desconto/Abatimento')
  boleto.drawString(160*mm, 68*mm, '(-) Outras deduções')
  boleto.drawString(160*mm, 60*mm, '(+) Mora/Multa')
  boleto.drawString(160*mm, 52*mm, '(+) Outros acréscimos')
  boleto.drawString(160*mm, 44*mm, '(=) Valor cobrado')
  boleto.drawString(7*mm, 36*mm, 'Sacado')
  boleto.drawString(7*mm, 23*mm, 'Sacador/avalista')
  boleto.drawString(135*mm, 23*mm, 'Código de baixa')
  boleto.drawString(161*mm, 20*mm, 'Autenticação mecânica')
  
  boleto.setFont('Helvetica-Bold',14)
  boleto.drawString(58*mm, 112*mm, linhadigitavel)
  
  boleto.setFont(FONTE_DADOS, FONTE_DADOS_TAM)
  boleto.drawString(7*mm, 104*mm, localpagamento)
  boleto.drawString(180*mm, 104*mm, vencimento)
  boleto.drawString(7*mm, 96*mm, cedente)
  boleto.drawString(7*mm, 88*mm, emissao)
  boleto.drawString(41*mm, 88*mm, documento)
  boleto.drawString(71*mm, 88*mm, especiedoc)
  boleto.drawString(91*mm, 88*mm, aceite)
  boleto.drawString(114*mm, 88*mm, emissao)
  boleto.drawString(160*mm, 96*mm, agencia)
  boleto.drawString(7*mm, 80*mm, usobanco)
  boleto.drawString(41*mm, 80*mm, carteira)
  boleto.drawString(56*mm, 80*mm, especiemon)
  boleto.drawString(71*mm, 80*mm, '')
  boleto.drawString(124*mm, 80*mm, '')
  boleto.drawString(160*mm, 88*mm, nossonumero)
  
  boleto.drawString(20*mm, 72*mm, valorexpresso)
  boleto.drawString(177*mm, 80*mm, valor)
  boleto.drawString(160*mm, 72*mm, '')
  boleto.drawString(20*mm, 60*mm, juros)
  boleto.drawString(20*mm, 54*mm, observacao1)
  boleto.drawString(20*mm, 48*mm, observacao2)
  boleto.drawString(20*mm, 41*mm, observacao3)
  boleto.drawString(160*mm, 56*mm, '')
  boleto.drawString(160*mm, 48*mm, '')
  boleto.drawString(160*mm, 40*mm, '')
  boleto.drawString(160*mm, 32*mm, '')
  boleto.drawString(7*mm, 33*mm, sacado)
  boleto.drawString(7*mm, 29*mm, endereco)
  boleto.drawString(7*mm, 26*mm, endereco1)
  
  # Identificação das partes
  
  boleto.setFont(FONTE_FORM, FONTE_FORM_TAM_ID)
  boleto.drawString(165*mm, 140*mm, 'Recibo do sacado')
  boleto.drawString(163*mm, 23*mm, 'Ficha de compensação')
  boleto.setFont(FONTE_FORM, FONTE_FORM_TAM)
  
  # abaixo da logo do banco
  boleto.line(7*mm, 111*mm, 200*mm, 111*mm)
  
  # separador do número do banco
  boleto.line(42*mm, 111*mm, 42*mm, 116*mm)
  boleto.line(56*mm, 111*mm, 56*mm, 116*mm)
  
  # separador coluna local de pagamento e vencimento
  boleto.line(158*mm, 39*mm, 158*mm, 111*mm)
  
  # separadores local de pagamento, cedente, data do documento e uso do banco
  boleto.line(7*mm, 103*mm, 200*mm, 103*mm)
  boleto.line(7*mm, 95*mm, 200*mm, 95*mm)
  boleto.line(7*mm, 87*mm, 200*mm, 87*mm)
  boleto.line(7*mm, 79*mm, 200*mm, 79*mm)
  
  # separadores do bloco acima
  boleto.line(40*mm, 79*mm, 40*mm, 95*mm)
  boleto.line(55*mm, 79*mm, 55*mm, 87*mm)
  boleto.line(70*mm, 79*mm, 70*mm, 95*mm)
  boleto.line(90*mm, 87*mm, 90*mm, 95*mm)
  boleto.line(113*mm, 87*mm, 113*mm, 95*mm)
  boleto.line(123*mm, 79*mm, 123*mm, 87*mm)
  
  # separador em branco da quantidade e valor
  boleto.setStrokeColor(colors.white)
  boleto.line(123*mm, 80*mm, 123*mm, 83*mm)
  boleto.setStrokeColor(colors.black)
  
  # separadora valor documento, desconto abatimento
  boleto.line(158*mm, 71*mm, 200*mm, 71*mm)
  boleto.line(158*mm, 63*mm, 200*mm, 63*mm)
  boleto.line(158*mm, 55*mm, 200*mm, 55*mm)
  
  boleto.setLineWidth(0.2)
  boleto.line(158*mm, 47*mm, 200*mm, 47*mm)
  boleto.line(7*mm, 39*mm, 200*mm, 39*mm)
  
  # Divisor Ficha de compensação e autenticação mecânica
  boleto.setLineWidth(0.1)
  boleto.line(7*mm, 22*mm, 200*mm, 22*mm)
  
  boleto.line(144*mm, 12*mm, 144*mm, 19*mm)
  boleto.line(144*mm, 19*mm, 200*mm, 19*mm)
  boleto.line(200*mm, 12*mm, 200*mm, 19*mm)
  
  f = Frame(mm, mm, 5*mm, 20*mm, showBoundary=0)
  f.addFromList([I2of5(codigobarra, xdim = 0.3*mm, checksum=0, bearers=0)], boleto)
  
  boleto.save()
  
  if os.name=='posix':
    # imprimir o arquivo
    os.system(f'lpr ./BOLETO/boleto{banco}.pdf -P '+impressora+' -oPageSize=A4')



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

    codigo_barras2 = linha[41:47]
    codigo_barras3 = linha[47:61]

    dv = calcular_digito_verificador(f'{cod_banco2}{moeda}{campo_livre1}')
    dv2 = calcular_digito_verificador(campo_livre2)
    dv3 = calcular_digito_verificador(campo_livre3)

    cod_barras = (f'{cod_banco2}{moeda}{dac}{vencimento}{valor}{campo_livre1}{codigo_barras2}{codigo_barras3}')

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
    df_atual = pd.DataFrame(dados)
    df_final = pd.concat([df_final, df_atual], ignore_index=True)
    df_final.to_excel(f'{nome_arquivo}_Boletos.xlsx', index=False)

    processar_boleto(cod_banco2, nome, n_documento, data_emissao_formatada, valor_formatado, data_vencimento_formatada, agencia, Codigo_de_Barras, carteira,data_limite, codigo_protesto,juros_mora,cnpj_gcp,especie_titulo,n_registro,cod_barras)

    
def segmento_g(nome_arquivo, numero_linha,inscricao_header_lote):
    with open(nome_arquivo, 'r') as arquivo_ret:
        for _ in range(numero_linha - 1):
            # Pular linhas até atingir a linha desejada
            arquivo_ret.readline()

        # Ler a linha desejada
        linha = arquivo_ret.readline()

        # Processar a linha
        processar_linha(nome_arquivo, linha,inscricao_header_lote)



