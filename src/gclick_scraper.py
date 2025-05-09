from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver



def scrape_responsibles(driver):


    driver.get("https://appp.gclick.com.br/relatorios/tarefas")  # URL do Gclick

    wait = WebDriverWait(driver, 10)  # Configura espera dinâmica

    # Clica no botão para abrir as opções de colunas
    try:
        button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mat-mdc-button-touch-target")))
        button.click()
    except Exception as e:
        print(f"Erro ao clicar no botão: {e}")
        return []

    # Seleciona a checkbox de "Responsável"
    try:
        checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Responsável')]/preceding-sibling::mat-checkbox")))
        checkbox.click()
    except Exception as e:
        print(f"Erro ao selecionar a checkbox de 'Responsável': {e}")
        return []

    # Clica no botão "Aplicar" para aplicar as configurações
    try:
        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aplicar')]")))
        save_button.click()
    except Exception as e:
        print(f"Erro ao clicar no botão 'Salvar': {e}")
        return []

    # Aguarda os elementos da tabela carregarem
    try:
        rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "mat-ripple mat-mdc-button-ripple")))  
    except Exception as e:
        print(f"Erro ao carregar as linhas da tabela: {e}")
        return []

    # Captura os dados da coluna "Responsáveis e Nome"
    responsibles = []
    for row in rows:
        try:
            # Localiza o nome do responsável na linha
            responsible_name = row.find_element(By.CSS_SELECTOR, "mat-sort-header-content ng-tns-c1137168538-63").text  # Substitua pelo seletor correto
            
            # Localiza o nome da tarefa ou outro dado relacionado na mesma linha
            task_name = row.find_element(By.CSS_SELECTOR, "mat-sort-header-content ng-tns-c1137168538-45").text  # Substitua pelo seletor correto
            
            # Relaciona o responsável com o nome da tarefa
            responsibles.append({"responsavel": responsible_name, "tarefa": task_name})
        except Exception as e:
            print(f"Erro ao capturar os dados da linha: {e}")

    return responsibles