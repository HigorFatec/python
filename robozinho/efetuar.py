import pyautogui
import time
import datetime

pyautogui.PAUSE = 0.5  #PAU

time.sleep(2)

pyautogui.alert("Em instantes a emissão de manifesto será aberta...") #INICIO DE MODA

#Abrindo emissão
#pyautogui.click(76,28)
#time.sleep(1)
#pyautogui.click(77,63)
#time.sleep(1)
#pyautogui.click(370,184)
#time.sleep(1)
#pyautogui.click(472,184)
#time.sleep(1)

def obter_dia_posterior():
    data_atual = datetime.datetime.now().date()
    dia_posterior = data_atual + datetime.timedelta(days=1)
    return dia_posterior
data_posterior = obter_dia_posterior()
dia_posterior = data_posterior.strftime("%d%m%Y2000")

#pyautogui.click(934,75)
#time.sleep(1)
#pyautogui.alert("Insira FILIAL: 5, linha: RPU, e a data atual,\nSituação: Inconsistente.\n Após isso aperte em voltar e de aperte em 'Ok'")

#MUDE O NUMERO PARA O TOTAL DE REPETIÇÕES
for x in range(23):

    #BUSCAR MOTORISTA
    pyautogui.click(934,75)
    time.sleep(2)
    pyautogui.click(934,75)
    time.sleep(1)
    pyautogui.click(792,153)
    pyautogui.press("F4")
    pyautogui.press("F4")
    time.sleep(1)
    pyautogui.click(458,448)
    pyautogui.press("enter")
    time.sleep(5)

    #INSERIR A DATA E HORA
    pyautogui.click(781,449)
    pyautogui.press("HOME")
    pyautogui.write(dia_posterior)
    time.sleep(1)

    #EFETUAR
    pyautogui.click(626,74)
    time.sleep(2)
    pyautogui.press("enter")
    pyautogui.click(626,74)
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(10)
    pyautogui.click(820,438)
    time.sleep(10)
    pyautogui.click(767,435)
    time.sleep(2)

time.sleep(2)
pyautogui.click(981,750)
time.sleep(2)
pyautogui.click(580,173)
time.sleep(2)
pyautogui.press('enter')
pyautogui.press('enter')
time.sleep(2)

pyautogui.alert("MANIFESTOS FEITOS COM SUCESSO !!!!")

