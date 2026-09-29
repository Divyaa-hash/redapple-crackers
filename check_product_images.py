import sqlite3
import os

conn = sqlite3.connect('C:/Users/Divya/OneDrive/Desktop/crackers/db.sqlite3')
cursor = conn.cursor()

# Get all products
cursor.execute('SELECT id, name, image_url FROM products_product')
products = cursor.fetchall()

static_dir = 'C:/Users/Divya/OneDrive/Desktop/crackers/static/images/crackers'
existing_files = os.listdir(static_dir)

# Find products with placeholder or missing images
placeholder_images = [
    'celebration-collection-logo.jpg',
    'flower-pot.jpg',
    'gift_box_1.jpg',
    'gift_box_2.jpg',
    'gift_box_3.jpg',
    'gift_box_4.jpg',
    'placeholder.jpg',
]

products_need_fix = []
for product in products:
    id, name, image_url = product
    if image_url:
        filename = image_url.split('/')[-1]
        # Check if it's a placeholder or doesn't exist
        if filename in placeholder_images or filename not in existing_files:
            products_need_fix.append((id, name, image_url, filename))

print(f'Products that need image fixes: {len(products_need_fix)}')
print('\nThese products have placeholder or missing images:')
print('=' * 80)
for i, (id, name, image_url, filename) in enumerate(products_need_fix[:50]):
    print(f'{i+1}. ID {id}: {name}')
    print(f'   Current: {image_url}')
    print()

if len(products_need_fix) > 50:
    print(f'... and {len(products_need_fix) - 50} more')

print('\nTo fix these images:')
print('1. Go to Django Admin: http://127.0.0.1:8000/admin/')
print('2. Navigate to Products')
print('3. For each product, upload the correct image or set the image_url')
print('4. Save each product')

conn.close()
