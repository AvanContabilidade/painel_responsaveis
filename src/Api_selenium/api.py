import platform
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from gclick_scraper import scrape_responsibles
import chromedriver_autoinstaller
import os 

app = FastAPI()

def create_driver():
    chrome_options = Options()
    chrome_options.binary_location = "/opt/chrome/chrome"

    # Adiciona ao PATH para que o Chrome seja encontrado
    os.environ["PATH"] += os.pathsep + "/opt/chrome"

    chromedriver_autoinstaller.install()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao iniciar o ChromeDriver: {str(e)}")


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