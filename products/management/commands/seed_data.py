from django.core.management.base import BaseCommand
from django.utils import timezone
from products.models import Category, Brand, Product, Festival
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Seed database with sample products data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with sample data...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Sparklers',
                'slug': 'sparklers',
                'description': 'Handheld sparklers for celebrations',
                'order': 1
            },
            {
                'name': 'Rockets',
                'slug': 'rockets',
                'description': 'Sky rockets for spectacular displays',
                'order': 2
            },
            {
                'name': 'Fountains',
                'slug': 'fountains',
                'description': 'Ground fountains with colorful effects',
                'order': 3
            },
            {
                'name': 'Crackers',
                'slug': 'crackers',
                'description': 'Traditional crackers for festivals',
                'order': 4
            },
            {
                'name': 'Chakkar',
                'slug': 'chakkar',
                'description': 'Spinning ground wheels',
                'order': 5
            },
            {
                'name': 'Bombs',
                'slug': 'bombs',
                'description': 'Explosive bombs for loud celebrations',
                'order': 6
            },
            {
                'name': 'Flower Pots',
                'slug': 'flower-pots',
                'description': 'Colorful flower pot crackers',
                'order': 7
            },
            {
                'name': 'Sky Lanterns',
                'slug': 'sky-lanterns',
                'description': 'Floating sky lanterns',
                'order': 8
            },
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
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
            slug='diwali',
            defaults={
                'name': 'Diwali',
                'description': 'Festival of Lights',
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date(),
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'Created festival: {festival.name}')
        
        # Create products - generate 171 products
        products_data = []
        
        # Base product templates with actual uploaded images
        product_templates = [
            {
                'name': 'Golden Sparklers (Pack of 10)',
                'slug': 'golden-sparklers-pack-10',
                'sku': 'SPK-001',
                'category': categories[0],
                'brand': brands[0],
                'product_type': 'box',
                'safety_level': 'low',
                'short_description': 'Premium golden sparklers for celebrations',
                'description': 'High-quality golden sparklers that burn steadily with bright golden sparks. Perfect for Diwali and other celebrations.',
                'regular_price': Decimal('150.00'),
                'sale_price': Decimal('120.00'),
                'stock': 100,
                'pieces': 10,
                'duration': '60 seconds',
                'is_featured': True,
                'is_trending': True,
                'is_bestseller': True,
                'main_image': 'images/crackers/20250822073252.jpg',
                'additional_images': [],
            },
            {
                'name': 'Colorful Sky Rocket',
                'slug': 'colorful-sky-rocket',
                'sku': 'RKT-001',
                'category': categories[1],
                'brand': brands[0],
                'product_type': 'single',
                'safety_level': 'high',
                'short_description': 'Spectacular colorful sky rocket',
                'description': 'Launches high into the sky and explodes with colorful patterns. A crowd favorite for celebrations.',
                'regular_price': Decimal('250.00'),
                'sale_price': Decimal('200.00'),
                'stock': 50,
                'pieces': 1,
                'height': '100 meters',
                'is_featured': True,
                'is_trending': True,
                'main_image': 'images/crackers/20250822073925.jpeg',
                'additional_images': [],
            },
            {
                'name': 'Rainbow Fountain',
                'slug': 'rainbow-fountain',
                'sku': 'FTN-001',
                'category': categories[2],
                'brand': brands[1],
                'product_type': 'single',
                'safety_level': 'medium',
                'short_description': 'Colorful rainbow fountain display',
                'description': 'Ground fountain that shoots up colorful sparks in a rainbow pattern. Lasts for 2 minutes.',
                'regular_price': Decimal('180.00'),
                'stock': 75,
                'pieces': 1,
                'duration': '120 seconds',
                'is_featured': True,
                'is_new': True,
                'main_image': 'images/crackers/20250822074448.jpg',
                'additional_images': [],
            },
            {
                'name': 'Loud Crackers Box (50 pcs)',
                'slug': 'loud-crackers-box-50',
                'sku': 'CRK-001',
                'category': categories[3],
                'brand': brands[0],
                'product_type': 'box',
                'safety_level': 'high',
                'short_description': 'Traditional loud crackers',
                'description': 'Box of 50 traditional loud crackers. Perfect for creating festive noise during celebrations.',
                'regular_price': Decimal('300.00'),
                'sale_price': Decimal('250.00'),
                'stock': 60,
                'pieces': 50,
                'is_bestseller': True,
                'is_trending': True,
                'main_image': 'images/crackers/20250822074924.jpg',
                'additional_images': [],
            },
            {
                'name': 'Spinning Chakkar',
                'slug': 'spinning-chakkar',
                'sku': 'CHK-001',
                'category': categories[4],
                'brand': brands[2],
                'product_type': 'single',
                'safety_level': 'medium',
                'short_description': 'Colorful spinning ground wheel',
                'description': 'Spinning chakkar that creates beautiful patterns on the ground while spinning rapidly.',
                'regular_price': Decimal('80.00'),
                'stock': 120,
                'pieces': 1,
                'duration': '45 seconds',
                'is_new': True,
                'main_image': 'images/crackers/20250822075102.jpg',
                'additional_images': [],
            },
            {
                'name': 'Atom Bomb',
                'slug': 'atom-bomb',
                'sku': 'BMB-001',
                'category': categories[5],
                'brand': brands[0],
                'product_type': 'single',
                'safety_level': 'high',
                'short_description': 'Powerful atom bomb cracker',
                'description': 'Loud and powerful atom bomb cracker. Use with caution and follow safety guidelines.',
                'regular_price': Decimal('100.00'),
                'stock': 80,
                'pieces': 1,
                'is_bestseller': True,
                'main_image': 'images/crackers/20250822075125.jpg',
                'additional_images': [],
            },
            {
                'name': 'Red Flower Pot',
                'slug': 'red-flower-pot',
                'sku': 'FLP-001',
                'category': categories[6],
                'brand': brands[1],
                'product_type': 'single',
                'safety_level': 'medium',
                'short_description': 'Beautiful red flower pot',
                'description': 'Elegant red flower pot that blooms with colorful sparks. Perfect for home celebrations.',
                'regular_price': Decimal('120.00'),
                'sale_price': Decimal('99.00'),
                'stock': 90,
                'pieces': 1,
                'duration': '90 seconds',
                'is_featured': True,
                'main_image': 'images/crackers/20250822081608.jpg',
                'additional_images': [],
            },
            {
                'name': 'Sky Lantern (Pack of 5)',
                'slug': 'sky-lantern-pack-5',
                'sku': 'LNT-001',
                'category': categories[7],
                'brand': brands[3],
                'product_type': 'box',
                'safety_level': 'low',
                'short_description': 'Floating sky lanterns',
                'description': 'Pack of 5 beautiful sky lanterns that float up gracefully. Perfect for evening celebrations.',
                'regular_price': Decimal('400.00'),
                'stock': 40,
                'pieces': 5,
                'is_new': True,
                'is_featured': True,
                'main_image': 'images/crackers/20250822081917.jpg',
                'additional_images': [],
            },
            {
                'name': 'Silver Sparklers (Pack of 20)',
                'slug': 'silver-sparklers-pack-20',
                'sku': 'SPK-002',
                'category': categories[0],
                'brand': brands[0],
                'product_type': 'box',
                'safety_level': 'low',
                'short_description': 'Premium silver sparklers',
                'description': 'High-quality silver sparklers with bright silver sparks. Longer burning time.',
                'regular_price': Decimal('280.00'),
                'sale_price': Decimal('220.00'),
                'stock': 85,
                'pieces': 20,
                'duration': '90 seconds',
                'is_trending': True,
                'main_image': 'images/crackers/20250822081925.jpg',
                'additional_images': [],
            },
            {
                'name': 'Multi-Color Rocket Set',
                'slug': 'multi-color-rocket-set',
                'sku': 'RKT-002',
                'category': categories[1],
                'brand': brands[1],
                'product_type': 'combo',
                'safety_level': 'high',
                'short_description': 'Set of 5 multi-color rockets',
                'description': 'Combo pack of 5 rockets with different color effects. Great value for money.',
                'regular_price': Decimal('1000.00'),
                'sale_price': Decimal('800.00'),
                'stock': 30,
                'pieces': 5,
                'is_featured': True,
                'is_limited_edition': True,
                'main_image': 'images/crackers/20250822081933.jpg',
                'additional_images': [],
            },
        ]
        
        # Add base products
        products_data.extend(product_templates)
        
        # Generate additional products to reach 171 total
        # Use actual uploaded image filenames from product_list
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
        
        for i in range(11, 172):
            category = categories[i % len(categories)]
            brand = brands[i % len(brands)]
            product_type = random.choice(['single', 'box', 'combo', 'gift_box'])
            safety_level = random.choice(['low', 'medium', 'high'])
            
            base_price = random.randint(50, 2000)
            has_sale = random.random() > 0.5
            sale_price = Decimal(str(base_price * 0.8)) if has_sale else None
            
            # Assign actual uploaded image
            image_index = (i - 11) % len(uploaded_images)
            image_path = uploaded_images[image_index]
            
            products_data.append({
                'name': f'Premium {category.name} #{i}',
                'slug': f'premium-{category.slug}-{i}',
                'sku': f'PRD-{i:03d}',
                'category': category,
                'brand': brand,
                'product_type': product_type,
                'safety_level': safety_level,
                'short_description': f'High-quality {category.name} for celebrations',
                'description': f'Premium {category.name} from {brand.name}. Perfect for festivals and special occasions. Safe and reliable.',
                'regular_price': Decimal(str(base_price)),
                'sale_price': sale_price,
                'stock': random.randint(10, 200),
                'pieces': random.randint(1, 50),
                'is_featured': random.random() > 0.8,
                'is_new': random.random() > 0.7,
                'is_bestseller': random.random() > 0.8,
                'is_trending': random.random() > 0.8,
                'main_image': image_path,
                'additional_images': [],
            })
        
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
