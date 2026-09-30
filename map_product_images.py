import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Product to image mapping based on your provided list
# Updated with actual database names and exact filenames
product_image_mapping = {
    "Peacock Dance 30 Shots": "Peacock Dance - 30 Shots.webp",
    "Sony Pixel Shot 5*4": "Sony Pixel Shot 54",
    "6\" Fancy": "6' Fancy.webp",
    "5\" Fancy": "5' Fancy.webp",
    "Zoom Pink (2 Pcs)": "Zoom Pink (2 Pcs).webp",
    "Orange Fancy (2 Pcs)": "Orange Fancy (2 Pcs).webp",
    "Flower Power": "Flower Power.webp",
    "Kurkur (Red, Green, Silver, Gold, R&G)": "Kurkur( Red,Green,Silver,Gold,RandG).webp",
    "Layz (Red, Green, Silver, Gold, R&G)": "Layz ( Red,Green,Silver,Gold,RandG).webp",
    "Flower Pot Super Deluxe (2 Pcs)": "Flower Pot Super Deluxe (2 Pcs).webp",
    "Flower Pot Deluxe (5 Pcs)": "Flower Pot Deluxe (5 Pcs).webp",
    "Flower Pot Asoka (10 Pcs)": "Flower Pot Asoka (10 Pcs).webp",
    "Flower Pot Special (10 Pcs)": "Flower Pot Special (10 Pcs).webp",
    "Flower Pot Big (10 Pcs)": "Flower Pot Big (10 Pcs).webp",
    "Univercell 30 Shots (2\" Comet)": "Univercell 30 Shots (2' Comet).webp",
    "New 10*10 Light Celebration": "New 10'10 Light Celebration.webp",
    "Pala Sola Kii 3*10": "Pala Sola Kii 3'10",
    "Bharat Ratna 20 Shots (2.5\" Comet)": "Bharat Ratna 20 Shots (2.5' Comet).webp",
}

print('Mapping product images...')
print('=' * 80)

updated_count = 0
not_found_count = 0

for product_name, image_filename in product_image_mapping.items():
    try:
        # Try to find product by exact name match
        product = Product.objects.get(name=product_name)
        product.image_url = f'images/crackers/{image_filename}'
        product.save()
        print(f'[OK] Updated: {product.name} -> {image_filename}')
        updated_count += 1
    except Product.DoesNotExist:
        print(f'[X] Not found: {product_name}')
        not_found_count += 1

print('=' * 80)
print(f'Successfully updated {updated_count} products')
print(f'Not found: {not_found_count} products')
