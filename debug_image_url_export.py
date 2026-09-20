import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product
from django.core.serializers import serialize

# Check database
print("=== Database Check ===")
total = Product.objects.count()
with_url = Product.objects.exclude(image_url='').exclude(image_url__isnull=True).count()
print(f'Total products: {total}')
print(f'With image_url in DB: {with_url}')

# Get a sample product without image_url in fixture
sample_name = '4.5\' Wow Series Fancy Pipe Out'
sample = Product.objects.filter(name=sample_name).first()
if sample:
    print(f'\nSample product: {sample.name}')
    print(f'image_url value: {repr(sample.image_url)}')
    print(f'image_url type: {type(sample.image_url)}')
