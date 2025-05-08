import requests
from bs4 import BeautifulSoup
import csv

# URL for "Car Cover" search
url = "https://www.olx.in/items/q-car-cover"

# Set a user-agent to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_olx_data():
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    for listing in soup.select("li.EIR5N"):
        title = listing.select_one("span._2tW1I")
        price = listing.select_one("span._89yzn")
        location = listing.select_one("span._2tW1I._2fC2T")
        if title and price:
            items.append({
                "Title": title.get_text(strip=True),
                "Price": price.get_text(strip=True),
                "Location": location.get_text(strip=True) if location else "N/A"
            })

    return items

def save_to_csv(data, filename="olx_car_covers.csv"):
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Price", "Location"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    print("Fetching OLX Car Cover listings...")
    listings = fetch_olx_data()
    if listings:
        save_to_csv(listings)
    else:
        print("No data found or scraping failed.")
