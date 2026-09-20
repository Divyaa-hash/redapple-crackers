import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Get products without image_url
products_without = Product.objects.filter(image_url__isnull=True) | Product.objects.filter(image_url='')

print(f'Products without image_url: {products_without.count()}')

# Assign placeholder image to all products without image_url
placeholder = 'images/crackers/placeholder.jpg'
updated = products_without.update(image_url=placeholder)

print(f'Updated {updated} products with placeholder image')

# Verify
remaining = Product.objects.filter(image_url__isnull=True).count() + Product.objects.filter(image_url='').count()
print(f'Remaining without image_url: {remaining}')
