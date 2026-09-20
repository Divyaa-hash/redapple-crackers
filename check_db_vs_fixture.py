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

# Serialize and check
print("\n=== Serialization Check ===")
products_data = serialize('json', Product.objects.all())
products_json = json.loads(products_data)

print(f'Total serialized: {len(products_json)}')
with_url_serialized = sum(1 for p in products_json if p['fields'].get('image_url'))
print(f'With image_url in serialized: {with_url_serialized}')

# Check a specific product
sample = Product.objects.filter(name='4.5\' Wow Series Fancy Pipe Out').first()
if sample:
    print(f"\n=== Sample Product: {sample.name} ===")
    print(f'DB image_url: {repr(sample.image_url)}')
    
    # Find it in serialized data
    for p in products_json:
        if p['fields']['name'] == sample.name:
            print(f'Serialized image_url: {repr(p["fields"].get("image_url"))}')
            break
