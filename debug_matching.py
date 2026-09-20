import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Get products without image_url
products_without = Product.objects.filter(image_url__isnull=True) | Product.objects.filter(image_url='')

print(f'Products without image_url: {products_without.count()}')

# List static images
static_dir = 'static/images/crackers'
static_images = os.listdir(static_dir) if os.path.exists(static_dir) else []

print(f'\nFirst 5 products without images:')
for p in products_without[:5]:
    print(f'\nProduct: {p.name}')
    # Try to find similar images
    similar = [img for img in static_images if p.name.lower() in img.lower() or img.lower().replace('.webp', '') in p.name.lower()]
    if similar:
        print(f'  Similar images found: {similar[:3]}')
    else:
        print(f'  No similar images found')
