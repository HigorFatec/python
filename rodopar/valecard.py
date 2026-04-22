import os
import traceback
import mysql.connector
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Gerenciadores de driver e disfarce
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

while True:
    driver = None
    conn = None
    cursor = None

    try:
        print(f"--- Iniciando ciclo: {datetime.now()} ---")
        
        options = Options()
        
        # 1. DEFININDO O CAMINHO QUE VOCÊ ENCONTROU
        # O 'r' antes das aspas é vital para o Python entender as barras invertidas
        options.binary_location = r"U:\Users\higor.machado\.cache\selenium\chrome\win64\147.0.7727.117\chrome.exe"
        
        # 2. Configurações essenciais para o Windows Server
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # 3. Inicializa o Driver (Usando Service para evitar erros no Python 3.13)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # 4. Aplica o disfarce contra o Cloudflare
        stealth(driver,
                languages=["pt-BR", "pt"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        # --- A partir daqui, segue sua lógica original[cite: 3] ---
        driver.get('https://siag.valecard.com.br/frota/pages/start.jsf')
        wait = WebDriverWait(driver, 30)

        # Seleção do Perfil
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select'))).click()
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select/option[6]').click()

        # Login[cite: 3]
        wait.until(EC.presence_of_element_located((By.NAME, 'formLogin:j_id15')))
        driver.find_element(By.NAME, 'formLogin:j_id15').send_keys('higor.cargopolo')
        driver.find_element(By.NAME, 'formLogin:j_id17').send_keys('@Cargo20')
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[5]/input').click()

        sleep(10)

        # Extração e Banco de Dados[cite: 3]
        menu_alteracao = wait.until(EC.presence_of_element_located((By.ID, "MENU_FORM_HADOUKEN:j_id89")))
        actions = ActionChains(driver)
        actions.move_to_element(menu_alteracao).perform()

        submenu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']")))
        submenu.click()
        
        saldo_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//td[text()='Saldo Disponível']/following-sibling::td[1]")
        ))
        valor_capturado = saldo_element.text
        print(f"✅ Saldo Capturado: {valor_capturado}")

        # Conectar ao MySQL[cite: 3]
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
        print("✅ Dados salvos com sucesso!")

    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")
        traceback.print_exc()

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        if driver: driver.quit()

    print("Esperando 5 minutos para próxima execução...\n")
    sleep(300)
