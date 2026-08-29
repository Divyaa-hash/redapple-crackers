import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category, Brand

print(f'Total products: {Product.objects.count()}')
print(f'Active products: {Product.objects.filter(is_active=True).count()}')
print(f'Total categories: {Category.objects.count()}')
print(f'Active categories: {Category.objects.filter(is_active=True).count()}')
print(f'Total brands: {Brand.objects.count()}')
print(f'Active brands: {Brand.objects.filter(is_active=True).count()}')
print(f'First 5 brands:')
for b in Brand.objects.all()[:5]:
    print(f'  - {b.name} (active={b.is_active})')
print(f'First 5 products:')
for p in Product.objects.all()[:5]:
    print(f'  - {p.name} (active={p.is_active}, category={p.category.name}, brand={p.brand.name if p.brand else None}, price={p.regular_price})')

