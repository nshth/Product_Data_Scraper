# //Product Data scraper//
# csv_parser
# scraper
# image_downloader

    # each image has "src="https://ae01.alicdn.com/kf/S5b901365ae7742c4818b2d5f65f8a158i.png"" and "slate-data-type="image"" 
    # we have to select the image and scrape it using this bc no div is common
    # and download it to the folder create if not exists

# /
from src.csv_parser import parse_csv
from src.scraper import get_page_content, parse_with_beautifulsoup
from src.image_downloader import scrape_image, download_image
import os

def main():
    # csv_parser
    products = parse_csv()  
    for i,product in enumerate(products):
        index = i 
        target_product_url = product['product_link']
        variants = product['variants']
        total_qty = product['total_quantity']
        
        # scraper content 
        html_content = get_page_content(target_product_url)
        if html_content:
            print(f"Successfully fetched HTML content")
            soup_object = parse_with_beautifulsoup(html_content)
            print(soup_object)
        else:
            print(f"Failed to fetch HTML content")

        imgs = scrape_image(target_product_url, headless=True)

        folder_path = os.path.join("data", "output", "images")        
        for i, img in enumerate(imgs["image_urls"][:3]):
            print("Downloading", img)
            path = download_image(img, folder_path, name_prefix=f"product_img_{i+1}")
            if path:
                print("Saved to", path)

if __name__ == "__main__":
    main()
