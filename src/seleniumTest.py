from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
import time
import json

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


try:
    driver.get("https://mobie.pt/redemobie/encontrar-posto")
    print("Wait a few seconds for page to fully load")
    time.sleep(10)

    for request in driver.requests:
        if "mobierest/locations" in request.url and request.response:
            data = request.response.body.decode("utf-8")
            print("locations size is " + str(len(data)))
            json_data = json.loads(data)

            with open("./data/outputs/mobie_locations.json", "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            break

finally:
    driver.quit()