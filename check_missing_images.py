import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

print(f'Total products: {Product.objects.count()}')
print(f'Products with image_url: {Product.objects.exclude(image_url="").count()}')
print(f'Products without image_url: {Product.objects.filter(image_url="").count()}')

print('\nProducts without image_url:')
for product in Product.objects.filter(image_url=""):
    print(f'  - {product.name} (Category: {product.category.name})')
