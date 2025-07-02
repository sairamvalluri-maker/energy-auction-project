import requests
from bs4 import BeautifulSoup
import sqlite3
import re

def clean_number(text):
    cleaned = re.sub(r"[^\d.,]", "", text).replace(",", ".").strip()
    return float(cleaned) if cleaned else 0.0

def scrape_data():
    url = "https://www.eex.com/en/markets/energy-certificates/french-auctions-power"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")

    if len(tables) < 3:
        print("Expected auction table not found.")
        return

    regional_table = tables[2]
    rows = regional_table.find_all("tr")[1:]
    data = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 4:
            region = cells[0].text.strip()
            volume_text = cells[2].text.strip()
            price_text = cells[3].text.strip()
            if not volume_text or not price_text:
                continue
            try:
                volume = clean_number(volume_text)
                price = clean_number(price_text)
                data.append((region, volume, price))
            except Exception as e:
                print("Skipping row due to error:", e)
                continue

    conn = sqlite3.connect("energy_data.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS auctions")
    cur.execute("""
        CREATE TABLE auctions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT,
            volume REAL,
            price REAL
        )
    """)
    cur.executemany("INSERT INTO auctions (region, volume, price) VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()
    print(f"Scraped and saved {len(data)} rows.")

if __name__ == "__main__":
    scrape_data()
