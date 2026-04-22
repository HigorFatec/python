import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import mysql.connector
from datetime import datetime
import traceback
from time import sleep

while True:
    driver = None
    conn = None
    cursor = None

    try:
        print(f"--- Iniciando Ciclo Anti-Bloqueio: {datetime.now()} ---")
        
        options = uc.ChromeOptions()
        # Removido o binary_location pois agora está no padrão do C:\
        # Se quiser rodar sem janela no futuro: options.add_argument('--headless')
        
        # O UC vai encontrar o Chrome no C:\ sozinho agora
        driver = uc.Chrome(options=options)
        
        # 1. Acesso ao SIAG Valecard
        driver.get('https://siag.valecard.com.br/frota/pages/start.jsf')
        wait = WebDriverWait(driver, 30)

        # 2. Seleção do Perfil
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select'))).click()
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select/option[6]').click()

        # 3. Login
        wait.until(EC.presence_of_element_located((By.NAME, 'formLogin:j_id15'))).send_keys('higor.cargopolo')
        driver.find_element(By.NAME, 'formLogin:j_id17').send_keys('@Cargo20')
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[5]/input').click()

        # ESPERA ESTRATÉGICA: Dá tempo para o Cloudflare validar o "humano"
        sleep(15) 

        # 4. Navegação nos Menus
        menu_alteracao = wait.until(EC.presence_of_element_located((By.ID, "MENU_FORM_HADOUKEN:j_id89")))
        ActionChains(driver).move_to_element(menu_alteracao).perform()

        submenu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']")))
        submenu.click()
        
        sleep(5)

        # 5. Captura do Saldo
        saldo_elemento = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//td[text()='Saldo Disponível']/following-sibling::td[1]")
        ))
        valor_capturado = saldo_elemento.text
        print(f"✅ Saldo Capturado: {valor_capturado}")

        # 6. Gravação no MySQL
        conn = mysql.connector.connect(
            host="177.47.11.35", port=14804, user="cargopolo",
            password="9pN2ayXE3HaUAt", database="formulario"
        )
        cursor = conn.cursor()
        query = "INSERT INTO saldo_combustivel_valecard (valor, data_insercao) VALUES (%s, %s)"
        cursor.execute(query, (valor_capturado, datetime.now()))
        conn.commit()
        print("✅ Dados gravados com sucesso!")

    except Exception as e:
        print(f"❌ Erro detectado: {e}")
        traceback.print_exc()

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        if driver: driver.quit()

    print("Dormindo 5 minutos...\n")
    sleep(300)
