import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import csv
from pathlib import Path
import os.path as osp
from dataclasses import dataclass

@dataclass(frozen=True)
class CsvRow:
    date: str
    numbers: str
    stars: str
    jackpot: str

# Set path and file
projRootPath = Path(__file__).resolve().parent.parent
filepath = osp.normpath(f'{projRootPath}/data/outputs/results.csv')

results = set()

try:
    with open(filepath, "r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            sourceRow = CsvRow(
                date=linha["date"],
                numbers=linha["numbers"],
                stars=linha["stars"],
                jackpot=linha["jackpot"]
            )
            results.add(sourceRow)
except FileNotFoundError:
    results = set()

latestYear = int(max(record.date.split('-', 1)[0] for record in results))

for year in range(latestYear, latestYear+2):
    response = requests.get(f"https://www.euro-millions.com/results-history-{year}")
    soup = BeautifulSoup(response.text, 'html.parser')

    for row in soup.select("tr.resultRow"):
        date_elem = row.select_one("td.date")
        balls_elem = row.select("ul.balls li")
        jackpot_elem = row.select_one("td[data-title='Jackpot'] strong")

        if date_elem and balls_elem and jackpot_elem:
            data = date_elem.get_text(separator=" ", strip=True).strip().replace(" st ", " ").replace(" nd ", " ").replace(" rd ", " ").replace(" th ", " ")
            numbers = [int(b.get_text()) for b in balls_elem if "lucky-star" not in b["class"]]
            stars = [int(b.get_text()) for b in balls_elem if "lucky-star" in b["class"]]
            jackpot = jackpot_elem.get_text(strip=True).replace("€", "").replace(",", "").strip()

            sourceRow = CsvRow(
                date=dt.strptime(data, "%A %d %B %Y").strftime("%Y-%m-%d"),
                numbers=" ".join(str(n) for n in numbers),
                stars=" ".join(str(n) for n in stars),
                jackpot=int(jackpot)
            )
            results.add(sourceRow)

resultsList = list(results)
resultsList.sort(key=lambda row: row.date, reverse=True)
columns = ["date", "numbers", "stars", "jackpot"]

if resultsList:
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in resultsList:
            writer.writerow(row.__dict__)
