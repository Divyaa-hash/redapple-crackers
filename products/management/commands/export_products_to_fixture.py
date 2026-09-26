import json
import os
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from products.models import Product, Category


class Command(BaseCommand):
    help = 'Export products and categories to JSON fixture for production deployment'

    def handle(self, *args, **options):
        # Export categories
        categories_data = serialize('json', Category.objects.all())
        categories_file = 'categories_fixture.json'
        with open(categories_file, 'w', encoding='utf-8') as f:
            f.write(categories_data)
        self.stdout.write(f"Exported {Category.objects.count()} categories to {categories_file}")

        # Export products
        products_data = serialize('json', Product.objects.all())
        products_file = 'products_fixture.json'
        with open(products_file, 'w', encoding='utf-8') as f:
            f.write(products_data)
        self.stdout.write(f"Exported {Product.objects.count()} products to {products_file}")

        self.stdout.write("\nFixture files created successfully!")
        self.stdout.write("Upload these files to Render and run:")
        self.stdout.write("python manage.py loaddata categories_fixture.json")
        self.stdout.write("python manage.py loaddata products_fixture.json")
