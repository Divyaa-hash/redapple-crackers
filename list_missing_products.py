import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# List products without image_url
products_without = Product.objects.filter(image_url__isnull=True) | Product.objects.filter(image_url='')

print(f'Products without image_url: {products_without.count()}')
print('\nFirst 10 products without images:')
for p in products_without[:10]:
    print(f'  - {p.name}')
