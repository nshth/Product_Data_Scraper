# open a browser session using Playwright
# wait
# scrape with beautifulsoup

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from csv_parser import parse_csv

def get_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        # page.wait_for_selector() 
        content = page.content()
        browser.close()
        return content
    
def parse_with_beautifulsoup(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    div = soup.find(class_='title--wrap--UUHae_g')
    title = div.get_text()
    
    return title

if __name__ == "__main__":
    products = parse_csv()  
    
    for product in products:
        target_url = product['product_link']
        variants = product['variants']
        total_qty = product['total_quantity']
                
        html_content = get_page_content(target_url)
        if html_content:
            print(f"Successfully fetched HTML content")
            soup_object = parse_with_beautifulsoup(html_content)
            print(soup_object)
        else:
            print(f"Failed to fetch HTML content")