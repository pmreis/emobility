from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
import time
import json
import sys

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless=new",
    "--disable-blink-features=AutomationControlled",
    #"--disable-gpu",
    "--window-size=1920,1080",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--lang=pt-PT",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """
})

try:
    driver.get("https://mobie.pt/redemobie/encontrar-posto")
    print("Wait a few seconds for page to fully load")
    time.sleep(10)

    for request in driver.requests:
        if "mobierest/locations" in request.url and request.response:
            status = request.response.status_code
            print("URL:", request.url)
            print("Status:", status)
            print("Headers:", request.response.headers)
            print("Body:", request.response.body.decode('utf-8'))

            if status == 400:
                driver.quit()
                sys.exit(1)

            #file = open("./data/outputs/mobie_locations.json", "w", encoding="utf-8")
            #file.write(request.response.body.decode('utf-8'))
            #file.close()
            break

finally:
    driver.quit()