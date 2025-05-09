from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from gclick_scraper import scrape_responsibles  # Importa a função de scraping
import os

def main():
    # Configurações do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # (Opcional) Se quiser usar um Chrome fora do padrão, descomente e ajuste:
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    # Caminho absoluto para o chromedriver
    chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "chromedriver.exe"))
    service = Service(chromedriver_path)
    # Inicializa o WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Chama a função de scraping
        responsibles = scrape_responsibles(driver)

        # Exibe os resultados
        print("Responsáveis e Tarefas:")
        for item in responsibles:
            print(f"Responsável: {item['responsavel']}, Tarefa: {item['tarefa']}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
