from django.core.management.base import BaseCommand
from django.core.management import call_command
from products.models import Product, Category, Brand
import os
import json


class Command(BaseCommand):
    help = 'Seed production database from fixtures with better error handling'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('Seeding production database from fixtures...')
        self.stdout.write('=' * 60)
        
        fixture_dir = os.getcwd()
        cat_fixture = os.path.join(fixture_dir, 'categories_fixture.json')
        prod_fixture = os.path.join(fixture_dir, 'products_fixture.json')
        
        self.stdout.write(f'Fixture directory: {fixture_dir}')
        self.stdout.write(f'Categories fixture: {os.path.exists(cat_fixture)}')
        self.stdout.write(f'Products fixture: {os.path.exists(prod_fixture)}')
        
        # Check if we already have data
        existing_products = Product.objects.count()
        existing_categories = Category.objects.count()
        
        self.stdout.write(f'Existing products: {existing_products}')
        self.stdout.write(f'Existing categories: {existing_categories}')
        
        # If we already have data, skip seeding
        if existing_products > 0:
            self.stdout.write(self.style.WARNING(f'Database already has {existing_products} products. Skipping seed.'))
            return
        
        # Use Django's loaddata command which handles foreign keys properly
        try:
            self.stdout.write('Loading categories from fixture...')
            call_command('loaddata', 'categories_fixture.json', verbosity=2)
            self.stdout.write(self.style.SUCCESS(f'Loaded {Category.objects.count()} categories'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading categories: {e}'))
        
        try:
            self.stdout.write('Loading products from fixture...')
            call_command('loaddata', 'products_fixture.json', verbosity=2)
            self.stdout.write(self.style.SUCCESS(f'Loaded {Product.objects.count()} products'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading products: {e}'))
        
        # Final counts
        final_products = Product.objects.count()
        final_categories = Category.objects.count()
        
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('Production seeding complete!'))
        self.stdout.write(f'Total products: {final_products}')
        self.stdout.write(f'Total categories: {final_categories}')
        self.stdout.write('=' * 60)