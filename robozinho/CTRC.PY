import pyautogui
import time
import PySimpleGUI as sg
import datetime

pyautogui.PAUSE = 0.5

pyautogui.alert("Em instantes o Rodopar será aberto...\nNão mexa o mouse, muito menos o teclado\nEstamos em fase de teste, agradeço a colaboração\nCriado por: HigorMachado")
pyautogui.press("enter")

def get_user_string_input(title):
    layout = [
        [sg.InputText("", key="data")],
        [sg.Button("Enviar")]
    ]

    window = sg.Window(title, layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Enviar":
            data = values["data"]
            break

    window.close()

    data = ''.join(filter(str.isdigit, data))

    return data

    layout = [
        [sg.InputText("", key="data")],
        [sg.Button("Enviar")]
    ]

    window = sg.Window(title, layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Enviar":
            data = values["data"]
            break

    window.close()

    data = ''.join(filter(str.isdigit, data)) 

    return data

def obter_data_atual():
    data_atual = datetime.datetime.now().date()
    return data_atual
data_atual = obter_data_atual()
dia_atual = data_atual.strftime("%d%m%Y0800")

def obter_data_atual2():
    data_atual2 = datetime.datetime.now().date()
    return data_atual2
data_atual2 = obter_data_atual2()
dia_atual2 = data_atual2.strftime("%d%m%Y2000")

def obter_dia_anterior():
    data_atual = datetime.datetime.now().date()
    dia_anterior = data_atual - datetime.timedelta(days=4)
    return dia_anterior
data_anterior = obter_dia_anterior()
dia_anterior = data_anterior.strftime("%d%m%Y2000")

def obter_dia_posterior():
    data_atual = datetime.datetime.now().date()
    dia_posterior = data_atual + datetime.timedelta(days=1)
    return dia_posterior
data_posterior = obter_dia_posterior()
dia_posterior = data_posterior.strftime("%d%m%Y2000")

pyautogui.click(76,28,duration=1)
pyautogui.click(91,97,duration=1)
pyautogui.click(229,166,duration=1)
time.sleep(2)

pyautogui.write("5")

pyautogui.click(312,204,duration=1)

with open('saida.txt','r') as arquivo:
    for linha in arquivo:
        dt =linha.split(',')[0]
        linhas =linha.split(',')[1]
        codigo =linha.split(',')[2]

        pyautogui.click(337,178,duration=2)
        pyautogui.write(dt)

        pyautogui.click(1123,176,duration=2)
        time.sleep(30)

        pyautogui.click(1119,238,duration=2)
        time.sleep(2)

        pyautogui.click(1018,240,duration=2)
        time.sleep(10)
        pyautogui.press("enter")
        time.sleep(40)

        pyautogui.click(401,178,duration=1)
        for x in range(10):
            pyautogui.press("backspace")
        time.sleep(2)

pyautogui.click(1181,76)
time.sleep(2)

pyautogui.click(76,28)
time.sleep(1)
pyautogui.click(77,63)
time.sleep(1)
pyautogui.click(370,184)
time.sleep(1)
pyautogui.click(472,184)
time.sleep(1)
pyautogui.click(934,75)
time.sleep(2)
pyautogui.click(934,75)
time.sleep(1)

pyautogui.click(180,240,duration=1)
pyautogui.write("5")
pyautogui.click(208,287,duration=1)
pyautogui.write("RPU")
pyautogui.click(574,263,duration=1)
pyautogui.press("home")
pyautogui.write(dia_anterior)
pyautogui.click(702,264,duration=1)
pyautogui.press("home")
pyautogui.write(dia_anterior)
pyautogui.click(879,242,duration=1)
pyautogui.click(856,285,duration=1)
pyautogui.click(158,205,duration=1)
pyautogui.click(723,245,duration=1)
pyautogui.click(699,275,duration=1)
time.sleep(0.5)
pyautogui.click(104,206,duration=1)
pyautogui.press("F4")
time.sleep(1)

emissao = 40

for x in range(emissao):

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

    pyautogui.click(383,77)
    time.sleep(2)
    pyautogui.click(751,176)
    time.sleep(2)
    pyautogui.click(1156,63)
    pyautogui.click(1156,63)
    time.sleep(2)
    pyautogui.click(1156,63)
    time.sleep(2)

pyautogui.click(934,75)
time.sleep(2)
pyautogui.click(934,75)
time.sleep(1)

pyautogui.click(574,263,duration=1)
for l in range (10):
    pyautogui.press("backspace")
pyautogui.write(dia_atual)
pyautogui.click(702,264,duration=1)
for k in range (10):
    pyautogui.press("backspace")
pyautogui.write(dia_atual)
pyautogui.click(879,242,duration=1)
pyautogui.click(851,270,duration=1)

pyautogui.click(158,205,duration=1)
pyautogui.click(723,245,duration=1)
pyautogui.click(704,261,duration=1)
pyautogui.click(104,206,duration=1)
pyautogui.click(787,157,duration=1)
pyautogui.press("F4")
time.sleep(2)

emissao = 40

for x in range(emissao):

    pyautogui.click(934,75,duration=1)
    time.sleep(2)
    pyautogui.click(934,75,duration=1)
    time.sleep(1)
    pyautogui.click(792,153,duration=1)
    pyautogui.press("F4")
    pyautogui.press("F4")
    time.sleep(1)
    pyautogui.click(458,448,duration=1)
    pyautogui.press("enter")
    time.sleep(5)

    pyautogui.click(781,449,duration=1)
    pyautogui.press("HOME")
    pyautogui.write(dia_posterior)
    time.sleep(1)

    pyautogui.click(626,74,duration=1)
    time.sleep(2)
    pyautogui.press("enter")
    pyautogui.click(626,74,duration=1)
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(10)
    pyautogui.click(820,438,duration=1)
    time.sleep(10)
    pyautogui.click(767,435,duration=1)
    time.sleep(2)
    
    pyautogui.click(394,84,duration=1)
    time.sleep(1)
    pyautogui.click(581,173,duration=1)
    time.sleep(1)
    pyautogui.click(712,435,duration=1)
    time.sleep(10)
    pyautogui.click(1164,65,duration=1)
    pyautogui.click(1164,65,duration=1)
    time.sleep(2)

pyautogui.alert("MANIFESTOS ENVIADOS, PROCESSO FINALIZADO COM SUCESSO!!")
