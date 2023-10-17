import pyautogui
from time import sleep

#pyautogui.PAUSE = 1  #PAUSA ENTRE AÇÕES

pyautogui.alert("INICIANDO")

pyautogui.click(18,30,duration=1)   
sleep(1)
pyautogui.click(50,63,duration=1)
sleep(1)
pyautogui.click(205,117,duration=1)
sleep(1)

with open('saida.txt','r') as arquivo:
    for linha in arquivo:

        valores = linha.strip().split(',')

        pyautogui.click(136,159,duration=1)
        sleep(1)

        pyautogui.write("5")
        sleep(1)

        pyautogui.press("tab")
        sleep(1)

        pyautogui.press("enter")

        sleep(2)
        pyautogui.press("enter")
        sleep(1)

        pyautogui.click(429,443,duration=1)
        sleep(1)

        for x in range(50):
            pyautogui.press("backspace")
            sleep(0.1)

        pyautogui.write("DIARIA REF SEGUNDA SEMANA DE OUTUBRO DE 2023")
        sleep(1)

        pyautogui.press("tab")
        sleep(1)

        pyautogui.write("1")
        sleep(1)

        pyautogui.click(347,178,duration=1)
        sleep(1)

        pyautogui.click(319,200,duration=1)
        sleep(1)

        pyautogui.press("enter")
        sleep(1)


        for x in range(5):
            pyautogui.press("down")
            sleep(1)

        pyautogui.click(946,183,duration=1)
        sleep(1)

        pyautogui.click(899,202,duration=1)
        sleep(1)

        pyautogui.press("tab")
        sleep(1)

        pyautogui.write("5")
        sleep(1)

        pyautogui.press("enter")
        sleep(1)

        fit =valores[0]
        print(fit)
        total = valores[1] + ',' + valores[2] 
        print(total)

        #INSERINDO A FIT
        pyautogui.write(fit)
        sleep(1)

        pyautogui.click(418,364,duration=1)
        sleep(1)

        pyautogui.write(total)
        sleep(1)

        pyautogui.click(722,82,duration=1)
        sleep(1)

        pyautogui.click(417,80,duration=1)
        sleep(1)
        pyautogui.press('enter')
        sleep(1)
        pyautogui.press('enter')
        sleep(1)

        pyautogui.click(675,75,duration=1)
        sleep(1)
        
