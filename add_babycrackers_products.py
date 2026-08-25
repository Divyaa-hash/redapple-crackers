"""
Script to add BabyCrackers products with their actual images
Once you extract the image URLs from BabyCrackers, add them to the BABYCRACKERS_PRODUCTS list below
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

# ADD YOUR BABYCRACKERS PRODUCT DATA HERE
# Format: {'name': 'Product Name', 'image_url': 'https://...', 'category': 'Category', 'price': 100, 'discount_price': 80}
BABYCRACKERS_PRODUCTS = [
    # Example - replace with actual BabyCrackers data:
    {
        'name': 'Flower Pot',
        'image_url': 'https://www.babycrackers.com/images/flower-pot.jpg',  # Replace with actual URL
        'local_filename': 'flower-pot.jpg',
        'category': 'Fountains',
        'price': 150,
        'discount_price': 120,
        'description': 'Premium flower pot from BabyCrackers',
        'sku': 'BC-FLOWER-001'
    },
    # Add more products here...
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
        name='BabyCrackers',
        defaults={'slug': 'babycrackers'}
    )
    
    for product_data in BABYCRACKERS_PRODUCTS:
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
        product, created = Product.objects.update_or_create(
            sku=product_data['sku'],
            defaults={
                'name': product_data['name'],
                'slug': product_data['name'].lower().replace(' ', '-'),
                'category': category,
                'brand': brand,
                'short_description': f"Premium {product_data['name']} from BabyCrackers",
                'description': product_data['description'],
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
            print(f"Created product: {product_data['name']}")
        else:
            print(f"Updated product: {product_data['name']}")
    
    print("\nAll products updated successfully!")
    print(f"Images saved to: {os.path.join(settings.BASE_DIR, 'static', 'images', 'crackers')}")

if __name__ == '__main__':
    print("Starting BabyCrackers product import...")
    print("Make sure to add the actual product data to BABYCRACKERS_PRODUCTS list above\n")
    
    if len(BABYCRACKERS_PRODUCTS) == 1 and BABYCRACKERS_PRODUCTS[0]['name'] == 'Flower Pot':
        print("WARNING: Only example data found. Please add actual BabyCrackers product data.")
        print("To extract image URLs from BabyCrackers:")
        print("1. Open https://www.babycrackers.com/#/productlist in your browser")
        print("2. Press F12 to open Developer Tools")
        print("3. Go to Network tab and filter by 'Img'")
        print("4. Copy the image URLs and add them to this script")
    else:
        update_products()