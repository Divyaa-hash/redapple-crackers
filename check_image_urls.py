import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

print('Checking first 10 product image URLs:')
for p in Product.objects.all()[:10]:
    print(f'\nProduct: {p.name}')
    print(f'  Image field type: {type(p.main_image)}')
    print(f'  Image value: {p.main_image}')
    print(f'  Image value (str): {str(p.main_image)}')
    print(f'  Is URL: {str(p.main_image).startswith("http") if p.main_image else "None"}')

print('\n\n=== Checking products that should have images ===')
with_images = Product.objects.filter(main_image__isnull=False).exclude(main_image='')
print(f'Products with images: {with_images.count()}')
for p in with_images[:5]:
    print(f'  - {p.name}: {str(p.main_image)[:60]}...')
