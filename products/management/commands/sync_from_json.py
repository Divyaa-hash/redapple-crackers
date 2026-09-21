import json
from django.core.management.base import BaseCommand
from products.models import Product, Category, Festival

class Command(BaseCommand):
    help = 'Safely sync products and categories from JSON export (idempotent)'

    def handle(self, *args, **options):
        self.stdout.write('Syncing products and categories from JSON export...')
        
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
        
        # Sync categories (create or update by slug)
        categories_created = 0
        categories_updated = 0
        category_map = {}  # Map name to category object
        
        for cat_data in categories_data:
            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data.get('description', ''),
                    'is_active': cat_data.get('is_active', True),
                    'order': cat_data.get('order', 0),
                    'meta_title': cat_data.get('meta_title', ''),
                    'meta_description': cat_data.get('meta_description', ''),
                    'meta_keywords': cat_data.get('meta_keywords', ''),
                }
            )
            if created:
                categories_created += 1
                self.stdout.write(f'+ Created category: {cat_data["name"]}')
            else:
                # Update existing category
                category.name = cat_data['name']
                category.description = cat_data.get('description', '')
                category.is_active = cat_data.get('is_active', True)
                category.order = cat_data.get('order', 0)
                category.meta_title = cat_data.get('meta_title', '')
                category.meta_description = cat_data.get('meta_description', '')
                category.meta_keywords = cat_data.get('meta_keywords', '')
                category.save()
                categories_updated += 1
                self.stdout.write(f'~ Updated category: {cat_data["name"]}')
            
            category_map[cat_data['name']] = category
        
        # Sync products (create or update by SKU)
        products_created = 0
        products_updated = 0
        products_skipped = 0
        
        for prod_data in products_data:
            # Get category
            category = category_map.get(prod_data.get('category_name'))
            if not category:
                self.stdout.write(self.style.WARNING(f'! Skipped product (category not found): {prod_data["name"]}'))
                products_skipped += 1
                continue
            
            # Get festival if exists
            festival = None
            festival_name = prod_data.get('festival_name')
            if festival_name:
                try:
                    festival = Festival.objects.get(name=festival_name)
                except Festival.DoesNotExist:
                    pass  # Festival doesn't exist, skip it
            
            # Create or update product by SKU
            try:
                product = Product.objects.get(sku=prod_data['sku'])
                # Update existing product
                product.name = prod_data['name']
                product.slug = prod_data['slug']
                product.category = category
                product.product_type = prod_data.get('product_type', 'single')
                product.safety_level = prod_data.get('safety_level', 'medium')
                product.short_description = prod_data['short_description']
                product.description = prod_data['description']
                product.safety_instructions = prod_data.get('safety_instructions', '')
                product.regular_price = prod_data['regular_price']
                product.sale_price = prod_data.get('sale_price')
                product.wholesale_price = prod_data.get('wholesale_price')
                product.stock = prod_data['stock']
                product.low_stock_threshold = prod_data['low_stock_threshold']
                product.image_url = prod_data.get('image_url')
                product.additional_images = prod_data.get('additional_images', [])
                product.video_url = prod_data.get('video_url')
                product.weight = prod_data.get('weight')
                product.dimensions = prod_data.get('dimensions')
                product.pieces = prod_data['pieces', 1)
                product.duration = prod_data.get('duration')
                product.sound_level = prod_data.get('sound_level')
                product.height = prod_data.get('height')
                product.is_featured = prod_data.get('is_featured', False)
                product.is_new = prod_data.get('is_new', False)
                product.is_bestseller = prod_data.get('is_bestseller', False)
                product.is_digital = prod_data.get('is_digital', False)
                product.is_trending = prod_data.get('is_trending', False)
                product.is_limited_edition = prod_data.get('is_limited_edition', False)
                product.has_free_shipping = prod_data.get('has_free_shipping', False)
                product.has_gift_wrap = prod_data.get('has_gift_wrap', False)
                product.reward_points = prod_data.get('reward_points', 0)
                product.festival = festival
                product.meta_title = prod_data.get('meta_title', '')
                product.meta_description = prod_data.get('meta_description', '')
                product.meta_keywords = prod_data.get('meta_keywords', '')
                product.is_active = prod_data.get('is_active', True)
                product.order = prod_data.get('order', 0)
                product.save()
                products_updated += 1
                self.stdout.write(f'~ Updated product: {prod_data["name"]}')
            except Product.DoesNotExist:
                # Create new product
                product = Product.objects.create(
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
                    pieces=prod_data['pieces', 1),
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
                products_created += 1
                self.stdout.write(f'+ Created product: {prod_data["name"]}')
        
        # Count after
        products_after = Product.objects.count()
        categories_after = Category.objects.count()
        
        self.stdout.write(self.style.SUCCESS('Sync completed successfully'))
        self.stdout.write(f'Categories: {categories_created} created, {categories_updated} updated')
        self.stdout.write(f'Products: {products_created} created, {products_updated} updated, {products_skipped} skipped')
        self.stdout.write(f'After: {products_after} products, {categories_after} categories')
