from header_arq import header_arquivo
from header_lote import header_lote
#from segmento_g import segmento_g
from boleto2 import segmento_g
from segmento_h import segmento_h
from trailer_lote import trailer_lote
from trailer_arquivo import trailer_arquivo
from header_lote import processar_linha
import os
import sys
import pyautogui


# LER LINHA ESPECIFICA HEADER ARQUIVO
#header_arquivo( ARQUIVO , LINHA)

#LER LINHA ESPECIFICA HEADER LOTE
#header_lote (ARQUIVO, LINHA)

def processar_arquivo(arquivo):

    inscricao_header_lote = None  # Inicializa a variável para armazenar o valor de inscricao

    with open(arquivo, 'r') as arquivo_ret:
        for numero_linha, linha in enumerate(arquivo_ret, start=1):
            segmento = linha[7:8]  # Ajuste isso de acordo com a posição do segmento em suas linhas
            if segmento == '3' and linha[13:14] == 'H':
                segmento_h(arquivo, numero_linha)
            # Adicione mais condições conforme necessário
            elif segmento == '0':
                header_arquivo(arquivo, numero_linha)
            elif segmento == '1':
                inscricao_header_lote = processar_linha(arquivo, linha)  # Atualiza a variável com o valor de inscricao
                header_lote(arquivo,numero_linha)
            elif segmento == '5':
                trailer_lote(arquivo,numero_linha)
            elif segmento =='9':
                trailer_arquivo(arquivo,numero_linha)
            elif segmento == '3' and linha[13:14] == 'G':
                segmento_g(arquivo, numero_linha,inscricao_header_lote)


    # Registrar o valor final do contador no log
    pyautogui.alert("Processo finalizado com Sucesso!!")


# Obtém o caminho do script principal
caminho_script = sys.argv[0]
diretorio_script = os.path.dirname(os.path.abspath(caminho_script))

# Define o diretório de entrada
diretorio_entrada = os.path.join(diretorio_script, 'caminho')

# Define o diretório de saída
diretorio_saida = os.path.join(diretorio_script, 'lido')       

# Verifica se o diretório de saída existe, se não, tenta criá-lo
if not os.path.exists(diretorio_saida):
    try:
        os.makedirs(diretorio_saida)
    except Exception as e:
        print(f"Erro ao criar o diretório de saída {diretorio_saida}: {e}")
        exit(1)

# Lista todos os arquivos no diretório de entrada
arquivos_ret = [arquivo for arquivo in os.listdir(diretorio_entrada) if arquivo.lower().endswith('.ret')]

# Processa cada arquivo
for arquivo_ret in arquivos_ret:
    caminho_arquivo_entrada = os.path.join(diretorio_entrada, arquivo_ret)
    
    try:
        # Gera um nome de arquivo de saída
        arquivo_saida = f'{arquivo_ret}'  # Ajuste conforme necessário
        caminho_arquivo_saida = os.path.join(diretorio_saida, arquivo_saida)
        
        # Processa o arquivo e salva o resultado no diretório de saída
        processar_arquivo(caminho_arquivo_entrada)
        
        # Aqui você pode mover ou copiar o arquivo processado para o diretório de saída
        os.replace(caminho_arquivo_entrada, caminho_arquivo_saida)
    except Exception as e:
        print(f"Erro ao processar o arquivo {caminho_arquivo_entrada}: {e}")

print("Processamento concluído.")


# Exemplo de chamada
#processar_arquivo('VS04123C.ret')