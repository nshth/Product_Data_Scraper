# generate csv to import bulk product

import csv
import os
from datetime import datetime

def csv_gen(parent_data, variations_data, filename='product-data'):

    if not parent_data and variations_data:
        print("product_data not exist")
        return
        
    export_folder = "data/output/csv"
    os.makedirs(export_folder, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"Data saved to {filename}")

def generate_csv(data, filename):
    if not data:
        print(f"No data to write to {filename}")
        return
    
    fieldnames = set()
    for product in data:
        fieldnames.update(product.keys())

    priority_fields = ['ID', 'product_name', 'description', 'category', 'variant_name', 'variant_sku', 
                      'stock', 'attributes', 'image_urls']
    
    ordered_fields = [f for f in priority_fields if f in fieldnames]

    remaining_fields = sorted(fieldnames - set(ordered_fields))
    ordered_fields.extend(remaining_fields)
    
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=ordered_fields)
            writer.writeheader()
            
            for product in data:
                row = {field: product.get(field, '') for field in ordered_fields}
                writer.writerow(row)
        
        print(f"CSV saved: {filename}")
        
    except Exception as e:
        print(f"Error saving {filename}: {e}")
