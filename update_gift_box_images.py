import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Gift box products with new uploaded images
gift_boxes = {
    'Love Feast - 20 Item': 'images/crackers/20250902095402_yIeVn5U.png',
    'Turbo - 30 Item': 'images/crackers/20250902061911_Kq37n50.png',
    'Fun Special - 40 Item': 'images/crackers/20250902061858_QrekqRj.png',
    'Spectra Festive - 50 Item': 'images/crackers/20250822085410_1R4FqDa.png'
}

for product_name, image_path in gift_boxes.items():
    try:
        product = Product.objects.get(name=product_name)
        product.main_image = image_path
        product.save()
        print(f'Updated {product_name} with new image: {image_path}')
    except Product.DoesNotExist:
        print(f'Product not found: {product_name}')
