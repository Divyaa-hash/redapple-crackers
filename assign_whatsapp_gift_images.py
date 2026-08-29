import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Gift box products with WhatsApp images
gift_boxes = {
    'Love Feast - 20 Item': 'images/crackers/gift_box_1.jpg',
    'Turbo - 30 Item': 'images/crackers/gift_box_2.jpg',
    'Fun Special - 40 Item': 'images/crackers/gift_box_3.jpg',
    'Spectra Festive - 50 Item': 'images/crackers/gift_box_4.jpg'
}

for product_name, image_path in gift_boxes.items():
    try:
        product = Product.objects.get(name=product_name)
        product.main_image = image_path
        product.save()
        print(f'Updated {product_name} with WhatsApp image: {image_path}')
    except Product.DoesNotExist:
        print(f'Product not found: {product_name}')
