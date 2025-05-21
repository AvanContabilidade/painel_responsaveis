import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import os


screenshot_dir = r"C:\Users\fisca\OneDrive\Documentos\Projeto paineis\selenium-gclick-project\Imagens"

if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_SENHA = os.getenv("DB_SENHA")


# Configurações do Selenium

def scrape_responsibles(driver):
    # URL da página de login
    login_url = "https://appp.gclick.com.br/autenticacao"
    try: 
        driver.get(login_url)
        print("Página de login acessada.")
    except Exception as e:
        print(f"Erro ao acessar a página de login: {e}")
        return []


    wait = WebDriverWait(driver, 60)

    # Preenche campo de usuário
    try:
        username_field = wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        username_field.send_keys(DB_USER)
        print("Campo de usuário preenchido.")
    except Exception as e:
        print(f"Erro ao preencher o campo de usuário: {e}")
        return []
    
    # Preenche campo de senha
    try:
        password_field = wait.until(EC.presence_of_element_located((By.ID, "mat-input-1")))
        password_field.send_keys(DB_SENHA)
        print("Campo de senha preenchido.")
    except Exception as e:
        print(f"Erro ao preencher o campo de senha: {e}")
        return []

    # Clica no botão de login
    try:
        login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submit-button")))
        login_button.click()
        print("Botão de login clicado.")
    except Exception as e:
        print(f"Erro ao clicar no botão de login: {e}")
        return []
    

    #checar o login 
    try: 
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "user-img-button")))
        print("Login realizado com sucesso.")
        driver.save_screenshot(os.path.join(screenshot_dir, "login_success.png"))
    except Exception as e:
        print(f"Erro ao realizar o login: {e}")
        driver.save_screenshot(os.path.join(screenshot_dir, "erro_login.png"))
        return []


    #ir direto pra URL das tarefas 
    try: 
        tarefas_url = "https://appp.gclick.com.br/relatorios/tarefas"
        driver.get(tarefas_url)
        print("Pagina de tarefas acessada.")
        driver.save_screenshot(os.path.join(screenshot_dir, "tarefas_page_accessed.png"))
    except Exception as e:
        print(f"Erro ao acessar a página de tarefas: {e}")
        driver.save_screenshot(os.path.join(screenshot_dir, "erro_tarefas_page.png"))
        return []


    wait = WebDriverWait(driver, 60)

    
    #Colocar filtro de responsáveis
    try:
        botao_colunas = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@mattooltip='Exibir/ocultar colunas']")))
        # Faz scroll até o botão para garantir que está visível
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_colunas)
        # Aguarda até estar clicável
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@mattooltip='Exibir/ocultar colunas']")))
        botao_colunas.click()
        print("Botão de colunas clicado.")
        driver.save_screenshot(os.path.join(screenshot_dir, "botao_colunas_clicked.png"))

    except Exception as e:
        print(f"Erro ao clicar no filtro de responsáveis: {e}")
        driver.save_screenshot(os.path.join(screenshot_dir, "erro_filtro_responsaveis.png"))
        return []
            
    #Selecionando filtro de responsáveis
    try:
        responsaveis_label = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'Responsáveis')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", responsaveis_label)

        ActionChains(driver).move_to_element(responsaveis_label).click().perform()
        print("Filtro 'Responsáveis' selecionado.")
        driver.save_screenshot(os.path.join(screenshot_dir, "filtro_responsaveis_selecionado.png"))
    except Exception as e:
        print(f"Erro ao selecionar o filtro 'Responsáveis': {e}")
        driver.save_screenshot(os.path.join(screenshot_dir, "erro_filtro_responsaveis_selecionar.png"))
        return []





    try:
        # Aguarda todos os botões com a classe 'success-button'
        botao_aplicar_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "success-button"))
        )
        botoes_aplicar = driver.find_elements(By.CLASS_NAME, "success-button")

        # Garante que há pelo menos dois botões
        if len(botoes_aplicar) >= 2:
            segundo_botao = botoes_aplicar[1]
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", segundo_botao)

            # Aguarda overlay sumir novamente antes do clique (caso tenha reaparecido)
            overlay_timeout = 10
            overlay_gone = False
            for _ in range(overlay_timeout * 2):
                overlays = driver.find_elements(By.CLASS_NAME, "cdk-overlay-backdrop")
                if not overlays or all(not o.is_displayed() for o in overlays):
                    overlay_gone = True
                    break
                time.sleep(0.5)

            if not overlay_gone:
                print("Overlay ainda presente após aguardar o segundo botão.")

            driver.execute_script("arguments[0].click();", segundo_botao)
            time.sleep(8)
            print("Segundo botão 'Aplicar' clicado com sucesso.")
            driver.save_screenshot(os.path.join(screenshot_dir, "segundo_botao_aplicar_clicked.png"))
        else:
            raise Exception("Não foi possível encontrar o segundo botão 'Aplicar'")

               
    except Exception:
        driver.execute_script("arguments[0].click();", botao_aplicar_menu)

        print("Botão 'Aplicar' do menu de filtros clicado com sucesso.")
        driver.save_screenshot(os.path.join(screenshot_dir, "botao_aplicar_menu_filtros_clicked.png"))
        # Aguarda até a coluna 'Responsáveis' estar visível na tabela
        try:
            responsaveis1 = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mat-column-responsaveis"))
            )
            driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth", responsaveis1)
            print("Coluna 'Responsáveis' detectada na tabela.")
            driver.save_screenshot(os.path.join(screenshot_dir, "coluna_responsaveis_detectada.png"))
        except Exception as e:
            print(f"Coluna 'Responsáveis' não apareceu a tempo: {e}")
            driver.save_screenshot(os.path.join(screenshot_dir, "erro_coluna_responsaveis_nao_apareceu.png"))
            return []
    except Exception as e:
                print(f"Erro ao clicar no botão 'Aplicar' do menu de filtros: {e}")
                driver.save_screenshot(os.path.join(screenshot_dir, "erro_botao_aplicar_menu_filtros.png"))


    
    try:
        box_itens = wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "mat-mdc-select-trigger")
        ))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", box_itens)
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(screenshot_dir, "box_itens_visivel.png"))
        box_itens.click()
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(screenshot_dir, "menu_itens_aberto.png"))
        # Aguarda o menu abrir e a opção aparecer pelo texto
        opcao_1000 = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), '1000')]")
        ))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opcao_1000)
        time.sleep(0.2)
        driver.save_screenshot(os.path.join(screenshot_dir, "opcao_1000_visivel.png"))
        opcao_1000.click()
        print("Selecionada a opção de mais itens por página.")
        driver.save_screenshot(os.path.join(screenshot_dir, "opcao_1000_clicada.png"))
        time.sleep(2)
    except Exception as e:
        print(f"Erro ao selecionar quantidade de itens por página: {e}")
        driver.save_screenshot(os.path.join(screenshot_dir, "erro_selecionar_itens_pagina.png"))



    wait = WebDriverWait(driver, 60)

    #pegar as informações dos responsáveis (meta e nome do mesmo)
    dados_responsaveis = []

    while True:
        print("Processando página atual...")

        try: 
            tbody = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//tbody[contains(@class, 'mdc-data-table__content')]")
            ))

            linhas = tbody.find_elements(By.TAG_NAME, "tr")
            for linha in linhas:
                try:
                    td_meta = linha.find_element(By.CLASS_NAME, "mat-column-dmeta")
                    td_responsavel = linha.find_element(By.CSS_SELECTOR, ".mat-column-responsaveis")
                    td_status = linha.find_element(By.CLASS_NAME, "mat-column-status")
                    driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth", td_responsavel)

                    meta = td_meta.text.strip()
                    responsavel = td_responsavel.text.strip()
                    status = td_status.text.strip()

                    dados_responsaveis.append([meta, responsavel, status])
                except Exception as e:
                    print(f"Erro ao extrair dados da linha: {e}")
                    continue

        except Exception as e:
            print(f"Erro ao processar a tabela: {e}")
            driver.save_screenshot(os.path.join(screenshot_dir, "erro_processar_tabela.png"))
            break

        # Tenta avançar para a próxima página 
        try: 
            proximo_btn = driver.find_element(By.XPATH, "//button[@aria-label='Próxima página' and not(@disabled)]")
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", proximo_btn)
            time.sleep(1)  # dá tempo pro scroll
            if not proximo_btn.is_enabled():
                print("Botão 'Próxima página' desabilitado, não há mais páginas.")
                break
            proximo_btn.click()
            time.sleep(6)  # Espera um pouco para a próxima página carregar
        except Exception:
            print("Não há mais páginas para avançar.")
            break

    print("Dados coletados:")
    for meta, responsavel, status in dados_responsaveis:
        print(f"Meta: {meta} | Responsável: {responsavel} | Status: {status}")

    return dados_responsaveis

    