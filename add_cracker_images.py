"""
Alternative script to add product images using high-quality placeholder images
from Unsplash (fireworks-related) that you can later replace with actual BabyCrackers images
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

# Using high-quality fireworks images from Unsplash as placeholders
# These can be replaced with actual BabyCrackers images when available

CRACKER_PRODUCTS = [
    {
        'name': 'Flower Pot',
        'image_url': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=400&h=400&fit=crop',
        'local_filename': 'flower-pot.jpg',
        'category': 'Fountains',
        'price': 150,
        'discount_price': 120,
        'description': 'Beautiful flower pot that creates stunning visual effects',
        'sku': 'BC-FLOWER-001'
    },
    {
        'name': 'Sky Rocket',
        'image_url': 'https://images.unsplash.com/photo-1573164713988-8665fc963095?w=400&h=400&fit=crop',
        'local_filename': 'sky-rocket.jpg',
        'category': 'Rockets',
        'price': 200,
        'discount_price': 160,
        'description': 'High-flying sky rocket with amazing burst patterns',
        'sku': 'BC-ROCKET-001'
    },
    {
        'name': 'Ground Chakkar',
        'image_url': 'https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?w=400&h=400&fit=crop',
        'local_filename': 'ground-chakkar.jpg',
        'category': 'Crackers',
        'price': 80,
        'discount_price': None,
        'description': 'Spinning ground chakkar with colorful lights',
        'sku': 'BC-CHAKKAR-001'
    },
    {
        'name': 'Golden Sparklers',
        'image_url': 'https://images.unsplash.com/photo-1534237710431-e2fc698436d0?w=400&h=400&fit=crop',
        'local_filename': 'golden-sparklers.jpg',
        'category': 'Sparklers',
        'price': 50,
        'discount_price': 40,
        'description': 'Long-lasting golden sparklers for any celebration',
        'sku': 'BC-SPARKLE-001'
    },
    {
        'name': 'Atom Bomb',
        'image_url': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&h=400&fit=crop',
        'local_filename': 'atom-bomb.jpg',
        'category': 'Crackers',
        'price': 100,
        'discount_price': 80,
        'description': 'Powerful atom bomb with loud sound and bright flash',
        'sku': 'BC-ATOM-001'
    },
    {
        'name': 'Multi Color Fountain',
        'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=400&fit=crop',
        'local_filename': 'multi-color-fountain.jpg',
        'category': 'Fountains',
        'price': 250,
        'discount_price': 200,
        'description': 'Multi-color fountain with cascading effects',
        'sku': 'BC-FOUNTAIN-001'
    },
    {
        'name': 'Whistling Rocket',
        'image_url': 'https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=400&h=400&fit=crop',
        'local_filename': 'whistling-rocket.jpg',
        'category': 'Rockets',
        'price': 180,
        'discount_price': 150,
        'description': 'Whistling rocket that creates excitement with sound',
        'sku': 'BC-WHISTLE-001'
    },
    {
        'name': 'Chakkar Ground',
        'image_url': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400&h=400&fit=crop',
        'local_filename': 'chakkar-ground.jpg',
        'category': 'Crackers',
        'price': 90,
        'discount_price': None,
        'description': 'Traditional ground chakkar with spinning motion',
        'sku': 'BC-CHAKKAR-002'
    },
    {
        'name': 'Color Sparklers',
        'image_url': 'https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=400&h=400&fit=crop',
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
        'image_url': 'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=400&h=400&fit=crop',
        'local_filename': 'fancy-fountain.jpg',
        'category': 'Fountains',
        'price': 300,
        'discount_price': 250,
        'description': 'Premium fancy fountain with multiple effects',
        'sku': 'BC-FOUNTAIN-002'
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
    
    for product_data in CRACKER_PRODUCTS:
        # Download image
        image_path = download_image(product_data['image_url'], product_data['local_filename'])
        
        if not image_path:
            continue
        
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
        if image_path:
            with open(image_path, 'rb') as f:
                product.main_image.save(product_data['local_filename'], File(f), save=True)
        
        if created:
            print(f"Created product: {product_data['name']}")
        else:
            print(f"Updated product: {product_data['name']}")
    
    print("\nAll products updated successfully!")
    print(f"Images saved to: {os.path.join(settings.BASE_DIR, 'static', 'images', 'crackers')}")

if __name__ == '__main__':
    print("Starting cracker product image download and database update...")
    print("Using high-quality placeholder images from Unsplash\n")
    
    update_products()