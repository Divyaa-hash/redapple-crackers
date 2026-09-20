import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Get all products without image_url
products_without_image = Product.objects.filter(image_url__isnull=True) | Product.objects.filter(image_url='')

print(f'Products without image_url: {products_without_image.count()}')

# List static images
static_dir = 'static/images/crackers'
if os.path.exists(static_dir):
    static_images = set(os.listdir(static_dir))
    print(f'Static images available: {len(static_images)}')
else:
    static_images = set()
    print('Static directory not found')

# Try to match products to static images
updated = 0
for product in products_without_image:
    # Try exact match
    product_name = f"{product.name}.webp"
    if product_name in static_images:
        product.image_url = f'images/crackers/{product_name}'
        product.save()
        updated += 1
        print(f'Matched: {product.name}')
        continue
    
    # Try partial match
    for img in static_images:
        if product.name.lower() in img.lower() or img.lower().replace('.webp', '') in product.name.lower():
            product.image_url = f'images/crackers/{img}'
            product.save()
            updated += 1
            print(f'Partial match: {product.name} -> {img}')
            break

print(f'\nUpdated {updated} products with image_url')
print(f'Remaining without image_url: {Product.objects.filter(image_url__isnull=True).count() + Product.objects.filter(image_url='').count()}')
