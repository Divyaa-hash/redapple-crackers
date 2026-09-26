import os
from django.core.management.base import BaseCommand
from django.core.serializers import deserialize
from products.models import Product, Category


class Command(BaseCommand):
    help = 'Force reload products from fixture (overwrites existing)'

    def handle(self, *args, **options):
        # Get base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Load categories
        categories_file = os.path.join(base_dir, '..', '..', 'categories_fixture.json')
        if os.path.exists(categories_file):
            try:
                with open(categories_file, 'r', encoding='utf-8') as f:
                    categories_data = f.read()
                
                Category.objects.all().delete()
                for obj in deserialize('json', categories_data):
                    obj.save()
                
                self.stdout.write(self.style.SUCCESS(f'Loaded {Category.objects.count()} categories'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error loading categories: {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'Categories file not found: {categories_file}'))

        # Load products
        products_file = os.path.join(base_dir, '..', '..', 'products_fixture.json')
        if os.path.exists(products_file):
            try:
                with open(products_file, 'r', encoding='utf-8') as f:
                    products_data = f.read()
                
                Product.objects.all().delete()
                for obj in deserialize('json', products_data):
                    obj.save()
                
                self.stdout.write(self.style.SUCCESS(f'Loaded {Product.objects.count()} products'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error loading products: {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'Products file not found: {products_file}'))

        self.stdout.write(self.style.SUCCESS('Product reload completed successfully!'))
