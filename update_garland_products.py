import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Product IDs for the Garland crackers
product_ids = [
    120,  # 28 Giant
    121,  # 56 Giant
    122,  # 24 Deluxe
    123,  # 50 Deluxe
    124,  # 100 Deluxe
]

print('Updating Garland products with logo image...')
print('=' * 80)

updated_count = 0
for product_id in product_ids:
    try:
        product = Product.objects.get(id=product_id)
        product.image_url = 'images/crackers/logo.jpg'
        product.save()
        print(f'[OK] Updated: {product.name} (ID: {product.id})')
        updated_count += 1
    except Product.DoesNotExist:
        print(f'[X] Product not found: ID {product_id}')

print('=' * 80)
print(f'Successfully updated {updated_count} products with logo image')
