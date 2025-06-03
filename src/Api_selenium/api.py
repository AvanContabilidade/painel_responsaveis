import platform
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from gclick_scraper import scrape_responsibles

app = Flask(__name__)

@app.route('/', methods=['GET'])
def scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--single-process")  # Importante para ambientes com poucos recursos

    system = platform.system()

    if system == "windows":
        chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        chromedriver_path = r"C:\Users\fisca\OneDrive\Documentos\Projeto paineis\selenium-gclick-project\chromedriver-win64\chromedriver.exe"
    else :
        chrome_options.binary_location = "/usr/bin/chromium-browser"  # Render usa Chromium
        chromedriver_path = "/usr/bin/chromedriver"  # Caminho padrão no Render
        
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try: 
        dados = scrape_responsibles(driver)
        driver.quit()

        if dados:
            return jsonify({"success": True, "data": dados}), 200
        else: 
            return jsonify({"success": False, "message": "Nenhum dado foi coletado."}), 404
    except Exception as e:
        driver.quit()
        return jsonify({"success": False, "message": str(e)}), 500
    

