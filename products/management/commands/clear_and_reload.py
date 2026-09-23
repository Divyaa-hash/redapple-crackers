from django.core.management.base import BaseCommand
from products.models import Product, Category
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Clear all products and categories and reload Vasantham catalogue'

    def handle(self, *args, **options):
        self.stdout.write('=' * 50)
        self.stdout.write('VASANTHAM CRACKERS CLEAR AND RELOAD')
        self.stdout.write('=' * 50)
        self.stdout.write('WARNING: This will DELETE ALL products and categories from the database!')
        self.stdout.write('Applying 80% discount to all products')

        # Count before deletion
        products_before = Product.objects.count()
        categories_before = Category.objects.count()
        self.stdout.write(f'Before: {products_before} products, {categories_before} categories')
        
        # Use raw SQL to delete all related data bypassing Django ORM constraints
        with connection.cursor() as cursor:
            # Delete order items first
            try:
                cursor.execute("DELETE FROM orders_orderitem")
            except:
                pass
            # Delete orders
            try:
                cursor.execute("DELETE FROM orders_order")
            except:
                pass
            # Delete cart items
            try:
                cursor.execute("DELETE FROM cart_cartitem")
            except:
                pass
            # Delete carts
            try:
                cursor.execute("DELETE FROM cart_cart")
            except:
                pass
            # Delete wishlist items
            try:
                cursor.execute("DELETE FROM wishlist_wishlistitem")
            except:
                pass
            # Delete wishlists
            try:
                cursor.execute("DELETE FROM wishlist_wishlist")
            except:
                pass
            # Delete product reviews
            try:
                cursor.execute("DELETE FROM products_productreview")
            except:
                pass
            # Delete products
            cursor.execute("DELETE FROM products_product")
            # Delete categories
            cursor.execute("DELETE FROM products_category")
        
        self.stdout.write('✓ Deleted all products and categories')
        
        # Load Vasantham products from export file
        try:
            import json
            with open('products_export.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.stdout.write(f'✓ Loaded products_export.json')
            
            # Get static images and create mapping by slug
            static_path = 'static/images/crackers'
            image_mapping = {}
            if os.path.exists(static_path):
                for filename in os.listdir(static_path):
                    if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        # Remove extension to get base name
                        base_name = os.path.splitext(filename)[0]
                        # Use correct static URL format
                        image_mapping[base_name] = f'/static/images/crackers/{filename}'
                self.stdout.write(f'✓ Found {len(image_mapping)} static images')
                
                # Create a secondary mapping with normalized names for fuzzy matching
                normalized_mapping = {}
                for base_name, url in image_mapping.items():
                    normalized = base_name.lower().replace('-', ' ').replace('_', ' ').replace("'", "").replace("¼", "1-4").replace("½", "1-2").replace("¾", "3-4")
                    normalized_mapping[normalized] = url
                self.stdout.write(f'✓ Created {len(normalized_mapping)} normalized mappings')
            
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
            created_products = []
            matched_count = 0
            for prod_data in products_data:
                category = Category.objects.get(slug=prod_data['category_slug'])
                
                # Try to match image by slug
                product_slug = prod_data['slug']
                image_url = prod_data.get('image_url')
                
                if not image_url and image_mapping:
                    # Try exact match first
                    if product_slug in image_mapping:
                        image_url = image_mapping[product_slug]
                        matched_count += 1
                    else:
                        # Try fuzzy match - normalize both for comparison
                        slug_normalized = product_slug.lower().replace('-', ' ').replace('_', ' ').replace("'", "").replace("¼", "1-4").replace("½", "1-2").replace("¾", "3-4")
                        if slug_normalized in normalized_mapping:
                            image_url = normalized_mapping[slug_normalized]
                            matched_count += 1
                        else:
                            # Try partial match
                            for norm_name, url in normalized_mapping.items():
                                if slug_normalized in norm_name or norm_name in slug_normalized:
                                    image_url = url
                                    matched_count += 1
                                    break
                
                # Apply 80% discount to all products
                regular_price = float(prod_data['regular_price'])
                sale_price = regular_price * 0.2  # 20% of regular price = 80% discount

                create_kwargs = {
                    'name': prod_data['name'],
                    'slug': prod_data['slug'],
                    'sku': prod_data.get('sku', ''),
                    'category': category,
                    'regular_price': prod_data['regular_price'],
                    'sale_price': sale_price,
                    'stock': prod_data.get('stock', 0),
                    'low_stock_threshold': prod_data.get('low_stock_threshold', 5),
                    'short_description': prod_data.get('short_description', ''),
                    'description': prod_data.get('description', ''),
                    'safety_instructions': prod_data.get('safety_instructions', ''),
                    'is_active': prod_data.get('is_active', True),
                    'order': prod_data.get('order', 0)
                }
                
                # Always set image_url if found, otherwise use placeholder
                if image_url:
                    create_kwargs['image_url'] = image_url
                else:
                    # Use placeholder image for products without matching images
                    create_kwargs['image_url'] = 'https://via.placeholder.com/400x400/ef4444/ffffff?text=No+Image'
                
                product = Product.objects.create(**create_kwargs)
                created_products.append(product)
            
            # Count how many products got images
            products_with_images = Product.objects.filter(image_url__isnull=False).count()
            self.stdout.write(f'✓ Created {len(products_data)} products ({products_with_images} with images, {matched_count} matched)')
            if products_with_images < len(products_data):
                self.stdout.write(f'⚠ {len(products_data) - products_with_images} products without images')
                # List some products without images
                products_without = Product.objects.filter(image_url__isnull=True)[:10]
                for p in products_without:
                    self.stdout.write(f'  - {p.slug}: {p.name}')
            
            self.stdout.write('=' * 50)
            self.stdout.write(self.style.SUCCESS('VASANTHAM RELOAD COMPLETED SUCCESSFULLY'))
            self.stdout.write('=' * 50)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during reload: {e}'))
            raise
