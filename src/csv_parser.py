# load csv
# iterate each and get product link
# and get variant names and quantity and total quantity
# pass product link, variant names to scraper.py

import pandas as pd

product_list = []

def parse_csv():
    products = pd.read_csv('data/input/demo.csv', quotechar='"')
    product_list = []
    
    for _, product in products.iterrows():
        product_link = product['Product_link']

        v1 = product["Variant_1"]
        v1_quantity = product["V1_quantity"]

        v2 = product["Variant_2"]
        v2_quantity = product["V2_quantity"]

        v3 = product["Variant_3"]
        v3_quantity = product["V3_quantity"]

        total_quantity = product["total_quantity"]

        product_data = {
            'product_link': product_link,
            'variants': [
                {'name': v1, 'quantity': v1_quantity},
                {'name': v2, 'quantity': v2_quantity},
                {'name': v3, 'quantity': v3_quantity}
            ],
            'total_quantity': total_quantity
        }
        
        product_list.append(product_data)
    
    return product_list 
