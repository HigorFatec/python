import pyautogui
import pyperclip
from time import sleep

#PAUSA DE 0.5 SEGUNDOS POR OPERAÇÃO
pyautogui.PAUSE = 0.5

#AVISO DE INICIO DE OPERAÇÃO
pyautogui.alert("COMEÇANDO")

#CLICK EM "FLUXO DE CAIXA"
pyautogui.click(211,28)

#CLICK EM "MOVIMENTAÇÃO"
pyautogui.click(230,67)

#CLICK EM "ENTRADAS CONTA PAGAR"
pyautogui.click(369,65)


#INICIANDO ESTRUTURA DE REPETIÇÃO
with open('saida.txt','r') as arquivo:
    for linha in arquivo:
        #ATRIBUINDO VALORES AS VARIAVEIS POR LINHA
        cnpj = linha.split(';')[0]
        periodo = linha.split(';')[1]
        documento = linha.split(';')[2]
        serie = linha.split(';')[3]
        valor = linha.split(';')[4]
        filial = linha.split(';')[5]
        
        #CLICANDO NO CAMPO FORNECEDOR
        pyautogui.click(202,183)
        pyautogui.write("3192")
        pyautogui.press("enter")

        #CAMPO SÉRIE
        pyautogui.press("A")
        pyautogui.press("enter")
        
        #INSERINDO DOCUMENTO (VARIAVEL MINHA_STRING CONCATENADA)
        minha_string = f"{filial}-{documento}-{serie}"
        pyperclip.copy(minha_string)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press("enter")

        #INSERINDO "TIPO" (PADRÃO)
        pyautogui.write("IMT")
        pyautogui.press("enter")

        #INSERINDO FILIAL
        pyautogui.write(filial)
        
        #INSERINDO INDICE
        pyautogui.write("1")
        pyautogui.press("enter")
        pyautogui.press("enter")

        #INSERINDO CODIGO DO BANCO
        pyautogui.write("237")
        pyautogui.press("enter")
        pyautogui.press("enter")

        #INSERINDO DATA DE EMISSÃO
        pyautogui.write(f'{periodo}0000')
        pyautogui.press("tab")
        
        #INSERINDO DATA DE REFERENCIA
        pyautogui.write(f'{periodo}0000')        
        pyautogui.press("tab")

        #INSERINDO VALOR DO DOCUMENTO
        pyautogui.write(valor)
        
        #ANOTAÇÃO DE REFERENCIA
        pyautogui.click(366,515)
        pyautogui.write('PAGAMENTO AUTOMATICO F&R')

        #SALVAR DADOS
        pyautogui.hotkey('alt','s')
        
        #ACESSANDO PARCELAS
        pyautogui.click(112,157)

        #INSERE NOVO ITEM
        pyautogui.click(20,187)
        
        sleep(1)
        #CLICANDO EM SIM EM CASO DE SABADOS
        pyautogui.click(1111,587)
        
        #CONFIRMANDO
        pyautogui.click(853,184)
        
        #ACESSANDO A ABA DE CLASSIFICAÇÃO
        pyautogui.click(229,155)

        #INSERINDO NOVO ITEM
        pyautogui.click(33,203)

        #ACESSANDO CAMPO DE UNIDADE DE NEGOCIO
        pyautogui.click(241,203)

        #INSERINDO DADOS PADRÕES DE CLASSIFICAÇÃO
        pyautogui.write("19")
        pyautogui.press("tab")
        pyautogui.write("59")
        pyautogui.press("tab")
        pyautogui.write("102")
        pyautogui.press("tab")
        pyautogui.write("70")
        pyautogui.press("tab")
        pyautogui.write("252")
        pyautogui.press("tab")
        pyautogui.write(valor)
        pyautogui.press("enter")
        
        #EFETUANDO 
        pyautogui.click(508,335)
        
        
        #ACESSANDO CLASSIFICAÇÃO
        pyautogui.click(40,156)
        
        #INCLUINDO NOVO REGISTRO
        pyautogui.hotkey('alt','i')
        pyautogui.click(703,78)

        sleep(1)
        #NOVO PROCESSO
        
pyautogui.alert("FIM DA OPERAÇÃO")
