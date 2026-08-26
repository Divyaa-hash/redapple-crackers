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
        
        # Create products
        products_data = [
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
            },
        ]
        
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
