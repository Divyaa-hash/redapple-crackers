"""
Comprehensive cracker products catalog with placeholder images
This creates a full catalog of typical crackers products
You can manually replace the images with actual BabyCrackers images later
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
from django.conf import settings
from django.core.files import File
from products.models import Product, Category, Brand

# Comprehensive cracker products catalog
COMPREHENSIVE_CRACKERS = [
    # FOUNTAINS
    {
        'name': 'Flower Pot Small',
        'image_url': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=400&h=400&fit=crop',
        'local_filename': 'flower-pot-small.jpg',
        'category': 'Fountains',
        'price': 120,
        'discount_price': 95,
        'description': 'Small flower pot for home celebrations',
        'sku': 'FP-SMALL-001'
    },
    {
        'name': 'Flower Pot Medium',
        'image_url': 'https://images.unsplash.com/photo-1573164713988-8665fc963095?w=400&h=400&fit=crop',
        'local_filename': 'flower-pot-medium.jpg',
        'category': 'Fountains',
        'price': 180,
        'discount_price': 150,
        'description': 'Medium flower pot with longer duration',
        'sku': 'FP-MED-001'
    },
    {
        'name': 'Flower Pot Large',
        'image_url': 'https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?w=400&h=400&fit=crop',
        'local_filename': 'flower-pot-large.jpg',
        'category': 'Fountains',
        'price': 250,
        'discount_price': 200,
        'description': 'Large flower pot for grand celebrations',
        'sku': 'FP-LRG-001'
    },
    {
        'name': 'Multi Color Fountain',
        'image_url': 'https://images.unsplash.com/photo-1534237710431-e2fc698436d0?w=400&h=400&fit=crop',
        'local_filename': 'multi-color-fountain.jpg',
        'category': 'Fountains',
        'price': 300,
        'discount_price': 250,
        'description': 'Multi-color fountain with various effects',
        'sku': 'MCF-001'
    },
    {
        'name': 'Golden Shower Fountain',
        'image_url': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&h=400&fit=crop',
        'local_filename': 'golden-shower-fountain.jpg',
        'category': 'Fountains',
        'price': 220,
        'discount_price': 180,
        'description': 'Golden shower fountain with sparkling effects',
        'sku': 'GSF-001'
    },
    
    # ROCKETS
    {
        'name': 'Sky Rocket 5 Shot',
        'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=400&fit=crop',
        'local_filename': 'sky-rocket-5-shot.jpg',
        'category': 'Rockets',
        'price': 350,
        'discount_price': 280,
        'description': '5-shot sky rocket with colorful bursts',
        'sku': 'SR-5-001'
    },
    {
        'name': 'Sky Rocket 10 Shot',
        'image_url': 'https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=400&h=400&fit=crop',
        'local_filename': 'sky-rocket-10-shot.jpg',
        'category': 'Rockets',
        'price': 550,
        'discount_price': 450,
        'description': '10-shot sky rocket for spectacular display',
        'sku': 'SR-10-001'
    },
    {
        'name': 'Whistling Rocket',
        'image_url': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400&h=400&fit=crop',
        'local_filename': 'whistling-rocket.jpg',
        'category': 'Rockets',
        'price': 180,
        'discount_price': 150,
        'description': 'Whistling rocket with sound effects',
        'sku': 'WR-001'
    },
    {
        'name': 'Multicolor Rocket',
        'image_url': 'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=400&h=400&fit=crop',
        'local_filename': 'multicolor-rocket.jpg',
        'category': 'Rockets',
        'price': 280,
        'discount_price': 220,
        'description': 'Multicolor rocket with varied effects',
        'sku': 'MR-001'
    },
    
    # SPARKLERS
    {
        'name': 'Golden Sparklers Pack',
        'image_url': 'https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=400&h=400&fit=crop',
        'local_filename': 'golden-sparklers-pack.jpg',
        'category': 'Sparklers',
        'price': 80,
        'discount_price': 60,
        'description': 'Pack of 10 golden sparklers',
        'sku': 'GS-10-001'
    },
    {
        'name': 'Color Sparklers Pack',
        'image_url': 'https://images.unsplash.com/photo-1519074069444-1ba4fff66d16?w=400&h=400&fit=crop',
        'local_filename': 'color-sparklers-pack.jpg',
        'category': 'Sparklers',
        'price': 100,
        'discount_price': 80,
        'description': 'Pack of 10 color-changing sparklers',
        'sku': 'CS-10-001'
    },
    {
        'name': 'Electric Sparklers',
        'image_url': 'https://images.unsplash.com/photo-1520306385303-7e7583ddc7ed?w=400&h=400&fit=crop',
        'local_filename': 'electric-sparklers.jpg',
        'category': 'Sparklers',
        'price': 120,
        'discount_price': 95,
        'description': 'Electric sparklers with enhanced brightness',
        'sku': 'ES-001'
    },
    
    # CRACKERS
    {
        'name': 'Atom Bomb',
        'image_url': 'https://images.unsplash.com/photo-1502086223501-68ea9946b40f?w=400&h=400&fit=crop',
        'local_filename': 'atom-bomb.jpg',
        'category': 'Crackers',
        'price': 150,
        'discount_price': 120,
        'description': 'Loud atom bomb with bright flash',
        'sku': 'AB-001'
    },
    {
        'name': 'Ground Chakkar',
        'image_url': 'https://images.unsplash.com/photo-1533238982087-a39b8af5254b?w=400&h=400&fit=crop',
        'local_filename': 'ground-chakkar.jpg',
        'category': 'Crackers',
        'price': 90,
        'discount_price': 70,
        'description': 'Spinning ground chakkar with lights',
        'sku': 'GC-001'
    },
    {
        'name': 'Chakkar Ground Large',
        'image_url': 'https://images.unsplash.com/photo-1467810563316-547d94611c32?w=400&h=400&fit=crop',
        'local_filename': 'chakkar-ground-large.jpg',
        'category': 'Crackers',
        'price': 130,
        'discount_price': 100,
        'description': 'Large ground chakkar with extended spin',
        'sku': 'GCL-001'
    },
    {
        'name': 'Shot Gun',
        'image_url': 'https://images.unsplash.com/photo-1573164713988-8665fc963095?w=400&h=400&fit=crop',
        'local_filename': 'shot-gun.jpg',
        'category': 'Crackers',
        'price': 110,
        'discount_price': 90,
        'description': 'Loud shot gun cracker',
        'sku': 'SG-001'
    },
    {
        'name': 'Larva Cracker',
        'image_url': 'https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?w=400&h=400&fit=crop',
        'local_filename': 'larva-cracker.jpg',
        'category': 'Crackers',
        'price': 95,
        'discount_price': 75,
        'description': 'Larva cracker with unique sound',
        'sku': 'LC-001'
    },
    
    # COMBOS
    {
        'name': 'Family Pack Combo',
        'image_url': 'https://images.unsplash.com/photo-1534237710431-e2fc698436d0?w=400&h=400&fit=crop',
        'local_filename': 'family-pack-combo.jpg',
        'category': 'Combos',
        'price': 1500,
        'discount_price': 1200,
        'description': 'Complete family pack with assorted crackers',
        'sku': 'FPC-001'
    },
    {
        'name': 'Premium Gift Box',
        'image_url': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&h=400&fit=crop',
        'local_filename': 'premium-gift-box.jpg',
        'category': 'Combos',
        'price': 2500,
        'discount_price': 2000,
        'description': 'Premium gift box with luxury crackers',
        'sku': 'PGB-001'
    },
]

def download_image(url, filename):
    """Download image from URL and save to local static folder"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Create the full path for saving
        save_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'crackers', filename)
        
        # Save the image
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {filename}")
        return save_path
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        return None

