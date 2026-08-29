from django.core.management.base import BaseCommand
from django.utils import timezone
from products.models import Category, Brand, Product, Festival
from decimal import Decimal
import random
import pandas as pd


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
        
        # Get uploaded images list
        uploaded_images = [
            'images/crackers/20250822073252.jpg',
            'images/crackers/20250822073925.jpeg',
            'images/crackers/20250822074448.jpg',
            'images/crackers/20250822074924.jpg',
            'images/crackers/20250822075102.jpg',
            'images/crackers/20250822075125.jpg',
            'images/crackers/20250822081608.jpg',
            'images/crackers/20250822081917.jpg',
            'images/crackers/20250822081925.jpg',
            'images/crackers/20250822081933.jpg',
            'images/crackers/20250822081944.jpg',
            'images/crackers/20250822082214.jpg',
            'images/crackers/20250822082424.jpg',
            'images/crackers/20250822082436.jpg',
            'images/crackers/20250822082448.jpg',
            'images/crackers/20250822082458.jpg',
            'images/crackers/20250822082819.jpg',
            'images/crackers/20250822082916.jpg',
            'images/crackers/20250822082924.jpg',
            'images/crackers/20250822082931.jpg',
            'images/crackers/20250822082939.jpg',
            'images/crackers/20250822082947.jpg',
            'images/crackers/20250822083104.jpg',
            'images/crackers/20250822083112.jpg',
            'images/crackers/20250822083504.png',
            'images/crackers/20250822083509.jpg',
            'images/crackers/20250822084439.jpg',
            'images/crackers/20250822084828.jpg',
            'images/crackers/20250822084838.jpg',
            'images/crackers/20250822084934.jpg',
            'images/crackers/20250822085012.png',
            'images/crackers/20250822085251.jpg',
            'images/crackers/20250822085410.png',
            'images/crackers/20250822085428.jpg',
            'images/crackers/20250822085435.jpg',
            'images/crackers/20250822085538.jpg',
            'images/crackers/20250822085546.jpg',
            'images/crackers/20250822085551.jpg',
            'images/crackers/20250822090447.jpg',
            'images/crackers/20250822090513.jpg',
            'images/crackers/20250822090654.jpg',
            'images/crackers/20250822090701.jpg',
            'images/crackers/20250822090724.jpg',
            'images/crackers/20250822091709.jpg',
            'images/crackers/20250822091738.jpg',
            'images/crackers/20250822091957.jpg',
            'images/crackers/20250822092004.jpg',
            'images/crackers/20250822092056.jpg',
            'images/crackers/20250822092109.jpg',
            'images/crackers/20250822092140.jpg',
            'images/crackers/20250822092200.jpg',
            'images/crackers/20250822092312.jpg',
            'images/crackers/20250822092420.jpg',
            'images/crackers/20250822092912.jpg',
            'images/crackers/20250822092919.jpg',
            'images/crackers/20250822092924.jpg',
            'images/crackers/20250822092938.jpg',
            'images/crackers/20250823062123.jpg',
            'images/crackers/20250823062221.jpg',
            'images/crackers/20250823062331.jpg',
            'images/crackers/20250823065657.jpg',
            'images/crackers/20250823065703.jpg',
            'images/crackers/20250823065951.jpg',
            'images/crackers/20250823070113.jpg',
            'images/crackers/20250823070606.jpg',
            'images/crackers/20250823070757.jpg',
            'images/crackers/20250823070939.jpg',
            'images/crackers/20250823071229.jpg',
            'images/crackers/20250823071410.jpg',
            'images/crackers/20250823080608.jpg',
            'images/crackers/20250823080612.jpg',
            'images/crackers/20250825022233.jpg',
            'images/crackers/20250825022440.jpg',
            'images/crackers/20250825023332.jpg',
            'images/crackers/20250825023341.jpg',
            'images/crackers/20250825023447.jpg',
            'images/crackers/20250825023453.jpg',
            'images/crackers/20250825023501.jpg',
            'images/crackers/20250825023510.jpg',
            'images/crackers/20250825023914.jpg',
            'images/crackers/20250825024108.jpg',
            'images/crackers/20250825024117.jpg',
            'images/crackers/20250825024124.jpg',
            'images/crackers/20250825024135.jpg',
            'images/crackers/20250825024143.jpg',
            'images/crackers/20250825024157.jpg',
            'images/crackers/20250825024223.jpg',
            'images/crackers/20250825024529.jpg',
            'images/crackers/20250825025343.jpg',
            'images/crackers/20250825025357.jpg',
            'images/crackers/20250825025514.jpg',
            'images/crackers/20250825025533.jpg',
            'images/crackers/20250825025735.jpg',
            'images/crackers/20250825025745.jpg',
            'images/crackers/20250825025753.jpg',
            'images/crackers/20250825025759.jpg',
            'images/crackers/20250825025809.jpg',
            'images/crackers/20250825025822.jpg',
            'images/crackers/20250825025841.jpg',
            'images/crackers/20250825025903.jpg',
            'images/crackers/20250825030032.jpg',
            'images/crackers/20250825030211.jpg',
            'images/crackers/20250825030258.jpg',
            'images/crackers/20250825030308.jpg',
            'images/crackers/20250825030402.jpg',
            'images/crackers/20250825030542.jpg',
            'images/crackers/20250825030912.jpg',
            'images/crackers/20250825030931.jpg',
            'images/crackers/20250825030940.jpg',
            'images/crackers/20250830053032.jpg',
            'images/crackers/20250830054207.jpg',
            'images/crackers/20250830054225.jpg',
            'images/crackers/20250830054236.jpg',
            'images/crackers/20250830054243.jpg',
            'images/crackers/20250830054255.jpeg',
            'images/crackers/20250830054643.jpg',
            'images/crackers/20250830055056.jpg',
            'images/crackers/20250830060249.jpg',
            'images/crackers/20250830060304.jpg',
            'images/crackers/20250830060328.jpg',
            'images/crackers/20250902013326.jpeg',
            'images/crackers/20250902013728.jpg',
            'images/crackers/20250902014024.jpeg',
            'images/crackers/20250902045926.jpeg',
            'images/crackers/20250902050305.jpg',
            'images/crackers/20250902050503.jpeg',
            'images/crackers/20250902050640.jpeg',
            'images/crackers/20250902050715.jpg',
            'images/crackers/20250902050944.jpg',
            'images/crackers/20250902051034.jpg',
            'images/crackers/20250902051217.jpg',
            'images/crackers/20250902060635.jpg',
            'images/crackers/20250902060814.jpg',
            'images/crackers/20250902060825.jpg',
            'images/crackers/20250902060921.jpg',
            'images/crackers/20250902061212.jpg',
            'images/crackers/20250902061858.png',
            'images/crackers/20250902061904.jpg',
            'images/crackers/20250902061911.png',
            'images/crackers/20250902062229.jpg',
            'images/crackers/20250902062235.jpg',
            'images/crackers/20250902062240.jpg',
            'images/crackers/20250902062510.jpg',
            'images/crackers/20250902063842.jpg',
            'images/crackers/20250902095402.png',
            'images/crackers/20250902095643.jpg',
            'images/crackers/20250902095738.jpg',
            'images/crackers/20250902095742.jpg',
            'images/crackers/20250902095914.jpeg',
            'images/crackers/20250902095920.jpg',
            'images/crackers/20250902100103.jpg',
            'images/crackers/20250902100117.jpg',
            'images/crackers/20250902114322.jpg',
            'images/crackers/20250910081622.jpg',
            'images/crackers/20250910082458.jpg',
            'images/crackers/20250910083043.jpg',
            'images/crackers/20250910083634.jpeg',
            'images/crackers/20250910083901.jpg',
            'images/crackers/20250910084504.jpg',
            'images/crackers/20250915092351.jpg',
            'images/crackers/20250915093339.jpg',
            'images/crackers/20250915093752.jpg',
            'images/crackers/20250915101616.jpg',
            'images/crackers/20250922070716.jpeg',
            'images/crackers/20250923041551.jpg',
            'images/crackers/20250923041959.jpg',
            'images/crackers/20250923042148.jpg',
            'images/crackers/20250923042534.jpg',
            'images/crackers/20250930060047.jpeg',
            'images/crackers/20251010060432.jpg',
        ]
        
        # Create products from Excel data
        products_data = []
        for index, row in df.iterrows():
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
            sku = f'VMS-{index + 1:03d}'
            
            # Assign image
            image_index = index % len(uploaded_images)
            image_path = uploaded_images[image_index]
            
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
