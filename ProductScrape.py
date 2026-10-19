# from bs4 import BeautifulSoup
import cloudscraper
import json
from playwright.sync_api import sync_playwright

url = "https://www.vevor.com.au/mig-welding-wire-c_12223/vevor-flux-core-mig-welding-wire-e71t-gs-0-03-10lbs-gasless-mild-steel-mig-wire-p_010994568578?requestId=6ad5a02571ad5000c41d03f3"

# requests returned 403, cloudscrape can bypass cloudflare
scraper = cloudscraper.create_scraper()

response = scraper.get(url)

print(response.status_code)
# print(response.text)

# soup = BeautifulSoup(response.text, "html.parser")

# JSON-LD : for seach engines, web crawlers, and AI systems with clear machine readable context about what's on a page
script=soup.select_one('script[type="application/ld+json"]')
data = json.loads(script.string)

print(data["name"])
print(data["offers"][0]["price"])

# Open Graph : used why websites and social platforms when displaying a link preview
title = soup.select_one('meta[property="og:title"]')["content"]
price = soup.select_one('meta[property="og:price:amount"]')["content"]

print(title, price)

# Because this website contains javascript, it requires real browser to executes and render if data were not present in headers
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(url, wait_until="domcontentloaded")
    page.locator("h1").first.wait_for()

    title = page.locator("h1").first.inner_text()

    print("Via playwright")
    print("Title:", title)

    browser.close()
