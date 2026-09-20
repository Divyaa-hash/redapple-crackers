from django.core.management.base import BaseCommand
from django.core.management import call_command
from products.models import Product, Category
import os


class Command(BaseCommand):
    help = 'Sync database from fixtures - clears existing data and loads fresh data'

    def handle(self, *args, **options):
        self.stdout.write('Starting database sync from fixtures...')
        
        # Check if fixtures exist
        fixture_dir = os.getcwd()
        cat_fixture = os.path.join(fixture_dir, 'categories_fixture.json')
        prod_fixture = os.path.join(fixture_dir, 'products_fixture.json')
        
        self.stdout.write(f'Current directory: {fixture_dir}')
        self.stdout.write(f'Categories fixture exists: {os.path.exists(cat_fixture)}')
        self.stdout.write(f'Products fixture exists: {os.path.exists(prod_fixture)}')
        
        # Clear existing data
        self.stdout.write('Clearing existing products...')
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared all products'))
        
        self.stdout.write('Clearing existing categories...')
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared all categories'))
        
        # Load fixtures
        try:
            self.stdout.write('Loading categories from fixture...')
            call_command('loaddata', 'categories_fixture.json', verbosity=2)
            self.stdout.write(self.style.SUCCESS('Loaded categories'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading categories: {e}'))
        
        try:
            self.stdout.write('Loading products from fixture...')
            call_command('loaddata', 'products_fixture.json', verbosity=2)
            self.stdout.write(self.style.SUCCESS('Loaded products'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading products: {e}'))
        
        # Report counts
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'\nDatabase sync complete!'))
        self.stdout.write(f'Products: {product_count}')
        self.stdout.write(f'Categories: {category_count}')