def update_products():
    """Download images and update product records in database"""
    
    # Get or create brand
    brand, _ = Brand.objects.get_or_create(
        name='RedApple Premium',
        defaults={'slug': 'redapple-premium'}
    )
    
    for product_data in COMPREHENSIVE_CRACKERS:
        # Download image
        image_path = download_image(product_data['image_url'], product_data['local_filename'])
        
        if not image_path:
            print(f"Skipping {product_data['name']} due to image download failure")
            continue
        
        # Get or create category
        category, _ = Category.objects.get_or_create(
            name=product_data['category'],
            defaults={'slug': product_data['category'].lower().replace(' ', '-')}
        )
        
        # Create or update product
        # Use a unique slug by adding random suffix if needed
        base_slug = product_data['name'].lower().replace(' ', '-')
        unique_slug = base_slug
        counter = 1
        
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        
        product, created = Product.objects.update_or_create(
            sku=product_data['sku'],
            defaults={
                'name': product_data['name'],
                'slug': unique_slug,
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
        if image_path:
            with open(image_path, 'rb') as f:
                product.main_image.save(product_data['local_filename'], File(f), save=True)
        
        if created:
            print(f"Created product: {product_data['name']}")
        else:
            print(f"Updated product: {product_data['name']}")
    
    print("\nAll products updated successfully!")
    print(f"Images saved to: {os.path.join(settings.BASE_DIR, 'static', 'images', 'crackers')}")
    print(f"Total products: {len(COMPREHENSIVE_CRACKERS)}")

if __name__ == '__main__':
    print("Starting comprehensive cracker product import...")
    print("This will create a full catalog of cracker products\n")
    
    update_products()