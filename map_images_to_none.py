import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Get all products without image_url (including None and empty string)
products_without_image = Product.objects.filter(image_url__isnull=True) | Product.objects.filter(image_url='')

print(f'Products without image_url: {products_without_image.count()}')

# List static images
static_dir = 'static/images/crackers'
if os.path.exists(static_dir):
    static_images = os.listdir(static_dir)
    print(f'Static images available: {len(static_images)}')
else:
    static_images = []
    print('Static directory not found')

# Try to match products to static images with more flexible matching
updated = 0
for product in products_without_image:
    # Clean product name for matching
    product_name_clean = product.name.lower().strip()
    
    for img in static_images:
        img_name_clean = img.lower().replace('.webp', '').replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
        
        # Try exact match
        if product_name_clean == img_name_clean:
            product.image_url = f'images/crackers/{img}'
            product.save()
            updated += 1
            print(f'Exact match: {product.name} -> {img}')
            break
        
        # Try if product name is contained in image name
        if product_name_clean in img_name_clean and len(product_name_clean) > 5:
            product.image_url = f'images/crackers/{img}'
            product.save()
            updated += 1
            print(f'Partial match: {product.name} -> {img}')
            break
        
        # Try if image name is contained in product name
        if img_name_clean in product_name_clean and len(img_name_clean) > 5:
            product.image_url = f'images/crackers/{img}'
            product.save()
            updated += 1
            print(f'Reverse partial match: {product.name} -> {img}')
            break

print(f'\nUpdated {updated} products with image_url')
print(f'Remaining without image_url: {Product.objects.filter(image_url__isnull=True).count() + Product.objects.filter(image_url='').count()}')
