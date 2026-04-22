from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth # <--- O segredo está aqui
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import mysql.connector
from datetime import datetime
import traceback
from selenium.webdriver.common.action_chains import ActionChains

while True:
    driver = None
    conn = None
    cursor = None

    try:
        # --- CONFIGURAÇÃO PARA NÃO SER DETECTADO ---
        options = Options()
        # Remove a mensagem "O Chrome está sendo controlado por software de teste"
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Inicia o driver (usando o manager para evitar erro de versão)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # APLICA O STEALTH (Disfarça o Selenium de navegador real)
        stealth(driver,
            languages=["pt-BR", "pt"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        # --- SEU FLUXO ORIGINAL ---
        driver.get('https://siag.valecard.com.br/frota/pages/start.jsf')
        wait = WebDriverWait(driver, 20)

        # Seleção do Perfil
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select'))).click()
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select/option[6]').click()

        # Login
        wait.until(EC.presence_of_element_located((By.NAME, 'formLogin:j_id15')))
        driver.find_element(By.NAME, 'formLogin:j_id15').send_keys('higor.cargopolo')
        driver.find_element(By.NAME, 'formLogin:j_id17').send_keys('@Cargo20')
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[5]/input').click()

        sleep(10)
        
        # Navegação no Menu
        actions = ActionChains(driver)
        menu_alteracao = wait.until(EC.presence_of_element_located((By.ID, "MENU_FORM_HADOUKEN:j_id89")))
        actions.move_to_element(menu_alteracao).perform()

        submenu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']")))
        submenu.click()
        
        sleep(5)

        # Captura do Saldo
        saldo_disponivel = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//td[text()='Saldo Disponível']/following-sibling::td[1]")
        ))
        valor_texto = saldo_disponivel.text
        print("Saldo Disponível:", valor_texto)

        # Inserção no MySQL
        try:
            conn = mysql.connector.connect(
                host="177.47.11.35", port=14804, user="cargopolo",
                password="9pN2ayXE3HaUAt", database="formulario"
            )
            cursor = conn.cursor()
            query = "INSERT INTO saldo_combustivel_valecard (valor, data_insercao) VALUES (%s, %s)"
            cursor.execute(query, (valor_texto, datetime.now()))
            conn.commit()
            print("✅ Saldo inserido com sucesso!")
        except Exception as db_e:
            print("❌ Erro no Banco:", db_e)

    except Exception as e:
        print("❌ Ocorreu um erro:", e)
        traceback.print_exc()

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        if driver: driver.quit()

    print("Esperando 5 minutos para próxima execução...\n")
    sleep(300)
