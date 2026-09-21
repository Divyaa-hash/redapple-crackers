import json
from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Product, Category, Festival

class Command(BaseCommand):
    help = 'Clear all products and categories, then reload from JSON export (DESTRUCTIVE)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('WARNING: This will DELETE ALL products and categories from the database!'))
        self.stdout.write('This is a destructive operation.')
        
        # Load JSON file
        try:
            with open('products_export.json', 'r', encoding='utf-8') as f:
                export_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('ERROR: products_export.json not found. Run export_products_json first.'))
            return
        
        categories_data = export_data.get('categories', [])
        products_data = export_data.get('products', [])
        
        # Count before
        products_before = Product.objects.count()
        categories_before = Category.objects.count()
        self.stdout.write(f'Before: {products_before} products, {categories_before} categories')
        
        # Use transaction to ensure atomic operation
        with transaction.atomic():
            # Delete all products
            self.stdout.write('Deleting all products...')
            Product.objects.all().delete()
            
            # Delete all categories
            self.stdout.write('Deleting all categories...')
            Category.objects.all().delete()
            
            self.stdout.write(self.style.SUCCESS('Cleared all products and categories'))
            
            # Create categories
            self.stdout.write('Creating categories...')
            category_map = {}
            for cat_data in categories_data:
                category = Category.objects.create(
                    name=cat_data['name'],
                    slug=cat_data['slug'],
                    description=cat_data.get('description', ''),
                    is_active=cat_data.get('is_active', True),
                    order=cat_data.get('order', 0),
                    meta_title=cat_data.get('meta_title', ''),
                    meta_description=cat_data.get('meta_description', ''),
                    meta_keywords=cat_data.get('meta_keywords', ''),
                )
                category_map[cat_data['name']] = category
                self.stdout.write(f'+ Created category: {cat_data["name"]}')
            
            # Create products
            self.stdout.write('Creating products...')
            for prod_data in products_data:
                # Get category
                category = category_map.get(prod_data.get('category_name'))
                if not category:
                    self.stdout.write(self.style.WARNING(f'! Skipped product (category not found): {prod_data["name"]}'))
                    continue
                
                # Get festival if exists
                festival = None
                festival_name = prod_data.get('festival_name')
                if festival_name:
                    try:
                        festival = Festival.objects.get(name=festival_name)
                    except Festival.DoesNotExist:
                        pass  # Festival doesn't exist, skip it
                
                # Create product
                Product.objects.create(
                    name=prod_data['name'],
                    slug=prod_data['slug'],
                    sku=prod_data['sku'],
                    category=category,
                    product_type=prod_data.get('product_type', 'single'),
                    safety_level=prod_data.get('safety_level', 'medium'),
                    short_description=prod_data['short_description'],
                    description=prod_data['description'],
                    safety_instructions=prod_data.get('safety_instructions', ''),
                    regular_price=prod_data['regular_price'],
                    sale_price=prod_data.get('sale_price'),
                    wholesale_price=prod_data.get('wholesale_price'),
                    stock=prod_data['stock'],
                    low_stock_threshold=prod_data['low_stock_threshold'],
                    image_url=prod_data.get('image_url'),
                    additional_images=prod_data.get('additional_images', []),
                    video_url=prod_data.get('video_url'),
                    weight=prod_data.get('weight'),
                    dimensions=prod_data.get('dimensions'),
                    pieces=prod_data.get('pieces', 1),
                    duration=prod_data.get('duration'),
                    sound_level=prod_data.get('sound_level'),
                    height=prod_data.get('height'),
                    is_featured=prod_data.get('is_featured', False),
                    is_new=prod_data.get('is_new', False),
                    is_bestseller=prod_data.get('is_bestseller', False),
                    is_digital=prod_data.get('is_digital', False),
                    is_trending=prod_data.get('is_trending', False),
                    is_limited_edition=prod_data.get('is_limited_edition', False),
                    has_free_shipping=prod_data.get('has_free_shipping', False),
                    has_gift_wrap=prod_data.get('has_gift_wrap', False),
                    reward_points=prod_data.get('reward_points', 0),
                    festival=festival,
                    meta_title=prod_data.get('meta_title', ''),
                    meta_description=prod_data.get('meta_description', ''),
                    meta_keywords=prod_data.get('meta_keywords', ''),
                    is_active=prod_data.get('is_active', True),
                    order=prod_data.get('order', 0),
                )
                self.stdout.write(f'+ Created product: {prod_data["name"]}')
        
        # Count after
        products_after = Product.objects.count()
        categories_after = Category.objects.count()
        
        self.stdout.write(self.style.SUCCESS('Reload completed successfully'))
        self.stdout.write(f'Products removed: {products_before}')
        self.stdout.write(f'Categories removed: {categories_before}')
        self.stdout.write(f'Products created: {products_after}')
        self.stdout.write(f'Categories created: {categories_after}')
        self.stdout.write(f'After: {products_after} products, {categories_after} categories')
