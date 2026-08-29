import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Gift box products
gift_boxes = {
    'Love Feast - 20 Item': 'images/crackers/20250902095402.png',
    'Turbo - 30 Item': 'images/crackers/20250902061911.png',
    'Fun Special - 40 Item': 'images/crackers/20250902061858.png',
    'Spectra Festive - 50 Item': 'images/crackers/20250822085410.png'
}

for product_name, image_path in gift_boxes.items():
    try:
        product = Product.objects.get(name=product_name)
        product.main_image = image_path
        product.save()
        print(f'Updated {product_name} with image: {image_path}')
    except Product.DoesNotExist:
        print(f'Product not found: {product_name}')
