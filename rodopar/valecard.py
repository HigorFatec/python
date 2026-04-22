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

def get_chrome_options():
    options = Options()
    
    # 1. Resolve o erro de "Cannot find Chrome binary" procurando caminhos comuns
    caminhos_chrome = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    for caminho in caminhos_chrome:
        if os.path.exists(caminho):
            options.binary_location = caminho
            break

    # 2. Configurações para ambiente de servidor
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Remove rastros de automação
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options

while True:
    driver = None
    conn = None
    cursor = None

    try:
        print(f"--- Iniciando ciclo: {datetime.now()} ---")
        
        # Inicializa o Driver com Service (evita erros de binário no Python 3.13)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=get_chrome_options())

        # Aplica o "Stealth" para burlar o Cloudflare
        stealth(driver,
                languages=["pt-BR", "pt"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        # Acessa o site
        driver.get('https://siag.valecard.com.br/frota/pages/start.jsf')
        wait = WebDriverWait(driver, 30)

        # Seleção do Perfil
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select'))).click()
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select/option[6]').click()

        # Login
        wait.until(EC.presence_of_element_located((By.NAME, 'formLogin:j_id15')))
        driver.find_element(By.NAME, 'formLogin:j_id15').send_keys('higor.cargopolo')
        driver.find_element(By.NAME, 'formLogin:j_id17').send_keys('@Cargo20')
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[5]/input').click()

        sleep(10) # Aguarda carregamento pós-login

        # Navegação no Menu
        try:
            menu_alteracao = wait.until(EC.presence_of_element_located((By.ID, "MENU_FORM_HADOUKEN:j_id89")))
            actions = ActionChains(driver)
            actions.move_to_element(menu_alteracao).perform()

            submenu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']")))
            submenu.click()
            
            sleep(5)

            # Captura do Saldo
            saldo_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//td[text()='Saldo Disponível']/following-sibling::td[1]")
            ))
            valor_texto = saldo_element.text
            print(f"Saldo localizado: {valor_texto}")

            # Inserção no Banco de Dados
            conn = mysql.connector.connect(
                host="177.47.11.35",
                port=14804,
                user="cargopolo",
                password="9pN2ayXE3HaUAt",
                database="formulario"
            )
            cursor = conn.cursor()
            query = "INSERT INTO saldo_combustivel_valecard (valor, data_insercao) VALUES (%s, %s)"
            cursor.execute(query, (valor_texto, datetime.now()))
            conn.commit()
            print("✅ Sucesso: Saldo salvo no MySQL.")

        except Exception as e_intern:
            print(f"❌ Erro na extração/banco: {e_intern}")
            traceback.print_exc()

    except Exception as e:
        print(f"❌ Erro crítico no ciclo: {e}")
        traceback.print_exc()

    finally:
        # Encerramento limpo de todas as conexões
        if cursor: cursor.close()
        if conn: conn.close()
        if driver: driver.quit()

    print("Aguardando 5 minutos para a próxima execução...\n")
    sleep(300)
