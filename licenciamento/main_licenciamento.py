from time import sleep
import pyautogui

contador = 0


pyautogui.PAUSE = 0.7

pyautogui.alert("This is an alert box.")

pyautogui.click(284,43)

pyautogui.click(326,96)

pyautogui.click(598,98)

#SSY3C77
#CCU2G37

#ABRINDO O ARQUIVO ONDE SE ENCONTRA AS DT COM SEUS DADOS
with open('saida.txt','r', encoding='utf-8') as arquivo:
    for linha in arquivo:
        fornecedor = linha.split(';')[0] #45
        serie = linha.split(';')[1] #A
        documento = linha.split(';')[2] #FOX9J21/LIC24
        tipo = linha.split(';')[3] #FAT
        filial = linha.split(';')[4] #37
        indice = linha.split(';')[5] #1
        banco = linha.split(';')[6] #237
        docto = linha.split(';')[7] #160,22

        #parc1 = linha.split(';')[8] #1
        vencimento1 = linha.split(';')[9] #09/05/2024
        valor1 = linha.split(';')[10] # 160,22

        unidade = linha.split(';')[11]
        gasto = linha.split(';')[12]
        custo = linha.split(';')[13]
        sintetica = linha.split(';')[14]
        analitica = linha.split(';')[15]

        valor = linha.split(';')[16]

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
        pyautogui.click(457,651)
        pyautogui.write('AUTOMATIZACAO NA ENTRADA DE CONTAS A PAGAR IPVA')
        pyautogui.hotkey('alt','s')
        pyautogui.hotkey('alt','s')

        #ABRINDO PARCELAS
        pyautogui.click(140,203)

        pyautogui.click(29,242)
        sleep(3)
        pyautogui.press('tab')
        pyautogui.write(vencimento1)
        pyautogui.press('tab')
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1023,580)
        pyautogui.click(1067,240)

        # pyautogui.click(22,189)
        # sleep(3)
        # pyautogui.press('tab')
        # pyautogui.write(vencimento2)
        # pyautogui.press('tab')
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(397,186)
        # pyautogui.press('tab')
        # pyautogui.write(parc2)
        # pyautogui.click(854,187)

        # pyautogui.click(22,189)
        # sleep(3)
        # pyautogui.press('tab')
        # pyautogui.write(vencimento3)
        # pyautogui.press('tab')
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(397,186)
        # pyautogui.press('tab')
        # pyautogui.write(parc3)
        # pyautogui.click(854,187)

        # pyautogui.click(22,189)
        # sleep(3)
        # pyautogui.press('tab')
        # pyautogui.write(vencimento4)
        # pyautogui.press('tab')
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(397,186)
        # pyautogui.press('tab')
        # pyautogui.write(parc4)
        # pyautogui.click(854,187)

        # pyautogui.click(22,189)
        # sleep(3)
        # pyautogui.press('tab')
        # pyautogui.write(vencimento5)
        # pyautogui.press('tab')
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(1023,580)
        # pyautogui.click(397,186)
        # pyautogui.press('tab')
        # pyautogui.write(parc5)
        # pyautogui.click(854,187)

        sleep(2)

        #CLASSIFICAÇÃO

        #UNIDADE DE NEGOCIO
        pyautogui.click(41,260)
        pyautogui.press('f2')
        pyautogui.press('tab')
        pyautogui.write(unidade)
        pyautogui.press('f4')
        pyautogui.click(865,525)
        pyautogui.press('enter')
        pyautogui.press('enter')


        #CENTRO DE GASTO
        pyautogui.press('f2')  
        pyautogui.write(gasto)
        pyautogui.press('f4')
        pyautogui.click(865,525)
        pyautogui.press('enter')
        pyautogui.press('enter')

        #CENTRO DE CUSTO
        pyautogui.press('f2')
        pyautogui.write(custo)
        pyautogui.press('f4')
        pyautogui.click(865,525)
        pyautogui.press('enter')
        pyautogui.press('enter')

        #CONTA SINTETICA
        pyautogui.write(sintetica)
        pyautogui.press('tab')
        pyautogui.write(analitica)
        pyautogui.press('tab')
        pyautogui.write(valor)
        pyautogui.click(635,428)

        pyautogui.hotkey('alt','s')
        pyautogui.hotkey('alt','s')
        pyautogui.click(1128,606)
        pyautogui.click(1158,631)

        pyautogui.hotkey('alt','i')
        pyautogui.click(874,104)
        pyautogui.click(874,104)

        sleep(2)

        pyautogui.click(294,235)  
    
        sleep(2)


        contador += 1

        print(f"Foram feitas {contador} linhas! Placa {documento}")   