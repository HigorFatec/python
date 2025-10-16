from selenium import webdriver
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
        driver = webdriver.Chrome()
        driver.get('https://siag.valecard.com.br/frota/pages/start.jsf')

        # Aqui você cria o WebDriverWait para este driver:
        wait = WebDriverWait(driver, 20)

        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select').click()

        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[4]/select/option[6]').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'formLogin:j_id15')))
        driver.find_element(By.NAME, 'formLogin:j_id15').send_keys('higor.cargopolo')
        driver.find_element(By.NAME, 'formLogin:j_id17').send_keys('Car123$$')

        # Submeter o formulário
        driver.find_element(By.XPATH, '//*[@id="wrap-geral"]/div[2]/div/div/ul/li[5]/input').click()

        sleep(10)  # Espera a página carregar
        
        actions = ActionChains(driver)

        try:

            wait = WebDriverWait(driver, 10)

            # 1️⃣ Espera o menu principal "Alteração" aparecer
            menu_alteracao = wait.until(
                EC.presence_of_element_located((By.ID, "MENU_FORM_HADOUKEN:j_id89"))
            )

            # 2️⃣ Usa ActionChains para passar o mouse sobre o menu (abrir o dropdown)
            actions = ActionChains(driver)
            actions.move_to_element(menu_alteracao).perform()

            # 3️⃣ Espera o submenu aparecer (por exemplo, "Cancelamento de Cartão")
            submenu = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='MENU_FORM_HADOUKEN:j_id94:icon']"))
            )

            #4️⃣ Clica na opção desejada
            submenu.click()
            sleep(5)  # Espera a página carregar

            # Localiza o valor após o texto "Saldo Disponível"
            saldo_disponivel = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//td[text()='Saldo Disponível']/following-sibling::td[1]")
                )
            )

            print("Saldo Disponível:", saldo_disponivel.text)


            #sleep(1000)

            print("✅ Clique realizado com sucesso no menu Distribuição de Saldo de Filial!")
        except Exception as e:
            print("❌ Erro ao clicar no menu:", e)
            traceback.print_exc()



        sleep(10)

        try:
            # Conectar ao MySQL
            conn = mysql.connector.connect(
            host="177.47.11.35",
            port=14804,
            user="cargopolo",
            password="9pN2ayXE3HaUAt",
            database="formulario"
            )
            
            cursor = conn.cursor()

            query = """INSERT INTO saldo_combustivel_valecard (valor, data_insercao) VALUES (%s, %s)"""

            params = (saldo_disponivel.text, datetime.now())
            cursor.execute(query, params)

            conn.commit()

            print("Saldo inserido com sucesso no banco de dados! Valor:", saldo_disponivel.text)
            print(datetime.now())
        except Exception as e:
            print("Ocorreu um erro ao inserir no banco de dados:", e)
            traceback.print_exc()


        
    except Exception as e:
        print("Ocorreu um erro:", e)
        traceback.print_exc()

    finally:
        # Fechar conexões e driver, se existirem
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            print("Erro ao fechar cursor:", e)
        try:
            if conn:
                conn.close()
        except Exception as e:
            print("Erro ao fechar conexão:", e)
        try:
            if driver:
                driver.quit()
        except Exception as e:
            print("Erro ao fechar driver:", e)

    # Espera 5 minutos antes da próxima execução
    print("Esperando 5 minutos para próxima execução...\n")
    sleep(300)
