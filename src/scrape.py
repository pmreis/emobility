import requests
from bs4 import BeautifulSoup

response = requests.get("https://mobie.pt/redemobie/encontrar-posto")
doc = BeautifulSoup(response.text, 'html.parser')

print(doc)
