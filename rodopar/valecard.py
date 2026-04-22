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
    try:
        print(f"--- Iniciando Ciclo: {datetime.now()} ---")
        
        options = uc.ChromeOptions()
        # Força o navegador a abrir maximizado para evitar o erro de 'Out of Bounds'
        options.add_argument('--start-maximized')
        options.add_argument('--window-size=1920,1080')
        
        driver = uc.Chrome(options=options)
        
        # 1. Acesso ao SIAG
        driver.get('https://siag.valecard.com.br/frota/pages/start.jsf')
        wait = WebDriverWait(driver, 30)

        # 2. Seleção do Perfil
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select'))).click()
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select/option[6]').click()

        # 3. Login
        wait.until(EC.presence_of_element_located((By.NAME, 'formLogin:j_id15'))).send_keys('higor.cargopolo')
        driver.find_element(By.NAME, 'formLogin:j_id17').send_keys('@Cargo20')
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[5]/input').click()

        # Espera o Cloudflare e o carregamento do dashboard
        sleep(15) 

        # 4. Navegação nos Menus (Substituímos o move_to_element por um clique direto via JS para evitar erros de limite)
        try:
            menu_alteracao = wait.until(EC.presence_of_element_located((By.ID, "MENU_FORM_HADOUKEN:j_id89")))
            
            # Rola até o elemento antes de interagir
            driver.execute_script("arguments[0].scrollIntoView();", menu_alteracao)
            sleep(2)
            
            # Tenta o hover, se falhar, clica direto via JavaScript
            try:
                ActionChains(driver).move_to_element(menu_alteracao).perform()
            except:
                driver.execute_script("arguments[0].click();", menu_alteracao)

            submenu = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']")))
            submenu.click()
            
            sleep(5)

            # 5. Captura do Saldo
            saldo_elemento = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//td[text()='Saldo Disponível']/following-sibling::td[1]")
            ))
            valor_capturado = saldo_elemento.text
            print(f"✅ Saldo: {valor_capturado}")

            # 6. Banco de Dados
            conn = mysql.connector.connect(
                host="177.47.11.35", port=14804, user="cargopolo",
                password="9pN2ayXE3HaUAt", database="formulario"
            )
            cursor = conn.cursor()
            query = "INSERT INTO saldo_combustivel_valecard (valor, data_insercao) VALUES (%s, %s)"
            cursor.execute(query, (valor_capturado, datetime.now()))
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Gravado no banco!")

        except Exception as e_menu:
            print(f"❌ Erro na interação com menu/saldo: {e_menu}")
            # Tira um print para você ver o que o bot está vendo
            driver.save_screenshot("erro_menu.png")

    except Exception as e:
        print(f"❌ Erro Geral: {e}")
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()

    print("Aguardando 5 minutos...\n")
    sleep(300)
