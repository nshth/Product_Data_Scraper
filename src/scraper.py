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
        page.goto(url, timeout=120000)
        page.wait_for_selector('.title--wrap--UUHae_g', timeout=15000)

        view_more_button = page.locator("button.specification--btn--Y4pYc4b:has-text('View more')")
        if view_more_button.count() > 0 and view_more_button.first.is_visible(): # only if its available
            view_more_button.first.click()
            page.wait_for_selector('.specification--prop--Jh28bKu', timeout=5000)

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

    spec_line = spec_list.find_all('li', class_='specification--line--IXeRJI7')

    for line in spec_line:
        props = line.find_all('div', class_='specification--prop--Jh28bKu')

        for prop in props:
            key_div = prop.find('div', class_='specification--title--SfH3sA8')
            key = key_div.get_text(strip=True) if key_div else 'N/A'

            value_div = prop.find('div', class_='specification--desc--Dxx6W0W')
            value = value_div.get_text(strip=True) if value_div else 'N/A'

            spec[key] = value
            
    return title, spec

