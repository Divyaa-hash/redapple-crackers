"""
Export product data from local database to JSON fixtures.
This will create fixtures that can be loaded on Render to sync databases.
Includes Cloudinary URLs directly in the fixture data.
"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category
from django.core.serializers import serialize

# Load Cloudinary URL mapping
with open('cloudinary_url_mapping.json', 'r') as f:
    cloudinary_mapping = json.load(f)

# Export all categories
print("Exporting categories...")
categories_data = serialize('json', Category.objects.all())
with open('categories_fixture.json', 'w') as f:
    f.write(categories_data)
print(f"Exported {Category.objects.count()} categories to categories_fixture.json")

# Export all products with Cloudinary URLs
print("Exporting products...")
products_data = serialize('json', Product.objects.all())
products_json = json.loads(products_data)

# Update products with Cloudinary URLs from the mapping
updated_count = 0
for product in products_json:
    slug = product['fields']['slug']
    if slug in cloudinary_mapping:
        product['fields']['main_image'] = cloudinary_mapping[slug]
        updated_count += 1

with open('products_fixture.json', 'w') as f:
    json.dump(products_json, f)
print(f"Exported {len(products_json)} products to products_fixture.json")
print(f"Updated {updated_count} products with Cloudinary URLs")

print("\nExport complete!")
print("Files created:")
print("- products_fixture.json (with Cloudinary URLs)")
print("- categories_fixture.json")
