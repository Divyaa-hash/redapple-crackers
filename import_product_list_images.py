"""
Script to remove all existing products and import new ones from product_list folder
"""

import os
import sys
import django
import shutil

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.core.files import File
from django.db import connection
from products.models import Product, Category, Brand

# Product categories mapping (you can customize this)
CATEGORIES = {
    'Fountains': 'Fountains',
    'Rockets': 'Rockets', 
    'Sparklers': 'Sparklers',
    'Crackers': 'Crackers',
    'Combos': 'Combos',
    'Gift Boxes': 'Combos',
}

# Default product data (you can customize prices and descriptions)
DEFAULT_PRODUCT_DATA = {
    'Fountains': {'price': 150, 'discount_price': 120, 'description': 'Premium fountain for celebrations'},
    'Rockets': {'price': 200, 'discount_price': 160, 'description': 'High-flying rocket with amazing effects'},
    'Sparklers': {'price': 50, 'discount_price': 40, 'description': 'Long-lasting sparklers for any occasion'},
    'Crackers': {'price': 100, 'discount_price': 80, 'description': 'Traditional crackers with loud sound'},
    'Combos': {'price': 500, 'discount_price': 400, 'description': 'Complete combo pack for celebrations'},
}

def delete_all_products():
    """Delete all existing products using direct SQL"""
    print("Deleting all existing products...")
    try:
        # Use raw SQL to avoid constraint issues
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM products_product")
            print("Deleted all existing products using direct SQL")
    except Exception as e:
        print(f"Error deleting products: {e}")
        # Try using Django ORM as fallback
        try:
            count = Product.objects.all().count()
            Product.objects.all().delete()
            print(f"Deleted {count} existing products using ORM")
        except Exception as e2:
            print(f"ORM deletion also failed: {e2}")
            print("Continuing with import...")

def import_product_images():
    """Import product images from product_list folder"""
    
    # Source folder
    source_folder = os.path.join(settings.BASE_DIR, 'product_list')
    
    # Destination folder
    dest_folder = os.path.join(settings.BASE_DIR, 'static', 'images', 'crackers')
    
    # Ensure destination folder exists
    os.makedirs(dest_folder, exist_ok=True)
    
    # Get all image files
    image_files = []
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_files.append(filename)
    
    print(f"Found {len(image_files)} image files in product_list folder")
    
    # Get or create brand
    brand, _ = Brand.objects.get_or_create(
        name='RedApple Premium',
        defaults={'slug': 'redapple-premium'}
    )
    
    # Distribute products across categories
    category_names = list(CATEGORIES.keys())
    products_created = 0
    products_updated = 0
    
    for i, filename in enumerate(image_files):
        # Determine category (round-robin distribution)
        category_name = category_names[i % len(category_names)]
        
        # Get or create category
        category, _ = Category.objects.get_or_create(
            name=category_name,
            defaults={'slug': category_name.lower().replace(' ', '-')}
        )
        
        # Copy image to static folder
        source_path = os.path.join(source_folder, filename)
        dest_path = os.path.join(dest_folder, filename)
        shutil.copy2(source_path, dest_path)
        
        # Generate product data
        product_num = i + 1
        product_name = f"{category_name} Product {product_num}"
        sku = f"RA-{category_name[:3].upper()}-{product_num:03d}"
        
        # Ensure unique slug
        base_slug = f"{category_name.lower().replace(' ', '-')}-product-{product_num}"
        unique_slug = base_slug
        counter = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Get default data for category
        default_data = DEFAULT_PRODUCT_DATA.get(category_name, DEFAULT_PRODUCT_DATA['Crackers'])
        
        # Create or update product (using get_or_create to handle duplicates)
        product, created = Product.objects.get_or_create(
            sku=sku,
            defaults={
                'name': product_name,
                'slug': unique_slug,
                'category': category,
                'brand': brand,
                'short_description': f"Premium {category_name} - Product {product_num}",
                'description': default_data['description'],
                'regular_price': default_data['price'],
                'sale_price': default_data['discount_price'],
                'stock': 50,
                'is_active': True,
                'is_featured': True,
                'is_new': True,
            }
        )
        
        # Update slug if product existed but slug was different
        if not created and product.slug != unique_slug:
            product.slug = unique_slug
            product.save()
        
        # Add/update image
        with open(dest_path, 'rb') as f:
            product.main_image.save(filename, File(f), save=True)
        
        if created:
            products_created += 1
            print(f"Created product {products_created}: {product_name}")
        else:
            products_updated += 1
            print(f"Updated product {products_updated}: {product_name}")
    
    total_products = products_created + products_updated
    print(f"\nSuccessfully processed {total_products} products ({products_created} created, {products_updated} updated)")
    print(f"Images saved to: {dest_folder}")

if __name__ == '__main__':
    print("Starting product import from product_list folder...")
    print("This will DELETE all existing products and add new ones\n")
    
    # Proceed with deletion and import
    print("Proceeding with deletion and import...")
    
    # Delete existing products
    delete_all_products()
    
    # Import new products
    import_product_images()
    
    print("\nProduct import completed successfully!")