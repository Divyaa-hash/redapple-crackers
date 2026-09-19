from django.core.management.base import BaseCommand
from django.core.management import call_command
from products.models import Product, Category


class Command(BaseCommand):
    help = 'Sync database from fixtures - clears existing data and loads fresh data'

    def handle(self, *args, **options):
        self.stdout.write('Starting database sync from fixtures...')
        
        # Clear existing data
        self.stdout.write('Clearing existing products...')
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared all products'))
        
        self.stdout.write('Clearing existing categories...')
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared all categories'))
        
        # Load fixtures
        self.stdout.write('Loading categories from fixture...')
        call_command('loaddata', 'categories_fixture.json')
        self.stdout.write(self.style.SUCCESS('Loaded categories'))
        
        self.stdout.write('Loading products from fixture...')
        call_command('loaddata', 'products_fixture.json')
        self.stdout.write(self.style.SUCCESS('Loaded products'))
        
        # Report counts
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'\nDatabase sync complete!'))
        self.stdout.write(f'Products: {product_count}')
        self.stdout.write(f'Categories: {category_count}')
