import os
import traceback
import mysql.connector
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Gerenciador que baixa o Geckodriver automaticamente
from webdriver_manager.firefox import GeckoDriverManager

def configurar_firefox():
    firefox_options = Options()
    
    # Define o caminho que você encontrou para garantir que ele não se perca
    firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    
    # Configurações de estabilidade
    firefox_options.add_argument("--start-maximized")
    
    # Se precisar rodar sem abrir a janela no futuro, use:
    # firefox_options.add_argument("--headless") 

    # Instala e inicia o Geckodriver automaticamente
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)
    
    return driver

while True:
    driver = None
    conn = None
    cursor = None

    try:
        print(f"--- Iniciando Ciclo Firefox: {datetime.now()} ---")
        driver = configurar_firefox()

        # 1. Acesso ao SIAG Valecard
        driver.get('https://siag.valecard.com.br/frota/pages/start.jsf')
        wait = WebDriverWait(driver, 30)

        # 2. Seleção do Perfil
        perfil_select = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select')))
        perfil_select.click()
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select/option[6]').click()

        # 3. Login
        wait.until(EC.presence_of_element_located((By.NAME, 'formLogin:j_id15'))).send_keys('higor.cargopolo')
        driver.find_element(By.NAME, 'formLogin:j_id17').send_keys('@Cargo20')
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[5]/input').click()

        sleep(10) # Tempo para carregar o dashboard principal

        # 4. Navegação no Menu (Passar o mouse)
        actions = ActionChains(driver)
        menu_alteracao = wait.until(EC.presence_of_element_located((By.ID, "MENU_FORM_HADOUKEN:j_id89")))
        actions.move_to_element(menu_alteracao).perform()

        # Clicar no submenu após o hover
        submenu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']")))
        submenu.click()
        
        sleep(5)

        # 5. Captura do Saldo Disponível
        saldo_elemento = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//td[text()='Saldo Disponível']/following-sibling::td[1]")
        ))
        valor_capturado = saldo_elemento.text
        print(f"✅ Saldo capturado com Firefox: {valor_capturado}")

        # 6. Gravação no MySQL
        conn = mysql.connector.connect(
            host="177.47.11.35",
            port=14804,
            user="cargopolo",
            password="9pN2ayXE3HaUAt",
            database="formulario"
        )
        cursor = conn.cursor()
        query = "INSERT INTO saldo_combustivel_valecard (valor, data_insercao) VALUES (%s, %s)"
        cursor.execute(query, (valor_capturado, datetime.now()))
        conn.commit()
        print("✅ Dados gravados com sucesso!")

    except Exception as e:
        print(f"❌ Erro no ciclo: {e}")
        traceback.print_exc()

    finally:
        # Fecha conexões para evitar "leaks" de memória no servidor
        if cursor: cursor.close()
        if conn: conn.close()
        if driver: driver.quit()

    print("Aguardando 5 minutos para o próximo ciclo...\n")
    sleep(300)
