import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

missing = [p for p in Product.objects.all() if not p.image_url and not p.main_image]
print('Products without images:')
print('=' * 80)
for p in missing:
    print(f'ID: {p.id}, Name: {p.name}, Slug: {p.slug}')
print(f'\nTotal: {len(missing)}')
