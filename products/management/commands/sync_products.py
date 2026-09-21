from django.core.management.base import BaseCommand
from django.core.management import call_command
from products.models import Product, Category, Brand
import json
import os


class Command(BaseCommand):
    help = 'Safe product synchronization from localhost fixtures to production'

    def handle(self, *args, **options):
        self.stdout.write('=' * 70)
        self.stdout.write('SAFE PRODUCT SYNCHRONIZATION')
        self.stdout.write('=' * 70)
        
        # Check fixture files
        fixture_dir = os.getcwd()
        cat_fixture = os.path.join(fixture_dir, 'categories_fixture.json')
        prod_fixture = os.path.join(fixture_dir, 'products_fixture.json')
        
        self.stdout.write(f'Categories fixture: {os.path.exists(cat_fixture)}')
        self.stdout.write(f'Products fixture: {os.path.exists(prod_fixture)}')
        
        if not os.path.exists(cat_fixture) or not os.path.exists(prod_fixture):
            self.stdout.write(self.style.ERROR('Fixture files not found! Please run export_current_products first.'))
            return
        
        # Load fixture data to show what will be synced
        try:
            with open(cat_fixture, 'r', encoding='utf-8') as f:
                categories_data = json.load(f)
            
            with open(prod_fixture, 'r', encoding='utf-8') as f:
                products_data = json.load(f)
            
            fixture_categories = len([x for x in categories_data if x['model'] == 'products.category'])
            fixture_products = len([x for x in products_data if x['model'] == 'products.product'])
            
            self.stdout.write(f'\nFIXTURE DATA TO SYNC:')
            self.stdout.write(f'Categories: {fixture_categories}')
            self.stdout.write(f'Products: {fixture_products}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading fixtures: {e}'))
            return
        
        # Check current database state
        current_categories = Category.objects.count()
        current_products = Product.objects.count()
        
        self.stdout.write(f'\nCURRENT DATABASE STATE:')
        self.stdout.write(f'Categories: {current_categories}')
        self.stdout.write(f'Products: {current_products}')
        
        # Show sample of what will be synced
        self.stdout.write(f'\nSAMPLE PRODUCTS IN FIXTURE:')
        sample_products = [x for x in products_data if x['model'] == 'products.product'][:5]
        for prod in sample_products:
            fields = prod['fields']
            self.stdout.write(f"- {fields['name']} (SKU: {fields['sku']}, Price: {fields['regular_price']})")
        
        # Ask for confirmation
        self.stdout.write(f'\n' + '=' * 70)
        self.stdout.write('SYNC PLAN:')
        self.stdout.write('This will:')
        self.stdout.write('1. Update existing categories from fixture')
        self.stdout.write('2. Update existing products from fixture (by SKU)')
        self.stdout.write('3. Add new products that don\'t exist')
        self.stdout.write('4. NOT delete any existing products')
        self.stdout.write('5. Preserve all user data, orders, cart, wishlist')
        self.stdout.write('=' * 70)
        
        # For automation, we proceed without confirmation
        self.stdout.write('Proceeding with safe synchronization...')
        
        # Step 1: Sync categories
        try:
            self.stdout.write('\nStep 1: Syncing categories...')
            for cat_data in categories_data:
                if cat_data['model'] == 'products.category':
                    fields = cat_data['fields']
                    Category.objects.update_or_create(
                        pk=cat_data['pk'],
                        defaults=fields
                    )
            
            final_categories = Category.objects.count()
            self.stdout.write(self.style.SUCCESS(f'Categories synced: {current_categories} -> {final_categories}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error syncing categories: {e}'))
            import traceback
            traceback.print_exc()
        
        # Step 2: Sync products (by SKU for idempotency)
        try:
            self.stdout.write('\nStep 2: Syncing products...')
            
            # Create or get default brand
            brand, _ = Brand.objects.get_or_create(
                name='RedApple',
                defaults={'slug': 'redapple', 'is_featured': True}
            )
            
            updated_count = 0
            created_count = 0
            skipped_count = 0
            
            for prod_data in products_data:
                if prod_data['model'] == 'products.product':
                    fields = prod_data['fields']
                    sku = fields.get('sku')
                    
                    if not sku:
                        skipped_count += 1
                        continue
                    
                    # Handle category foreign key
                    category_id = fields.get('category')
                    if category_id:
                        try:
                            category = Category.objects.get(pk=category_id)
                            fields['category'] = category
                        except Category.DoesNotExist:
                            self.stdout.write(f'Category {category_id} not found, skipping product {sku}')
                            skipped_count += 1
                            continue
                    else:
                        skipped_count += 1
                        continue
                    
                    # Handle brand foreign key
                    brand_id = fields.get('brand')
                    if brand_id:
                        try:
                            brand = Brand.objects.get(pk=brand_id)
                            fields['brand'] = brand
                        except Brand.DoesNotExist:
                            fields['brand'] = None
                    else:
                        fields['brand'] = None
                    
                    # Handle festival foreign key
                    festival_id = fields.get('festival')
                    if festival_id:
                        fields['festival'] = None
                    
                    # Preserve Cloudinary image URLs
                    # If image_url starts with 'images/crackers/', keep it as-is for static files
                    # If it's a Cloudinary URL, keep it as-is
                    
                    # Sync by SKU for idempotency
                    existing_product = Product.objects.filter(sku=sku).first()
                    
                    if existing_product:
                        # Update existing product
                        for key, value in fields.items():
                            if key != 'id':  # Don't try to update the primary key
                                setattr(existing_product, key, value)
                        existing_product.save()
                        updated_count += 1
                    else:
                        # Create new product
                        Product.objects.create(**fields)
                        created_count += 1
            
            final_products = Product.objects.count()
            self.stdout.write(self.style.SUCCESS(f'Products synced: {current_products} -> {final_products}'))
            self.stdout.write(f'Updated: {updated_count}, Created: {created_count}, Skipped: {skipped_count}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error syncing products: {e}'))
            import traceback
            traceback.print_exc()
        
        # Final report
        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS('SYNCHRONIZATION COMPLETE'))
        self.stdout.write(f'Final Categories: {Category.objects.count()}')
        self.stdout.write(f'Final Products: {Product.objects.count()}')
        self.stdout.write(f'Active Products: {Product.objects.filter(is_active=True).count()}')
        self.stdout.write('=' * 70)
        self.stdout.write('Shop page should now show the updated product catalogue.')