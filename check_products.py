import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category, Brand

print(f'Total products in database: {Product.objects.count()}')
print(f'Active products: {Product.objects.filter(is_active=True).count()}')

print(f'\nGift box products in database:')
gift_boxes = Product.objects.filter(category__name__icontains='GIFT BOX', is_active=True)
print(f'  Total gift boxes: {gift_boxes.count()}')
for p in gift_boxes:
    print(f'  - {p.name} (sku={p.sku}, image={p.main_image})')

print(f'\nFamily pack products in database:')
family_packs = Product.objects.filter(category__name__icontains='FAMILY PACK', is_active=True)
print(f'  Total family packs: {family_packs.count()}')
for p in family_packs:
    print(f'  - {p.name} (sku={p.sku}, image={p.main_image})')

