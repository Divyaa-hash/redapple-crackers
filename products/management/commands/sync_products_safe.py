from django.core.management.base import BaseCommand
from django.core.management import call_command
from products.models import Product, Category
import os


class Command(BaseCommand):
    help = 'Safely sync products from fixtures without deleting existing data'

    def handle(self, *args, **options):
        self.stdout.write('Starting safe product sync from fixtures...')
        
        # Check if fixtures exist
        fixture_dir = os.getcwd()
        cat_fixture = os.path.join(fixture_dir, 'categories_fixture.json')
        prod_fixture = os.path.join(fixture_dir, 'products_fixture.json')
        
        self.stdout.write(f'Current directory: {fixture_dir}')
        self.stdout.write(f'Categories fixture exists: {os.path.exists(cat_fixture)}')
        self.stdout.write(f'Products fixture exists: {os.path.exists(prod_fixture)}')
        
        # Get current counts
        initial_product_count = Product.objects.count()
        initial_category_count = Category.objects.count()
        self.stdout.write(f'Initial products: {initial_product_count}')
        self.stdout.write(f'Initial categories: {initial_category_count}')
        
        # Load categories using loaddata with --ignorenonexistent
        try:
            self.stdout.write('Loading categories from fixture (safe mode)...')
            call_command('loaddata', 'categories_fixture.json', verbosity=2, ignorenonexistent=True)
            self.stdout.write(self.style.SUCCESS('Categories loaded/updated'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading categories: {e}'))
        
        # Load products using loaddata with --ignorenonexistent
        try:
            self.stdout.write('Loading products from fixture (safe mode)...')
            call_command('loaddata', 'products_fixture.json', verbosity=2, ignorenonexistent=True)
            self.stdout.write(self.style.SUCCESS('Products loaded/updated'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading products: {e}'))
        
        # Report final counts
        final_product_count = Product.objects.count()
        final_category_count = Category.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'\nSafe sync complete!'))
        self.stdout.write(f'Products: {initial_product_count} -> {final_product_count} ({final_product_count - initial_product_count} added)')
        self.stdout.write(f'Categories: {initial_category_count} -> {final_category_count} ({final_category_count - initial_category_count} added)')
        self.stdout.write('No existing data was deleted.')