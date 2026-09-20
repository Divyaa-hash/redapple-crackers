import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Get all .webp files in static/images/crackers
image_dir = 'static/images/crackers'
if os.path.exists(image_dir):
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.webp')]
else:
    image_files = []

# Create mapping from product name to image file
image_mapping = {}

for image_file in image_files:
    # Remove .webp extension
    product_name = image_file.replace('.webp', '')
    image_mapping[product_name] = image_file

print(f'Found {len(image_mapping)} image files in {image_dir}')

# Update products with local image paths
updated_count = 0
for product in Product.objects.all():
    # Try exact match first
    if product.name in image_mapping:
        product.image_url = f'/static/images/crackers/{image_mapping[product.name]}'
        product.save(update_fields=['image_url'])
        updated_count += 1
        if updated_count <= 10:
            print(f'Updated {updated_count}: {product.name} -> {image_mapping[product.name]}')
    else:
        # Try partial match
        for img_name, img_file in image_mapping.items():
            if img_name.lower() in product.name.lower() or product.name.lower() in img_name.lower():
                product.image_url = f'/static/images/crackers/{img_file}'
                product.save(update_fields=['image_url'])
                updated_count += 1
                if updated_count <= 10:
                    print(f'Updated {updated_count}: {product.name} -> {img_file}')
                break

print(f'\nTotal updated: {updated_count} products')
print(f'Total products: {Product.objects.count()}')

# Save mapping for reference
with open('local_image_mapping.json', 'w') as f:
    json.dump(image_mapping, f, indent=2)
print('Saved mapping to local_image_mapping.json')
