from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = 'Clear all products and categories and reload Vasantham catalogue'

    def handle(self, *args, **options):
        self.stdout.write('=' * 50)
        self.stdout.write('VASANTHAM CRACKERS CLEAR AND RELOAD')
        self.stdout.write('=' * 50)
        self.stdout.write('WARNING: This will DELETE ALL products and categories from the database!')
        
        # Count before deletion
        products_before = Product.objects.count()
        categories_before = Category.objects.count()
        self.stdout.write(f'Before: {products_before} products, {categories_before} categories')
        
        # Delete all products
        Product.objects.all().delete()
        self.stdout.write('✓ Deleted all products')
        
        # Delete all categories
        Category.objects.all().delete()
        self.stdout.write('✓ Deleted all categories')
        
        # Load Vasantham products from export file
        try:
            import json
            with open('products_export.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.stdout.write(f'✓ Loaded products_export.json')
            
            # Create categories
            categories_data = data.get('categories', [])
            for cat_data in categories_data:
                Category.objects.create(
                    name=cat_data['name'],
                    slug=cat_data['slug'],
                    description=cat_data.get('description', ''),
                    is_active=True,
                    order=cat_data.get('order', 0)
                )
            self.stdout.write(f'✓ Created {len(categories_data)} categories')
            
            # Create products
            products_data = data.get('products', [])
            for prod_data in products_data:
                category = Category.objects.get(slug=prod_data['category'])
                Product.objects.create(
                    name=prod_data['name'],
                    slug=prod_data['slug'],
                    sku=prod_data.get('sku', ''),
                    category=category,
                    regular_price=prod_data['regular_price'],
                    sale_price=prod_data.get('sale_price'),
                    stock=prod_data.get('stock', 0),
                    low_stock_threshold=prod_data.get('low_stock_threshold', 5),
                    short_description=prod_data.get('short_description', ''),
                    description=prod_data.get('description', ''),
                    safety_instructions=prod_data.get('safety_instructions', ''),
                    is_active=prod_data.get('is_active', True),
                    order=prod_data.get('order', 0)
                )
            self.stdout.write(f'✓ Created {len(products_data)} products')
            
            self.stdout.write('=' * 50)
            self.stdout.write(self.style.SUCCESS('VASANTHAM RELOAD COMPLETED SUCCESSFULLY'))
            self.stdout.write('=' * 50)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during reload: {e}'))
            raise
