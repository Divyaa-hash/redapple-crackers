from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from products.models import Category, Brand, Product, Festival
from decimal import Decimal
import random
import pandas as pd
import os


class Command(BaseCommand):
    help = 'Seed database with sample products data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with sample data...')
        
        # Load Excel data
        try:
            excel_path = 'Vamsi_Crackers 2026 diwali.xlsx'
            df = pd.read_excel(excel_path)
            self.stdout.write(f'Loaded {len(df)} products from Excel file')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading Excel file: {e}'))
            return
        
        # Create categories from Excel
        excel_categories = df['Category'].unique().tolist()
        categories_data = []
        for i, cat_name in enumerate(excel_categories):
            slug = cat_name.lower().replace(' ', '-').replace('/', '-').replace('&', 'and').replace('(', '').replace(')', '').replace(',', '')
            categories_data.append({
                'name': cat_name,
                'slug': slug,
                'description': f'{cat_name} products',
                'order': i + 1
            })
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                # Update existing category
                for key, value in cat_data.items():
                    setattr(category, key, value)
                category.save()
                self.stdout.write(f'Updated category: {category.name}')
        
        # Create brands
        brands_data = [
            {'name': 'RedApple', 'slug': 'redapple', 'is_featured': True},
            {'name': 'Celebration', 'slug': 'celebration', 'is_featured': True},
            {'name': 'JoyFest', 'slug': 'joyfest', 'is_featured': False},
            {'name': 'SparkMaster', 'slug': 'sparkmaster', 'is_featured': False},
        ]
        
        brands = []
        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                slug=brand_data['slug'],
                defaults=brand_data
            )
            brands.append(brand)
            if created:
                self.stdout.write(f'Created brand: {brand.name}')
        
        # Create festival
        festival, created = Festival.objects.get_or_create(
            name='Diwali',
            defaults={
                'slug': 'diwali',
                'description': 'Festival of Lights',
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date(),
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'Created festival: {festival.name}')
        else:
            self.stdout.write(f'Festival already exists: {festival.name}')
        
        # Create category mapping
        category_map = {cat.name: cat for cat in categories}
        
        # Get uploaded images list from media/products directory
        media_products_path = os.path.join(settings.BASE_DIR, 'media', 'products')
        uploaded_images = []
        if os.path.exists(media_products_path):
            for filename in os.listdir(media_products_path):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    uploaded_images.append(f'products/{filename}')
        
        if not uploaded_images:
            self.stdout.write(self.style.WARNING('No images found in media/products directory'))
            uploaded_images = ['products/placeholder.jpg']
        
        # Define the 4 specific gift box images
        gift_box_images = [
            'diwali-special-gift-box-367.jpg',
            'premium-gift-box.jpg',
            'wedding-gift-box-806.jpg',
            'family-pack-combo.jpg'
        ]
        
        # Verify gift box images exist
        available_gift_box_images = []
        for img in gift_box_images:
            img_path = os.path.join(settings.BASE_DIR, 'media', 'products', img)
            if os.path.exists(img_path):
                available_gift_box_images.append(f'products/{img}')
            else:
                self.stdout.write(self.style.WARNING(f'Gift box image not found: {img}'))
        
        if not available_gift_box_images:
            self.stdout.write(self.style.WARNING('No gift box images found, using first available image'))
            available_gift_box_images = [uploaded_images[0]] if uploaded_images else ['products/placeholder.jpg']
        
        # Create products from Excel data (limit to 202 products to include gift boxes and family packs)
        products_data = []
        max_products = 202
        product_count = 0
        
        for index, row in df.iterrows():
            if product_count >= max_products:
                break
                
            if row['Status'] != 'Active':
                continue
                
            product_name = row['Product Name']
            category_name = row['Category']
            original_price = row['Original Price']
            offer_price = row['Offer Price']
            
            # Skip if no price data
            if pd.isna(original_price) and pd.isna(offer_price):
                continue
                
            # Use offer price if available, otherwise original price, add 10% markup
            base_price = offer_price if pd.notna(offer_price) else original_price
            if pd.isna(base_price):
                continue
                
            # Add 10% markup
            regular_price = Decimal(str(float(base_price) * 1.1))
            sale_price = None
            
            # If there was an offer price, use it as sale price with 10% markup
            if pd.notna(offer_price) and pd.notna(original_price):
                sale_price = regular_price
                regular_price = Decimal(str(float(original_price) * 1.1))
            
            # Get category
            category = category_map.get(category_name)
            if not category:
                self.stdout.write(f'Warning: Category not found: {category_name}')
                continue
            
            # Generate slug
            slug = product_name.lower().replace(' ', '-').replace('/', '-').replace('&', 'and').replace('(', '').replace(')', '').replace(',', '').replace('"', '').replace("'", '')
            
            # Generate SKU
            if 'GIFT BOXES' in category_name:
                # Use specific SKUs for gift boxes
                if 'Love Feast' in product_name:
                    sku = 'GB-LF-20'
                    slug = 'love-feast-20-item'
                elif 'Turbo' in product_name:
                    sku = 'GB-TB-30'
                    slug = 'turbo-30-item'
                elif 'Fun Special' in product_name:
                    sku = 'GB-FS-40'
                    slug = 'fun-special-40-item'
                elif 'Spectra Festive' in product_name:
                    sku = 'GB-SF-50'
                    slug = 'spectra-festive-50-item'
                else:
                    sku = f'VMS-{index + 1:03d}'
            else:
                sku = f'VMS-{index + 1:03d}'
            
            # Assign image - use specific gift box images for gift boxes
            if sku in ['GB-LF-20', 'GB-TB-30', 'GB-FS-40', 'GB-SF-50']:
                # Assign specific gift box images
                gift_box_image_map = {
                    'GB-LF-20': available_gift_box_images[0] if len(available_gift_box_images) > 0 else 'products/placeholder.jpg',
                    'GB-TB-30': available_gift_box_images[1] if len(available_gift_box_images) > 1 else 'products/placeholder.jpg',
                    'GB-FS-40': available_gift_box_images[2] if len(available_gift_box_images) > 2 else 'products/placeholder.jpg',
                    'GB-SF-50': available_gift_box_images[3] if len(available_gift_box_images) > 3 else 'products/placeholder.jpg',
                }
                image_path = gift_box_image_map[sku]
            else:
                # Assign image using modulo for other products
                image_index = index % len(uploaded_images)
                image_path = uploaded_images[image_index]
            
            product_count += 1
            
            # Determine product type based on category
            product_type = 'single'
            if 'GIFT BOXES' in category_name or 'FAMILY PACK' in category_name:
                product_type = 'gift_box'
            elif 'PACK' in product_name or 'Pcs' in product_name:
                product_type = 'box'
            elif 'SET' in product_name or 'COMBO' in product_name:
                product_type = 'combo'
            
            # Determine safety level
            safety_level = 'medium'
            if any(word in category_name for word in ['BOMB', 'CRACKERS', 'ROCKET']):
                safety_level = 'high'
            elif any(word in category_name for word in ['SPARKLERS', 'CANDLES', 'TOYS']):
                safety_level = 'low'
            
            products_data.append({
                'name': product_name,
                'slug': slug,
                'sku': sku,
                'category': category,
                'brand': brands[0],
                'product_type': product_type,
                'safety_level': safety_level,
                'short_description': f'{product_name} - {category_name}',
                'description': f'{product_name} from {category_name}. High quality crackers for celebrations and festivals.',
                'regular_price': regular_price,
                'sale_price': sale_price,
                'stock': random.randint(10, 100),
                'pieces': 1,
                'is_active': True,
                'is_featured': random.random() > 0.8,
                'is_new': random.random() > 0.9,
                'is_bestseller': random.random() > 0.85,
                'is_trending': random.random() > 0.85,
                'main_image': image_path,
                'additional_images': [],
            })
        
        self.stdout.write(f'Prepared {len(products_data)} products from Excel data')
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                sku=prod_data['sku'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
            else:
                # Update existing product
                for key, value in prod_data.items():
                    setattr(product, key, value)
                product.save()
                self.stdout.write(f'Updated product: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
