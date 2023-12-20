import pyautogui
import time


pyautogui.PAUSE = 0.5  #PAUSA ENTRE AÇÕES
time.sleep(2)

pyautogui.alert("Em instantes a emissão de manifesto será aberta...") #INICIO DE MODA


#MUDE O NUMERO PARA O TOTAL DE REPETIÇÕES
for x in range(20):

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

    #BAIXAR
    pyautogui.click(571,71)
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(2)
    
    #ENCERRAR MDF
    pyautogui.click(383,77)
    time.sleep(2)
    pyautogui.click(751,176)
    time.sleep(2)
    pyautogui.click(1156,63)
    pyautogui.click(1156,63)
    time.sleep(2)
    pyautogui.click(1156,63)
    time.sleep(2)