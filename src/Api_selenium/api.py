import platform
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from gclick_scraper import scrape_responsibles
import chromedriver_autoinstaller
import os 

app = FastAPI()

def create_driver():
    chrome_options = Options()
    
    # Configurações para rodar no Render.com
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-extensions")
    
    # Configurações específicas para o Chrome no Linux
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-setuid-sandbox')
    
    try:
        # Define o caminho correto para o Chrome
        chrome_options.binary_location = "/usr/bin/google-chrome"  # Caminho padrão do Chrome no Linux
        
        # Configura o Service com opções adicionais
        service = Service(
            ChromeDriverManager().install(),
            service_args=['--verbose']
        )
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Falha ao iniciar o ChromeDriver: {str(e)}"
        )

@app.get("/scrape")
def scrape():
    driver = None
    try:
        driver = create_driver()
        dados = scrape_responsibles(driver)
        
        if dados:
            return {"success": True, "data": dados}
        else:
            raise HTTPException(
                status_code=404,
                detail="Nenhum dado foi coletado."
            )
            
    except HTTPException:
        raise  # Re-lança exceções HTTP que já tratamos
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro durante o scraping: {str(e)}"
        )
    finally:
        if driver:
            driver.quit()


@app.get("/")
def read_root():
    return JSONResponse(content={"message": "API de scraping do GClick está rodando! -> Use /scrape para coletar dados."})