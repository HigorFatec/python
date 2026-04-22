from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from time import sleep
import mysql.connector
from datetime import datetime
import traceback

while True:
    driver = None
    conn = None
    cursor = None

    try:
        # Configurações para o servidor não ser detectado
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Inicializa o Driver padrão (resolve o erro de Binary Location)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Aplica o Stealth (Disfarce de Humano)
        stealth(driver,
                languages=["pt-BR", "pt"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        driver.get('https://siag.valecard.com.br/frota/pages/start.jsf')
        wait = WebDriverWait(driver, 30) # Tempo maior para o servidor

        # --- Início da sua lógica original ---
        # Seleção da opção no dropdown
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select'))).click()
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select/option[6]').click()

        # Login
        wait.until(EC.presence_of_element_located((By.NAME, 'formLogin:j_id15')))
        driver.find_element(By.NAME, 'formLogin:j_id15').send_keys('higor.cargopolo')
        driver.find_element(By.NAME, 'formLogin:j_id17').send_keys('@Cargo20')
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[5]/input').click()

        sleep(10)

        # Navegação nos Menus
        menu_alteracao = wait.until(EC.presence_of_element_located((By.ID, "MENU_FORM_HADOUKEN:j_id89")))
        actions = ActionChains(driver)
        actions.move_to_element(menu_alteracao).perform()

        submenu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']")))
        submenu.click()
        
        # Captura do Saldo
        saldo_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//td[text()='Saldo Disponível']/following-sibling::td[1]")
        ))
        valor_saldo = saldo_element.text
        print(f"Saldo Disponível: {valor_saldo}")

        # Banco de Dados
        conn = mysql.connector.connect(
            host="177.47.11.35",
            port=14804,
            user="cargopolo",
            password="9pN2ayXE3HaUAt",
            database="formulario"
        )
        cursor = conn.cursor()
        query = "INSERT INTO saldo_combustivel_valecard (valor, data_insercao) VALUES (%s, %s)"
        cursor.execute(query, (valor_saldo, datetime.now()))
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
