"""
Export product data from local database to JSON fixtures.
This will create fixtures that can be loaded on Render to sync databases.
"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category
from django.core.serializers import serialize

# Export all products
print("Exporting products...")
products_data = serialize('json', Product.objects.all())
with open('products_fixture.json', 'w') as f:
    f.write(products_data)
print(f"Exported {Product.objects.count()} products to products_fixture.json")

# Export all categories
print("Exporting categories...")
categories_data = serialize('json', Category.objects.all())
with open('categories_fixture.json', 'w') as f:
    f.write(categories_data)
print(f"Exported {Category.objects.count()} categories to categories_fixture.json")

print("\nExport complete!")
print("Files created:")
print("- products_fixture.json")
print("- categories_fixture.json")
print("\nTo load these on Render:")
print("1. Upload these files to Render (via git or manually)")
print("2. Run: python manage.py loaddata products_fixture.json")
print("3. Run: python manage.py loaddata categories_fixture.json")
