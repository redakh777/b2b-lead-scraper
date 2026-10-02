import csv
import time
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
API_KEY = "YOUR_SCRAPERAPI_KEY"  # Replace with your actual ScraperAPI key
BASE_URL = "https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=New+York%2C+NY&page={}"
API_ENDPOINT = "https://api.scraperapi.com"

all_leads = []

# Scrape Pages 1 through 3
for page_num in range(1, 4):
    target_url = BASE_URL.format(page_num)
    print(f"Scraping Page {page_num}: {target_url}...")
    
    params = {
        "api_key": API_KEY,
        "url": target_url,
        "render": "true",
        "country_code": "us"
    }
    
    try:
        response = requests.get(API_ENDPOINT, params=params, timeout=60)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.find_all("div", class_="result")
            
            for listing in listings:
                name_tag = listing.find("a", class_="business-name")
                phone_tag = listing.find("div", class_="phones")
                category_tag = listing.find("div", class_="categories")
                
                name = name_tag.get_text(strip=True) if name_tag else "N/A"
                phone = phone_tag.get_text(strip=True) if phone_tag else "N/A"
                categories = category_tag.get_text(strip=True) if category_tag else "N/A"
                
                all_leads.append({
                    "Business Name": name,
                    "Phone": phone,
                    "Category": categories
                })
            print(f"  Captured {len(listings)} leads from page {page_num}.")
        else:
            print(f"  Failed page {page_num}. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"  Error on page {page_num}: {e}")
        
    time.sleep(1)

# Save total results to CSV
output_filename = "restaurant_leads_nyc_full.csv"
with open(output_filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Business Name", "Phone", "Category"])
    writer.writeheader()
    writer.writerows(all_leads)

print(f"\nDone! Scraped total of {len(all_leads)} leads across 3 pages into '{output_filename}'.")