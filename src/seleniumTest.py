from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from io import BytesIO
import platform
import gzip
import json
import sys
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.by import By
#import time


if platform.system() == "Windows":
    chrome_service = Service(executable_path="./chromedriver.exe")
else:
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless=new",
    "--disable-blink-features=AutomationControlled",
    "--disable-gpu",
    "--window-size=1920,1080",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
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
    result = driver.get("https://mobie.pt/redemobie/encontrar-posto")

    #actions = ActionChains(driver)
    #element = driver.find_element(By.CLASS_NAME, "section-subheader-bold")
    #actions.move_to_element(element).click().perform()
    #element = driver.find_element(By.ID, "searchBox")
    #actions.move_to_element(element).click().perform()

    #driver.implicitly_wait(10)

    print("Total requests: " + str(len(driver.requests)))

    for request in driver.requests:
        if "mobierest/locations" in request.url:
            status = request.response.status_code
            print("URL:", request.url)
            print("Request method:", request.method)
            print("Status:", status)

            if status == 400:
                driver.quit()
                sys.exit(1)
       
            compressed_data = request.response.body
            with gzip.GzipFile(fileobj=BytesIO(compressed_data)) as f:
                decompressed = f.read()

            text = decompressed.decode("utf-8")    
            data = json.loads(text)

            file = open("./../data/sources/mobie_locations.json", "w", encoding="utf-8")
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
            file.close()

            print("Saved new locations")

            break

finally:
    driver.quit()