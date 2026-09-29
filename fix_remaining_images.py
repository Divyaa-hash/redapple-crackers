import sqlite3

conn = sqlite3.connect('C:/Users/Divya/OneDrive/Desktop/crackers/db.sqlite3')
cursor = conn.cursor()

# Update remaining products with placeholder images to use empty string
# This will make them fall back to slug-based images
updates = [
    (59, 'Binge Pop'),
    (62, 'Kickerzzz'),
    (75, 'Mini Peacock'),
    (81, 'Little Dove'),
    (84, 'Kickerzzz'),
    (103, 'Sword'),
    (104, 'Smiley Mushroom'),
    (107, 'Jolly Bobby Asok Brand'),
    (119, 'Avatar 2'),
    (125, '1H Wala'),
    (126, '1k Wala'),
    (127, '2k Wala'),
    (128, '5k Wala'),
    (129, '10k Wala'),
    (130, '1k Wala Spl'),
    (131, '2k Wala Spl'),
    (132, '5k Wala Spl'),
    (133, '10k Wala Spl'),
    (135, 'Colour Rocket'),
]

for product_id, name in updates:
    cursor.execute('UPDATE products_product SET image_url = NULL WHERE id = ?', (product_id,))
    print(f'Updated {name} (ID {product_id}) to use slug-based fallback')

conn.commit()
print(f'Updated {len(updates)} products to use placeholder instead of logo')

conn.close()
