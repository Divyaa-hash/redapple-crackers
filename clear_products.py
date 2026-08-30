import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category, Brand

print('Clearing existing products...')
Product.objects.all().delete()
print(f'Products cleared. Remaining: {Product.objects.count()}')

print('Clearing existing categories...')
Category.objects.all().delete()
print(f'Categories cleared. Remaining: {Category.objects.count()}')

print('Clearing existing brands...')
Brand.objects.all().delete()
print(f'Brands cleared. Remaining: {Brand.objects.count()}')

print('Database cleared successfully!')
