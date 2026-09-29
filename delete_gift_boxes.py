import sqlite3

conn = sqlite3.connect('C:/Users/Divya/OneDrive/Desktop/crackers/db.sqlite3')
cursor = conn.cursor()

# Delete Gift Box products (IDs 234, 235, 236, 237)
gift_box_ids = [234, 235, 236, 237]

for product_id in gift_box_ids:
    cursor.execute('DELETE FROM products_product WHERE id = ?', (product_id,))
    print(f'Deleted product ID {product_id}')

conn.commit()
print(f'Deleted {len(gift_box_ids)} Gift Box products')

conn.close()
