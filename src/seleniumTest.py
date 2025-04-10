from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import json
import sys

#chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

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
    "--lang=pt-PT"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=ChromeDriverManager().install(), options=chrome_options)

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

    actions = ActionChains(driver)
    element = driver.find_element(By.CLASS_NAME, "section-subheader-bold")
    actions.move_to_element(element).click().perform()
    element = driver.find_element(By.ID, "searchBox")
    actions.move_to_element(element).click().perform()

    for request in driver.requests:
        if "mobierest/locations" in request.url and request.response:
            status = request.response.status_code
            print("URL:", request.url)
            print("Request method:", request.method)
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