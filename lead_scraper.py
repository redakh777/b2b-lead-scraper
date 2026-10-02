import random
import time
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

SEARCH_URL = "https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=New+York%2C+NY&page="


def scrape_leads(pages_to_scrape=2):
    leads = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-sandbox",
            ],
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            locale="en-US",
            timezone_id="America/New_York",
        )

        page = context.new_page()

        # Apply stealth patches to mask Playwright indicators
        stealth_sync(page)

        for page_num in range(1, pages_to_scrape + 1):
            target_url = f"{SEARCH_URL}{page_num}"
            print(f"Scraping Page {page_num}: {target_url}")

            try:
                page.goto(
                    target_url, wait_until="domcontentloaded", timeout=30000
                )

                # Give time for dynamic checks or manual challenge solving if prompted
                time.sleep(random.uniform(3.0, 5.0))

                if "Attention Required" in page.title():
                    print(
                        "Cloudflare challenge encountered. Please solve it manually in the browser window..."
                    )
                    page.wait_for_selector(
                        "div.result", timeout=60000
                    )  # Waits up to 60s for manual pass

                html_content = page.content()
            except Exception as e:
                print(f"Failed to load page {page_num}: {e}")
                continue

            soup = BeautifulSoup(html_content, "html.parser")
            listings = soup.find_all("div", class_="result")

            for item in listings:
                try:
                    name = item.find("a", class_="business-name").text.strip()
                except AttributeError:
                    name = "N/A"

                try:
                    phone = item.find("div", class_="phones").text.strip()
                except AttributeError:
                    phone = "N/A"

                try:
                    rating_div = item.find("div", class_="result-rating")
                    rating_class = rating_div["class"]
                    rating_str = [
                        c for c in rating_class if c != "result-rating"
                    ][0]
                    rating = rating_str.replace("-", ".")
                except (AttributeError, KeyError, IndexError):
                    rating = "N/A"

                try:
                    price = item.find("div", class_="price-range").text.strip()
                except AttributeError:
                    price = "N/A"

                try:
                    street = item.find(
                        "div", class_="street-address"
                    ).text.strip()
                    locality = item.find("div", class_="locality").text.strip()
                    address = f"{street}, {locality}"
                except AttributeError:
                    address = "N/A"

                leads.append(
                    {
                        "Business Name": name,
                        "Phone": phone,
                        "Rating": rating,
                        "Price Range": price,
                        "Address": address,
                    }
                )

            time.sleep(random.uniform(2.0, 4.0))

        browser.close()

    return leads


def export_to_csv(data, filename="restaurant_leads_nyc.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"\nDone! Scraped {len(df)} leads and saved to '{filename}'.")


if __name__ == "__main__":
    scraped_data = scrape_leads(pages_to_scrape=2)
    if scraped_data:
        export_to_csv(scraped_data)