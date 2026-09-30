import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Product IDs that need logo image
product_ids = [
    135,  # Colour Rocket
    133,  # 10k Wala Spl
    132,  # 5k Wala Spl
    131,  # 2k Wala Spl
    130,  # 1k Wala Spl
    129,  # 10k Wala
    128,  # 5k Wala
    127,  # 2k Wala
    126,  # 1k Wala
    125,  # 1H Wala
    119,  # Avatar 2
    107,  # Jolly Bobby Asok Brand
    104,  # Smiley Mushroom
    103,  # Sword
    84,   # Kickerzzz (variant 1)
    81,   # Little Dove
    75,   # Mini Peacock
    62,   # Kickerzzz (variant 2)
    59,   # Binge Pop
]

print('Updating products with logo image...')
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
