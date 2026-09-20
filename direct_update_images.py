import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Load Cloudinary URL mapping
with open('cloudinary_url_mapping.json', 'r') as f:
    cloudinary_mapping = json.load(f)

# Update products with Cloudinary URLs in the image_url field
updated_count = 0
for product in Product.objects.all():
    if product.slug in cloudinary_mapping:
        # Set the image URL in the new image_url field
        product.image_url = cloudinary_mapping[product.slug]
        product.save(update_fields=['image_url'])
        updated_count += 1
        if updated_count <= 10:
            print(f'Updated {updated_count}: {product.name} -> {cloudinary_mapping[product.slug][:50]}...')

print(f'\nTotal updated: {updated_count} products')
