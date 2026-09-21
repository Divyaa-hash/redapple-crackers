from django.core.management.base import BaseCommand
from django.core.management import call_command
from products.models import Product, Category
import os


class Command(BaseCommand):
    help = 'Export current products and categories to fixtures for production sync'

    def handle(self, *args, **options):
        self.stdout.write('Exporting current products and categories to fixtures...')
        
        # Get current counts
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        self.stdout.write(f'Exporting {product_count} products and {category_count} categories')
        
        # Export categories
        try:
            self.stdout.write('Exporting categories...')
            call_command('dumpdata', 'products.Category', indent=2, output='categories_fixture.json')
            self.stdout.write(self.style.SUCCESS('Categories exported to categories_fixture.json'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error exporting categories: {e}'))
        
        # Export products
        try:
            self.stdout.write('Exporting products...')
            call_command('dumpdata', 'products.Product', indent=2, output='products_fixture.json')
            self.stdout.write(self.style.SUCCESS('Products exported to products_fixture.json'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error exporting products: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\nExport complete!'))
        self.stdout.write('Fixture files created:')
        self.stdout.write('- categories_fixture.json')
        self.stdout.write('- products_fixture.json')
        self.stdout.write('\nCommit these files and deploy to sync production database.')