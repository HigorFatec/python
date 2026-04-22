from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
import mysql.connector
from datetime import datetime
import traceback

# Configurações do Banco de Dados
DB_CONFIG = {
    "host": "177.47.11.35",
    "port": 14804,
    "user": "cargopolo",
    "password": "9pN2ayXE3HaUAt",
    "database": "formulario"
}

while True:
    driver = None
    conn = None
    cursor = None

    try:
        print(f"Iniciando execução em: {datetime.now()}")
        
        # 1. Configurações do Firefox para o Servidor
        firefox_options = Options()
        # Caminho informado por você
        firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        
        # Disfarces para evitar detecção de bot no Firefox
        firefox_options.set_preference("dom.webdriver.enabled", False)
        firefox_options.set_preference('useAutomationExtension', False)
        
        # Define uma resolução fixa para evitar bloqueios do Cloudflare
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        # 2. Inicializa o Driver
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)

        # 3. Navegação Inicial
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

        sleep(10) # Aguarda o dashboard carregar

        # 4. Navegação nos Menus (Simulando Mouse)
        try:
            # Menu "Alteração"
            menu_alteracao = wait.until(EC.presence_of_element_located((By.ID, "MENU_FORM_HADOUKEN:j_id89")))
            actions = ActionChains(driver)
            actions.move_to_element(menu_alteracao).perform()

            # Submenu
            submenu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']")))
            submenu.click()
            
            sleep(5)

            # Captura do Saldo
            saldo_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//td[text()='Saldo Disponível']/following-sibling::td[1]")
            ))
            valor_saldo = saldo_element.text
            print(f"Saldo Capturado: {valor_saldo}")

            # 5. Inserção no Banco de Dados
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                query = "INSERT INTO saldo_combustivel_valecard (valor, data_insercao) VALUES (%s, %s)"
                cursor.execute(query, (valor_saldo, datetime.now()))
                conn.commit()
                print("✅ Saldo inserido no banco com sucesso!")
            except Exception as db_e:
                print(f"❌ Erro no Banco de Dados: {db_e}")
                traceback.print_exc()

        except Exception as menu_e:
            print(f"❌ Erro na navegação interna: {menu_e}")
            traceback.print_exc()

    except Exception as e:
        print(f"❌ Erro Geral: {e}")
        traceback.print_exc()

    finally:
        # Encerramento Seguro
        if cursor: cursor.close()
        if conn: conn.close()
        if driver: driver.quit()

    print("Esperando 5 minutos para a próxima execução...\n")
    sleep(300)
