# B2B Lead Scraper - YellowPages (NYC Restaurants)

A production-ready Python web scraper that extracts local business leads from YellowPages across multiple catalog pages using BeautifulSoup and ScraperAPI to bypass anti-bot protections.

## Features
- **Anti-Bot Bypass**: Uses ScraperAPI proxy rotation to handle Cloudflare checks.
- **Multi-Page Pagination**: Automatically iterates through search result pages to collect datasets.
- **Structured Output**: Cleans and exports business names, phone numbers, and categories to CSV.

## Deliverable Sample
- `restaurant_leads_nyc_full.csv`: Sample dataset containing 90 extracted restaurant leads.

## Tech Stack
- Python 3
- `requests`
- `BeautifulSoup4`
- `ScraperAPI`
