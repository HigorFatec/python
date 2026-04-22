import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
from datetime import datetime
import traceback
from time import sleep

while True:
    driver = None
    try:
        print(f"--- Ciclo Anti-Erro de Limites: {datetime.now()} ---")
        
        options = uc.ChromeOptions()
        # Forçamos uma resolução alta para que nada fique "fora da tela"
        options.add_argument('--window-size=1920,1080')
        options.add_argument("--start-maximized")
        
        driver = uc.Chrome(options=options)
        
        # 1. Acesso e Login
        driver.get('https://siag.valecard.com.br/frota/pages/start.jsf')
        wait = WebDriverWait(driver, 40)

        # Seleção de Perfil
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select'))).click()
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select/option[6]').click()

        # Dados de Acesso
        wait.until(EC.presence_of_element_located((By.NAME, 'formLogin:j_id15'))).send_keys('higor.cargopolo')
        driver.find_element(By.NAME, 'formLogin:j_id17').send_keys('@Cargo20')
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[5]/input').click()

        # Pausa maior para o Cloudflare processar (Captura de tela 2026-04-22 173034.png)
        sleep(20) 

        # 2. RESOLVENDO O ERRO DE MOVIMENTO (MoveTargetOutOfBounds)
        # Em vez de ActionChains (que move o mouse físico), usamos CLIQUE VIA JAVASCRIPT DIRETO.
        # Isso ignora se o elemento está "fora da tela" ou escondido.
        
        print("Tentando acessar o menu via JS...")
        menu_id = "MENU_FORM_HADOUKEN:j_id89"
        submenu_xpath = "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']"
        
        # Espera o menu existir no código
        menu_element = wait.until(EC.presence_of_element_located((By.ID, menu_id)))
        
        # Força o clique no menu principal para abrir as opções
        driver.execute_script("arguments[0].click();", menu_element)
        sleep(3)
        
        # Localiza e clica no submenu (Saldo) também via JS
        submenu_element = wait.until(EC.presence_of_element_located((By.XPATH, submenu_xpath)))
        driver.execute_script("arguments[0].click();", submenu_element)
        
        print("✅ Navegação de menu concluída sem usar movimento de mouse.")
        sleep(7)

        # 3. Captura do Saldo
        saldo_xpath = "//td[text()='Saldo Disponível']/following-sibling::td[1]"
        saldo_elemento = wait.until(EC.presence_of_element_located((By.XPATH, saldo_xpath)))
        
        valor_capturado = saldo_elemento.text
        print(f"💰 Saldo Extraído: {valor_capturado}")

        # 4. Banco de Dados
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
        print("🚀 Sucesso total!")

    except Exception as e:
        print(f"❌ Falha no ciclo: {e}")
        # Se falhar, tira um print da tela para sabermos se parou no Cloudflare ou no menu
        if driver:
            driver.save_screenshot("ultimo_erro.png")
            print("📸 Screenshot do erro salvo como 'ultimo_erro.png'")
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()

    print("Próximo teste em 5 minutos...")
    sleep(300)
