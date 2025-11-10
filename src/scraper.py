# open a browser session using Playwright
# wait
# scrape with beautifulsoup

from playwright.sync_api import sync_playwright 
from bs4 import BeautifulSoup
import os

def get_page_content(url):
    with sync_playwright() as p: # starts a Playwright session
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector('.title--wrap--UUHae_g', timeout=15000)
        # page.click('button:has-text("View more")', timeout=2000)
        # page.wait_for_selector('.specification--line--IXeRJI7', timeout=5000)
        content = page.content()
        browser.close()
        return content
    
def parse_with_beautifulsoup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # title
    title_div = soup.find(class_='title--wrap--UUHae_g')
    title = title_div.get_text()

    # desc 
    # class="seo-sellpoints--sellerPoint--RcmFO_y"

    # specification
    spec_list = soup.find(class_='specification--list--GZuXzRX')
    spec = {}
    # only getting 6 we have to click view more button to get all specification.

    spec_line = spec_list.find_all('li', class_='specification--line--IXeRJI7')

    for line in spec_line:
        props = line.find_all('div', class_='specification--prop--Jh28bKu')

        for prop in props:
            key_div = prop.find('div', class_='specification--title--SfH3sA8')
            key = key_div.get_text(strip=True) if key_div else 'N/A'

            value_div = prop.find('div', class_='specification--desc--Dxx6W0W')
            value = value_div.get_text(strip=True) if key_div else 'N/A'

            spec[key] = value
            
    return title, spec

