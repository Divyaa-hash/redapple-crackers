import json
import os
from django.core.management.base import BaseCommand
from django.core.serializers import deserialize
from products.models import Product, Category


class Command(BaseCommand):
    help = 'Seed products and categories from JSON fixtures for production'

    def handle(self, *args, **options):
        # Load categories
        categories_file = 'categories_fixture.json'
        if os.path.exists(categories_file):
            with open(categories_file, 'r', encoding='utf-8') as f:
                categories_data = f.read()
            
            # Clear existing categories
            Category.objects.all().delete()
            
            # Load categories
            for obj in deserialize('json', categories_data):
                obj.save()
            
            self.stdout.write(f"Loaded {Category.objects.count()} categories")
        else:
            self.stdout.write(f"Categories file not found: {categories_file}")

        # Load products
        products_file = 'products_fixture.json'
        if os.path.exists(products_file):
            with open(products_file, 'r', encoding='utf-8') as f:
                products_data = f.read()
            
            # Clear existing products
            Product.objects.all().delete()
            
            # Load products
            for obj in deserialize('json', products_data):
                obj.save()
            
            self.stdout.write(f"Loaded {Product.objects.count()} products")
        else:
            self.stdout.write(f"Products file not found: {products_file}")

        self.stdout.write("\nProduct seeding completed successfully!")
