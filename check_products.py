import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category, Brand

print(f'Total products in database: {Product.objects.count()}')
print(f'Active products: {Product.objects.filter(is_active=True).count()}')

print('\n=== First 10 products in database ===')
for p in Product.objects.all()[:10]:
    print(f'  - {p.name} (Category: {p.category.name if p.category else "None"})')

print('\n=== All categories ===')
for c in Category.objects.all():
    print(f'  - {c.name} (Products: {c.products.count()})')

