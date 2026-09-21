from django.core.management.base import BaseCommand
from products.models import Product, Category, Brand
import json
import os


class Command(BaseCommand):
    help = 'Direct seed products from JSON without using loaddata'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('Direct seeding products from JSON...')
        self.stdout.write('=' * 60)
        
        fixture_file = os.path.join(os.getcwd(), 'products_fixture.json')
        cat_fixture_file = os.path.join(os.getcwd(), 'categories_fixture.json')
        
        self.stdout.write(f'Products fixture: {os.path.exists(fixture_file)}')
        self.stdout.write(f'Categories fixture: {os.path.exists(cat_fixture_file)}')
        
        # Load categories first
        try:
            with open(cat_fixture_file, 'r', encoding='utf-8') as f:
                categories_data = json.load(f)
            
            self.stdout.write(f'Loading {len(categories_data)} categories...')
            for cat_data in categories_data:
                if cat_data['model'] == 'products.category':
                    fields = cat_data['fields']
                    Category.objects.update_or_create(
                        pk=cat_data['pk'],
                        defaults=fields
                    )
            
            self.stdout.write(self.style.SUCCESS(f'Loaded {Category.objects.count()} categories'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading categories: {e}'))
        
        # Load products
        try:
            with open(fixture_file, 'r', encoding='utf-8') as f:
                products_data = json.load(f)
            
            self.stdout.write(f'Loading {len(products_data)} products...')
            
            # Create or get default brand
            brand, _ = Brand.objects.get_or_create(
                name='RedApple',
                defaults={'slug': 'redapple', 'is_featured': True}
            )
            
            loaded_count = 0
            for prod_data in products_data:
                if prod_data['model'] == 'products.product':
                    fields = prod_data['fields']
                    
                    # Handle category foreign key
                    category_id = fields.get('category')
                    if category_id:
                        try:
                            category = Category.objects.get(pk=category_id)
                            fields['category'] = category
                        except Category.DoesNotExist:
                            self.stdout.write(f'Category {category_id} not found, skipping product')
                            continue
                    
                    # Handle brand foreign key
                    brand_id = fields.get('brand')
                    if brand_id:
                        try:
                            brand = Brand.objects.get(pk=brand_id)
                            fields['brand'] = brand
                        except Brand.DoesNotExist:
                            fields['brand'] = None
                    
                    # Handle festival foreign key
                    festival_id = fields.get('festival')
                    if festival_id:
                        fields['festival'] = None  # Skip festival for now
                    
                    # Create or update product
                    Product.objects.update_or_create(
                        pk=prod_data['pk'],
                        defaults=fields
                    )
                    loaded_count += 1
            
            self.stdout.write(self.style.SUCCESS(f'Loaded {loaded_count} products'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading products: {e}'))
            import traceback
            traceback.print_exc()
        
        # Final counts
        final_products = Product.objects.count()
        final_categories = Category.objects.count()
        
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('Direct seeding complete!'))
        self.stdout.write(f'Total products: {final_products}')
        self.stdout.write(f'Total categories: {final_categories}')
        self.stdout.write('=' * 60)