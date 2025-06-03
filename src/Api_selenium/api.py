# src/Api_selenium/api.py

import platform
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from gclick_scraper import scrape_responsibles
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

@app.get("/")
def scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--single-process")

    system = platform.system()

    if system == "Windows":
        chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        chromedriver_path = r"C:\Users\fisca\OneDrive\Documentos\Projeto paineis\selenium-gclick-project\chromedriver-win64\chromedriver.exe"
        service = Service(executable_path=chromedriver_path)
    else:
        chrome_options.binary_location = "/usr/bin/chromium-browser"
        service = ChromeDriverManager().install()
    
    
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        dados = scrape_responsibles(driver)
        driver.quit()

        if dados:
            return {"success": True, "data": dados}
        else:
            return JSONResponse(status_code=404, content={"success": False, "message": "Nenhum dado foi coletado."})
    except Exception as e:
        driver.quit()
        return JSONResponse(status_code=500, content={"success": False, "message": str(e)})
