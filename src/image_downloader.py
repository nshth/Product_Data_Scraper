# downlod the image 
# aliexpress_scrape.py
import os
import re
import time
import requests
import io
from PIL import Image 
import pillow_avif
from playwright.sync_api import sync_playwright

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

def normalize_url(url): #to handle resolution issue
    if not url:
        return None
    match = re.search(r'(\.jpg|\.jpeg|\.png|\.webp)', url, re.IGNORECASE) # explain
    if match:
        url = url[:match.end()]
    
    return url.split('?')[0] 

def download_image(url, folder, name_prefix="img"):
    os.makedirs(folder, exist_ok=True)
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20, stream=True)
        resp.raise_for_status()
        image_data = io.BytesIO(resp.content)      
        img = Image.open(image_data)

        if img.mode == 'RGBA' or img.mode == 'LA':
            img = img.convert('RGB')  
        path = os.path.join(folder, f"{name_prefix}_{int(time.time()*1000)}.jpg")

        img.save(path, "JPEG", quality=95)

        return path
    
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def scrape_image(url, headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(user_agent=USER_AGENT, viewport={"width":1280,"height":800})
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        time.sleep(1.5)

        thumbs = page.query_selector_all(".slider--img--kD4mIg7 img")        
        img_urls = []
        for t in thumbs:
            src = t.get_attribute("src") 
            if src:
                img_urls.append(src)

        # # Some product pages embed JSON with images in a script tag. Try to grab any URLs from page HTML as fallback.
        # if not img_urls:
        #     print("no img urls")
        #     html = page.content()
        #     # simple regex to catch https...jpg/png links inside HTML/JS
        #     found = re.findall(r"https?:\/\/[^\s'\"\\<>]+?\.(?:jpg|jpeg|png|webp)", html)
        #     img_urls = list(dict.fromkeys(found))  # unique preserving order

        # explain
        img_urls = [normalize_url(u) for u in img_urls if u]
        img_urls = list(dict.fromkeys(img_urls)) # unique URLs
        img_urls = [u for u in img_urls if u and u.startswith("http")]
        browser.close()

    return {"image_urls": img_urls}


