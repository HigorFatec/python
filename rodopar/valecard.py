from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
from datetime import datetime
import traceback
from selenium.webdriver.common.action_chains import ActionChains

# 1. CAMINHO QUE VOCÊ ACHOU NO GERENCIADOR DE TAREFAS
# Precisamos avisar o Selenium onde o Chrome está, senão ele dá o erro de "cannot find binary"
CHROME_BINARY = r"U:\Users\higor.machado\.cache\selenium\chrome\win64\147.0.7727.117\chrome.exe"

while True:
    driver = None
    conn = None
    cursor = None

    try:
        print(f"--- Iniciando Ciclo: {datetime.now()} ---")
        
        options = Options()
        # Define o local do Chrome para corrigir o erro do seu print
        options.binary_location = CHROME_BINARY
        
        # Configurações para não ser detectado
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Gerencia o driver automaticamente
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Aplica o disfarce (Stealth)
        stealth(driver,
            languages=["pt-BR", "pt"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        # --- SEU FLUXO DE NAVEGAÇÃO ---
        driver.get('https://siag.valecard.com.br/frota/pages/start.jsf')
        wait = WebDriverWait(driver, 30)

        # Seleção de Perfil
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select'))).click()
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select/option[6]').click()

        # Login
        wait.until(EC.presence_of_element_located((By.NAME, 'formLogin:j_id15'))).send_keys('higor.cargopolo')
        driver.find_element(By.NAME, 'formLogin:j_id17').send_keys('@Cargo20')
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[5]/input').click()

        sleep(10)
        
        # Navegação no Menu
        menu_alteracao = wait.until(EC.presence_of_element_located((By.ID, "MENU_FORM_HADOUKEN:j_id89")))
        ActionChains(driver).move_to_element(menu_alteracao).perform()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']"))).click()
        
        # Captura de Saldo
        saldo_disponivel = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//td[text()='Saldo Disponível']/following-sibling::td[1]")
        ))
        valor_capturado = saldo_disponivel.text
        print(f"✅ Saldo Capturado: {valor_capturado}")

        # Inserção no MySQL
        conn = mysql.connector.connect(
            host="177.47.11.35", port=14804, user="cargopolo",
            password="9pN2ayXE3HaUAt", database="formulario"
        )
        cursor = conn.cursor()
        query = "INSERT INTO saldo_combustivel_valecard (valor, data_insercao) VALUES (%s, %s)"
        cursor.execute(query, (valor_capturado, datetime.now()))
        conn.commit()
        print("✅ Dados gravados!")

    except Exception as e:
        print(f"❌ Erro: {e}")
        traceback.print_exc()

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        if driver: driver.quit()

    print("Aguardando 5 minutos...\n")
    sleep(300)
