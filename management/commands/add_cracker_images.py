"""
Django management command to add cracker images from Unsplash
Run with: python manage.py add_cracker_images
"""

import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from products.models import Product, Category, Brand

class Command(BaseCommand):
    help = 'Download cracker images and update product database'

    def handle(self, *args, **options):
        self.stdout.write('Starting cracker product image download and database update...')
        
        # Using high-quality fireworks images from Unsplash as placeholders
        CRACKER_PRODUCTS = [
            {
                'name': 'Flower Pot',
                'image_url': 'https://images.unsplash.com/photo-1512496732179-4ecb94b36b92?w=400&h=400&fit=crop',
                'local_filename': 'flower-pot.jpg',
                'category': 'Fountains',
                'price': 150,
                'discount_price': 120,
                'description': 'Beautiful flower pot that creates stunning visual effects',
                'sku': 'BC-FLOWER-001'
            },
            {
                'name': 'Sky Rocket',
                'image_url': 'https://images.unsplash.com/photo-1467810563316-547d94611c32?w=400&h=400&fit=crop',
                'local_filename': 'sky-rocket.jpg',
                'category': 'Rockets',
                'price': 200,
                'discount_price': 160,
                'description': 'High-flying sky rocket with amazing burst patterns',
                'sku': 'BC-ROCKET-001'
            },
            {
                'name': 'Ground Chakkar',
                'image_url': 'https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=400&h=400&fit=crop',
                'local_filename': 'ground-chakkar.jpg',
                'category': 'Crackers',
                'price': 80,
                'discount_price': None,
                'description': 'Spinning ground chakkar with colorful lights',
                'sku': 'BC-CHAKKAR-001'
            },
            {
                'name': 'Golden Sparklers',
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
                'local_filename': 'golden-sparklers.jpg',
                'category': 'Sparklers',
                'price': 50,
                'discount_price': 40,
                'description': 'Long-lasting golden sparklers for any celebration',
                'sku': 'BC-SPARKLE-001'
            },
            {
                'name': 'Atom Bomb',
                'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=400&fit=crop',
                'local_filename': 'atom-bomb.jpg',
                'category': 'Crackers',
                'price': 100,
                'discount_price': 80,
                'description': 'Powerful atom bomb with loud sound and bright flash',
                'sku': 'BC-ATOM-001'
            },
            {
                'name': 'Multi Color Fountain',
                'image_url': 'https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=400&h=400&fit=crop',
                'local_filename': 'multi-color-fountain.jpg',
                'category': 'Fountains',
                'price': 250,
                'discount_price': 200,
                'description': 'Multi-color fountain with cascading effects',
                'sku': 'BC-FOUNTAIN-001'
            },
            {
                'name': 'Whistling Rocket',
                'image_url': 'https://images.unsplash.com/photo-1520306385303-7e7583ddc7ed?w=400&h=400&fit=crop',
                'local_filename': 'whistling-rocket.jpg',
                'category': 'Rockets',
                'price': 180,
                'discount_price': 150,
                'description': 'Whistling rocket that creates excitement with sound',
                'sku': 'BC-WHISTLE-001'
            },
            {
                'name': 'Chakkar Ground',
                'image_url': 'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=400&h=400&fit=crop',
                'local_filename': 'chakkar-ground.jpg',
                'category': 'Crackers',
                'price': 90,
                'discount_price': None,
                'description': 'Traditional ground chakkar with spinning motion',
                'sku': 'BC-CHAKKAR-002'
            },
            {
                'name': 'Color Sparklers',
                'image_url': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&h=400&fit=crop',
                'local_filename': 'color-sparklers.jpg',
                'category': 'Sparklers',
                'price': 75,
                'discount_price': 60,
                'description': 'Color-changing sparklers for magical effects',
                'sku': 'BC-SPARKLE-002'
            },
            {
                'name': 'Shot Gun',
                'image_url': 'https://images.unsplash.com/photo-1519074069444-1ba4fff66d16?w=400&h=400&fit=crop',
                'local_filename': 'shot-gun.jpg',
                'category': 'Crackers',
                'price': 120,
                'discount_price': 100,
                'description': 'Loud shot gun cracker for festive celebrations',
                'sku': 'BC-SHOTGUN-001'
            },
            {
                'name': 'Fancy Fountain',
                'image_url': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400&h=400&fit=crop',
                'local_filename': 'fancy-fountain.jpg',
                'category': 'Fountains',
                'price': 300,
                'discount_price': 250,
                'description': 'Premium fancy fountain with multiple effects',
                'sku': 'BC-FOUNTAIN-002'
            },
            {
                'name': 'Party Popper',
                'image_url': 'https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=400&h=400&fit=crop',
                'local_filename': 'party-popper.jpg',
                'category': 'Crackers',
                'price': 40,
                'discount_price': 30,
                'description': 'Safe party popper for indoor celebrations',
                'sku': 'BC-POPPER-001'
            },
        ]

        # Get or create brand
        brand, _ = Brand.objects.get_or_create(
            name='RedApple Premium',
            defaults={'slug': 'redapple-premium'}
        )
        
        for product_data in CRACKER_PRODUCTS:
            # Download image
            try:
                response = requests.get(product_data['image_url'], timeout=30)
                response.raise_for_status()
                
                # Create the full path for saving
                save_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'crackers', product_data['local_filename'])
                
                # Save the image
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                self.stdout.write(self.style.SUCCESS(f"✓ Downloaded: {product_data['local_filename']}"))
                
                # Get or create category
                category, _ = Category.objects.get_or_create(
                    name=product_data['category'],
                    defaults={'slug': product_data['category'].lower().replace(' ', '-')}
                )
                
                # Create or update product
                product, created = Product.objects.update_or_create(
                    sku=product_data['sku'],
                    defaults={
                        'name': product_data['name'],
                        'slug': product_data['name'].lower().replace(' ', '-'),
                        'category': category,
                        'brand': brand,
                        'short_description': f"Premium {product_data['name']}",
                        'description': product_data['description'],
                        'regular_price': product_data['price'],
                        'sale_price': product_data['discount_price'],
                        'stock': 50,
                        'is_active': True,
                        'is_featured': True,
                        'is_new': True,
                    }
                )
                
                # Update the product image
                with open(save_path, 'rb') as f:
                    product.main_image.save(product_data['local_filename'], File(f), save=True)
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"✓ Created product: {product_data['name']}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"✓ Updated product: {product_data['name']}"))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Failed to process {product_data['name']}: {e}"))
        
        self.stdout.write(self.style.SUCCESS("\n✓ All products updated successfully!"))
        self.stdout.write(f"✓ Images saved to: {os.path.join(settings.BASE_DIR, 'static', 'images', 'crackers')}")