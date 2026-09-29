import sqlite3
import os
import re

conn = sqlite3.connect('C:/Users/Divya/OneDrive/Desktop/crackers/db.sqlite3')
cursor = conn.cursor()

# Get all products
cursor.execute('SELECT id, name, image_url FROM products_product')
products = cursor.fetchall()

static_dir = 'C:/Users/Divya/OneDrive/Desktop/crackers/static/images/crackers'
existing_files = os.listdir(static_dir)

def find_best_match(product_name, files):
    """Find the best matching image file for a product name"""
    # Normalize product name for matching
    product_lower = product_name.lower()
    product_words = re.findall(r'\w+', product_lower)
    
    best_match = None
    best_score = 0
    
    for filename in files:
        if not (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.webp') or filename.endswith('.png')):
            continue
        
        # Skip timestamped files (files with just numbers like 20250822084838)
        if re.match(r'^\d{14}', filename):
            continue
        
        file_lower = filename.lower()
        file_words = re.findall(r'\w+', file_lower)
        
        # Calculate match score
        score = 0
        for word in product_words:
            if word in file_lower:
                score += 1
        
        # Bonus for exact matches on key words
        if len(product_words) > 0 and product_words[0] in file_lower:
            score += 2
            
        # Bonus for longer matches (more matching words)
        if score > 0:
            score += min(len(product_words), len(file_words))
            
        if score > best_score:
            best_score = score
            best_match = filename
    
    return best_match if best_score >= 3 else None  # Require at least 3 points

# Update products with better image matches
updates = []
for product in products:
    id, name, image_url = product
    
    # Find best matching image
    best_match = find_best_match(name, existing_files)
    
    if best_match:
        new_path = f'images/crackers/{best_match}'
        if image_url != new_path:
            updates.append((id, name, image_url, new_path))
            print(f'ID {id}: {name}')
            print(f'  Old: {image_url}')
            print(f'  New: {new_path}')
            print()

print(f'\nTotal updates needed: {len(updates)}')

if updates:
    # Automatically update
    for id, name, old_path, new_path in updates:
        cursor.execute('UPDATE products_product SET image_url = ? WHERE id = ?', (new_path, id))
    conn.commit()
    print(f'Updated {len(updates)} products!')
else:
    print('No updates needed - all images are correctly matched.')

conn.close()
