"""
Script to download product images from BabyCrackers and update Django database
Since BabyCrackers.com is a dynamic SPA, you'll need to manually inspect the site
to get the actual image URLs, then add them to the products list below.
"""

import os
import requests
from django.conf import settings
from django.core.files import File
from products.models import Product, Category, Brand

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

# Product data from BabyCrackers - ADD YOUR ACTUAL IMAGE URLs HERE
# You can inspect the website, network requests, or use browser developer tools
# to find the actual image URLs from babycrackers.com

PRODUCTS_TO_UPDATE = [
    {
        'name': 'Flower Pot',
        'image_url': 'https://example.com/flower-pot.jpg',  # Replace with actual URL
        'local_filename': 'flower-pot.jpg',
        'category': 'Fountains',
        'price': 150,
        'discount_price': 120
    },
    {
        'name': 'Sky Rocket',
        'image_url': 'https://example.com/rocket.jpg',  # Replace with actual URL
        'local_filename': 'rocket.jpg',
        'category': 'Rockets',
        'price': 200,
        'discount_price': 160
    },
    {
        'name': 'Ground Chakkar',
        'image_url': 'https://example.com/ground-chakkar.jpg',  # Replace with actual URL
        'local_filename': 'ground-chakkar.jpg',
        'category': 'Crackers',
        'price': 80,
        'discount_price': None
    },
    {
        'name': 'Sparklers',
        'image_url': 'https://example.com/sparklers.jpg',  # Replace with actual URL
        'local_filename': 'sparklers.jpg',
        'category': 'Sparklers',
        'price': 50,
        'discount_price': 40
    },
    {
        'name': 'Atom Bomb',
        'image_url': 'https://example.com/atom-bomb.jpg',  # Replace with actual URL
        'local_filename': 'atom-bomb.jpg',
        'category': 'Crackers',
        'price': 100,
        'discount_price': 80
    },
    {
        'name': 'Multi Color Fountain',
        'image_url': 'https://example.com/multi-color-fountain.jpg',  # Replace with actual URL
        'local_filename': 'multi-color-fountain.jpg',
        'category': 'Fountains',
        'price': 250,
        'discount_price': 200
    },
    {
        'name': 'Whistling Rocket',
        'image_url': 'https://example.com/whistling-rocket.jpg',  # Replace with actual URL
        'local_filename': 'whistling-rocket.jpg',
        'category': 'Rockets',
        'price': 180,
        'discount_price': 150
    },
    {
        'name': 'Chakkar Ground',
        'image_url': 'https://example.com/chakkar-ground.jpg',  # Replace with actual URL
        'local_filename': 'chakkar-ground.jpg',
        'category': 'Crackers',
        'price': 90,
        'discount_price': None
    },
    {
        'name': 'Color Sparklers',
        'image_url': 'https://example.com/color-sparklers.jpg',  # Replace with actual URL
        'local_filename': 'color-sparklers.jpg',
        'category': 'Sparklers',
        'price': 75,
        'discount_price': 60
    },
    {
        'name': 'Shot Gun',
        'image_url': 'https://example.com/shot-gun.jpg',  # Replace with actual URL
        'local_filename': 'shot-gun.jpg',
        'category': 'Crackers',
        'price': 120,
        'discount_price': 100
    },
    {
        'name': 'Fancy Fountain',
        'image_url': 'https://example.com/fancy-fountain.jpg',  # Replace with actual URL
        'local_filename': 'fancy-fountain.jpg',
        'category': 'Fountains',
        'price': 300,
        'discount_price': 250
    },
    {
        'name': 'Party Popper',
        'image_url': 'https://example.com/party-popper.jpg',  # Replace with actual URL
        'local_filename': 'party-popper.jpg',
        'category': 'Crackers',
        'price': 40,
        'discount_price': 30
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
        
        print(f"✓ Downloaded: {filename}")
        return save_path
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")
        return None

def update_products():
    """Download images and update product records in database"""
    
    # Get or create brand
    brand, _ = Brand.objects.get_or_create(
        name='BabyCrackers',
        defaults={'slug': 'babycrackers'}
    )
    
    for product_data in PRODUCTS_TO_UPDATE:
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
            name=product_data['name'],
            defaults={
                'slug': product_data['name'].lower().replace(' ', '-'),
                'sku': f"BC-{product_data['name'].upper().replace(' ', '-')[:8]}",
                'category': category,
                'brand': brand,
                'short_description': f"Premium {product_data['name']} from BabyCrackers",
                'description': f"High-quality {product_data['name']} perfect for celebrations. Safe and reliable fireworks product.",
                'regular_price': product_data['price'],
                'sale_price': product_data['discount_price'],
                'stock': 50,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        # Update the product image
        if image_path:
            with open(image_path, 'rb') as f:
                product.main_image.save(product_data['local_filename'], File(f), save=True)
        
        if created:
            print(f"✓ Created product: {product_data['name']}")
        else:
            print(f"✓ Updated product: {product_data['name']}")
    
    print("\n✓ All products updated successfully!")

if __name__ == '__main__':
    print("Starting BabyCrackers image download and product update...")
    print("Note: Make sure to replace the placeholder URLs with actual BabyCrackers image URLs")
    print("You can find these by inspecting the website in your browser's developer tools\n")
    
    update_products()