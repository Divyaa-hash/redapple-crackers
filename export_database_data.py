"""
Export product data from local database to JSON fixtures.
This will create fixtures that can be loaded on Render to sync databases.
Includes image_url field with local static image paths.
"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category
from django.core.serializers import serialize

# Export all categories
print("Exporting categories...")
categories_data = serialize('json', Category.objects.all())
with open('categories_fixture.json', 'w') as f:
    f.write(categories_data)
print(f"Exported {Category.objects.count()} categories to categories_fixture.json")

# Export all products with image_url field
print("Exporting products...")
products_data = serialize('json', Product.objects.all())
products_json = json.loads(products_data)

# Count products with image_url
with_image_url = sum(1 for p in products_json if p['fields'].get('image_url'))
print(f"Exported {len(products_json)} products to products_fixture.json")
print(f"Products with image_url: {with_image_url}")

with open('products_fixture.json', 'w') as f:
    json.dump(products_json, f)

print("\nExport complete!")
print("Files created:")
print("- products_fixture.json (with image_url field)")
print("- categories_fixture.json")
