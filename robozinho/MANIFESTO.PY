import pyautogui
import time
import PySimpleGUI as sg
import datetime

pyautogui.PAUSE = 0.5  #PAUSA ENTRE AÇÕES

#INICIO DE PROCESSO
pyautogui.alert("Em instantes o Rodopar será aberto...\nNão mexa o mouse, muito menos o teclado\nEstamos em fase de teste, agradeço a colaboração")
pyautogui.press("enter")

# FUNÇÕES
#FUNÇÃO PARA OBTER DADOS
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

    data = ''.join(filter(str.isdigit, data)) # Filtrar apenas numeros

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

    data = ''.join(filter(str.isdigit, data)) # Filtrar apenas numeros

    return data

#FUNÇÃO DATA ATUAL 8 HORAS AM
def obter_data_atual():
    data_atual = datetime.datetime.now().date()
    return data_atual
data_atual = obter_data_atual()
dia_atual = data_atual.strftime("%d%m%Y0800")

#FUNÇÃO DATA ATUAL 8 HORAS PM
def obter_data_atual2():
    data_atual2 = datetime.datetime.now().date()
    return data_atual2
data_atual2 = obter_data_atual2()
dia_atual2 = data_atual2.strftime("%d%m%Y2000")

#FUNÇÃO DIA ANTERIOR
def obter_dia_anterior():
    data_atual = datetime.datetime.now().date()
    dia_anterior = data_atual - datetime.timedelta(days=1)
    return dia_anterior
data_anterior = obter_dia_anterior()
dia_anterior = data_anterior.strftime("%d%m%Y2000")

#FUNÇÃO OBTER DATA DO DIA SEGUINTE
def obter_dia_posterior():
    data_atual = datetime.datetime.now().date()
    dia_posterior = data_atual + datetime.timedelta(days=1)
    return dia_posterior
data_posterior = obter_dia_posterior()
dia_posterior = data_posterior.strftime("%d%m%Y2000")

#Abrir o Manifesto BK (CRIAÇÃO DE MANIFESTO)
pyautogui.click(76,28,duration=1)
pyautogui.click(91,97,duration=1)
pyautogui.click(229,166,duration=1)
time.sleep(2)

#INSERINDO DADOS INICIAIS (FILIAL)
pyautogui.write("5")
for x in range(11):
    pyautogui.press("TAB")
pyautogui.write("5")
pyautogui.press("TAB")
pyautogui.write(dia_atual)

#ABRINDO O ARQUIVO ONDE SE ENCONTRA AS DT COM SEUS DADOS
with open('saida.txt','r') as arquivo:
    for linha in arquivo:
        dt =linha.split(',')[0]
        linhas =linha.split(',')[1]
        codigo =linha.split(',')[2]

        #INSERINDO A DT
        pyautogui.click(337,178,duration=2)
        pyautogui.write(dt)

        #INSERINDO O CODIGO DA CIDADE
        pyautogui.click(509,246,duration=2)
        pyautogui.write(codigo)
        
        #INSERINDO A LINHA DA CIDADE
        pyautogui.click(604,246,duration=2)
        pyautogui.write(linhas)

        #ATUALIZAR GRIDS
        pyautogui.click(1120,178,duration=2)
        time.sleep(20)

        #SELECIONAR TODOS
        pyautogui.click(1119,238,duration=2)
        time.sleep(2)

        #GERAR MANIFESTO
        pyautogui.click(1018,240,duration=2)
        time.sleep(2)
        pyautogui.press("enter")

        #APAGANDO DADOS INSERIDOS (DT, CODIGO E LINHA DAS CIDADES)
        pyautogui.click(401,178,duration=1)
        for x in range(10):
            pyautogui.press("backspace")
        pyautogui.click(527,245,duration=1)
        for x in range(8):
            pyautogui.press("backspace")
        pyautogui.click(631,245,duration=1)
        for x in range(8):
            pyautogui.press("backspace")
        time.sleep(2)

pyautogui.click(1181,76)
time.sleep(2)
#INICIANDO O PROCESSO DE BAIXAR OS MANIFESTOS!!

#Abrindo emissão
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

#PREENCHENDO INFORMAÇÕES NO BUSCAR
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
#FIM

#TOTAL DE MANIFESTOS A BAIXAR
emissao = 40

#MUDE O NUMERO PARA O TOTAL DE REPETIÇÕES
for x in range(emissao):

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
    time.sleep(5)
    pyautogui.click(751,176)
    time.sleep(5)
    pyautogui.click(1156,63)
    pyautogui.click(1156,63)
    time.sleep(5)
    pyautogui.click(1156,63)
    time.sleep(5)

#ABRINDO O BUSCAR
pyautogui.click(934,75)
time.sleep(2)
pyautogui.click(934,75)
time.sleep(1)

#PREENCHENDO INFORMAÇÕES NO BUSCAR
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
#FIM

emissao = 40

for x in range(emissao):

    #BUSCAR MOTORISTA
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

    #INSERIR A DATA E HORA
    pyautogui.click(781,449,duration=1)
    pyautogui.press("HOME")
    pyautogui.write(dia_posterior)
    time.sleep(1)

    #EFETUAR
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
    
    #ENVIAR MDF
    pyautogui.click(394,84,duration=1)
    time.sleep(2)
    pyautogui.click(581,173,duration=1)
    time.sleep(2)
    pyautogui.click(712,435,duration=1)
    time.sleep(10)
    pyautogui.click(1164,65,duration=1)
    pyautogui.click(1164,65,duration=1)
    time.sleep(2)

pyautogui.alert("MANIFESTOS ENVIADOS, PROCESSO FINALIZADO COM SUCESSO!!")
