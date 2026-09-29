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

# Manual mapping for specific products
manual_mapping = {
    'Flower Pot Big (10 Pcs)': 'Flower Pot Big (10 Pcs).webp',
    'Flower Pot Special (10 Pcs)': 'Flower Pot Special (10 Pcs).webp',
    'Flower Pot Asoka (10 Pcs)': 'Flower Pot Asoka (10 Pcs).webp',
    'Flower Pot Super Deluxe (2 Pcs)': 'Flower Pot Super Deluxe (2 Pcs).webp',
    'Purple Cone': 'Rio Wheel ( 5 Pcs) (Orange and Purple).webp',
    '28 Giant': '28 Giant.jpg',
    '56 Giant': '56 Giant.jpg',
    '24 Deluxe': '24 Deluxe.jpg',
    '50 Deluxe': '50 Deluxe.jpg',
    '100 Deluxe': '100 Deluxe.jpg',
    'Flower Power': 'Flower Power.webp',
}

updates = []
for product in products:
    id, name, image_url = product
    
    # Check if it's a placeholder
    if image_url and any(placeholder in image_url for placeholder in ['celebration-collection-logo', 'flower-pot', 'gift_box_', 'placeholder']):
        
        # Check manual mapping first
        if name in manual_mapping:
            new_file = manual_mapping[name]
            new_path = f'images/crackers/{new_file}'
            if new_file in existing_files:
                updates.append((id, name, image_url, new_path))
                print(f'ID {id}: {name}')
                print(f'  Old: {image_url}')
                print(f'  New: {new_path}')
                print()
                continue
        
        # Try to find a matching file
        name_lower = name.lower()
        best_match = None
        best_score = 0
        
        for filename in existing_files:
            if not (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.webp') or filename.endswith('.png')):
                continue
            
            # Skip timestamped files
            if re.match(r'^\d{14}', filename):
                continue
            
            file_lower = filename.lower()
            
            # Calculate simple match score
            score = 0
            for word in name_lower.split():
                if word in file_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = filename
        
        if best_match and best_score >= 2:
            new_path = f'images/crackers/{best_match}'
            updates.append((id, name, image_url, new_path))
            print(f'ID {id}: {name}')
            print(f'  Old: {image_url}')
            print(f'  New: {new_path}')
            print()

print(f'\nTotal updates: {len(updates)}')

if updates:
    for id, name, old_path, new_path in updates:
        cursor.execute('UPDATE products_product SET image_url = ? WHERE id = ?', (new_path, id))
    conn.commit()
    print(f'Updated {len(updates)} products!')
else:
    print('No updates made.')

conn.close()
