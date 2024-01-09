from time import sleep
import pyautogui

contador = 0

pyautogui.PAUSE = 0.5

pyautogui.alert("This is an alert box.")

pyautogui.click(209,30)

pyautogui.click(219,63)

pyautogui.click(380,64)

#ABRINDO O ARQUIVO ONDE SE ENCONTRA AS DT COM SEUS DADOS
with open('saida.txt','r') as arquivo:
    for linha in arquivo:
        fornecedor = linha.split(';')[0]
        serie = linha.split(';')[1]
        documento = linha.split(';')[2]
        tipo = linha.split(';')[3]
        filial = linha.split(';')[4]
        indice = linha.split(';')[5]
        banco = linha.split(';')[6]
        docto = linha.split(';')[7]

        parc1 = linha.split(';')[8]
        vencimento1 = linha.split(';')[9]
        parc2 = linha.split(';')[10]
        vencimento2 = linha.split(';')[11]
        parc3 = linha.split(';')[12]
        vencimento3 = linha.split(';')[13]
        parc4 = linha.split(';')[14]
        vencimento4 = linha.split(';')[15]
        parc5 = linha.split(';')[16]
        vencimento5 = linha.split(';')[17]

        unidade = linha.split(';')[18]
        gasto = linha.split(';')[19]
        custo = linha.split(';')[20]
        sintetica = linha.split(';')[21]
        analitica = linha.split(';')[22]
        valor = linha.split(';')[23]

        pyautogui.write(fornecedor)
        pyautogui.press('tab')
        pyautogui.write(serie)
        pyautogui.press('tab')
        pyautogui.write(documento)
        pyautogui.press('tab')
        pyautogui.write(tipo)
        pyautogui.press('tab')
        pyautogui.write(filial)
        pyautogui.press('tab')
        pyautogui.write(indice)
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write(banco)
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write(docto)
        pyautogui.click(306,512)
        pyautogui.write('AUTOMAÇÃO NA ENTRADA DE CONTAS A PAGAR IPVA')
        pyautogui.hotkey('alt','s')
        pyautogui.hotkey('alt','s')

        #ABRINDO PARCELAS
        pyautogui.click(112,158)

        pyautogui.click(22,189)
        sleep(3)
        pyautogui.press('tab')
        pyautogui.write(vencimento1)
        pyautogui.press('tab')
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(397,186)
        pyautogui.press('tab')
        pyautogui.write(parc1)
        pyautogui.click(854,187)

        pyautogui.click(22,189)
        sleep(3)
        pyautogui.press('tab')
        pyautogui.write(vencimento2)
        pyautogui.press('tab')
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(397,186)
        pyautogui.press('tab')
        pyautogui.write(parc2)
        pyautogui.click(854,187)

        pyautogui.click(22,189)
        sleep(3)
        pyautogui.press('tab')
        pyautogui.write(vencimento3)
        pyautogui.press('tab')
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(397,186)
        pyautogui.press('tab')
        pyautogui.write(parc3)
        pyautogui.click(854,187)

        pyautogui.click(22,189)
        sleep(3)
        pyautogui.press('tab')
        pyautogui.write(vencimento4)
        pyautogui.press('tab')
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(397,186)
        pyautogui.press('tab')
        pyautogui.write(parc4)
        pyautogui.click(854,187)

        pyautogui.click(22,189)
        sleep(3)
        pyautogui.press('tab')
        pyautogui.write(vencimento5)
        pyautogui.press('tab')
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(397,186)
        pyautogui.press('tab')
        pyautogui.write(parc5)
        pyautogui.click(854,187)

        sleep(2)

        #CLASSIFICAÇÃO

        #UNIDADE DE NEGOCIO
        pyautogui.click(30,201)
        pyautogui.press('f2')
        pyautogui.press('tab')
        pyautogui.write(unidade)
        pyautogui.press('f4')
        pyautogui.click(1119,360)
        pyautogui.press('enter')


        #CENTRO DE GASTO
        pyautogui.press('f2')
        pyautogui.write(gasto)
        pyautogui.press('f4')
        pyautogui.click(1119,360)
        pyautogui.press('enter')

        #CENTRO DE CUSTO
        pyautogui.press('f2')
        pyautogui.write(custo)
        pyautogui.press('f4')
        pyautogui.click(1119,360)
        pyautogui.press('enter')

        #CONTA SINTETICA
        pyautogui.write(sintetica)
        pyautogui.press('tab')
        pyautogui.write(analitica)
        pyautogui.press('tab')
        pyautogui.write(valor)
        pyautogui.click(506,337)

        pyautogui.hotkey('alt','s')
        pyautogui.hotkey('alt','s')

        pyautogui.hotkey('alt','i')
        pyautogui.click(702,77)
        pyautogui.click(702,77)

        sleep(2)

        pyautogui.click(1113,579)  
    
        sleep(2)

        pyautogui.click(701,78)
        pyautogui.click(701,78)
        sleep(1)

        pyautogui.click(188,182)

        sleep(1)

        contador += 1

        print(f"Foram feitas {contador} linhas!")   