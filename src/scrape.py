import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import csv


results = []

for year in range(2004, 2026):

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

            results.append({
                "date": dt.strptime(data, "%A %d %B %Y").strftime("%Y-%m-%d"),
                "numbers": numbers,
                "stars": stars,
                "jackpot": int(jackpot)
            })

results.sort(key=lambda r: r["date"])

with open("./../data/outputs/results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "numbers", "stars", "jackpot"])
    writer.writeheader()
    for r in results:
        writer.writerow({
            "date": r["date"],
            "numbers": " ".join(map(str, r["numbers"])),
            "stars": " ".join(map(str, r["stars"])),
            "jackpot": r["jackpot"]
        })
