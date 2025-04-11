from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import json
import sys

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
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

#driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#    "source": """
#        Object.defineProperty(navigator, 'webdriver', {
#            get: () => undefined
#        });
#    """
#})

try:
    driver.get("https://mobie.pt/redemobie/encontrar-posto")

    driver.implicitly_wait(5)
    
    actions = ActionChains(driver)
    element = driver.find_element(By.CLASS_NAME, "section-subheader-bold")
    actions.move_to_element(element).click().perform()
    element = driver.find_element(By.ID, "searchBox")
    actions.move_to_element(element).click().perform()

    print("Total requests: " + str(len(driver.requests)))

    for request in driver.requests:
        if "mobierest/locations" in request.url and request.response:
            status = request.response.status_code
            print("URL:", request.url)
            print("Request method:", request.method)
            print("Status:", status)

            if status == 400:
                driver.quit()
                sys.exit(1)

            file = open("./data/outputs/mobie_locations.json", "w", encoding="utf-8")
            file.write(request.response.body.decode('utf-8'))
            file.close()

            print("Saved new locations")

            break

finally:
    driver.quit()