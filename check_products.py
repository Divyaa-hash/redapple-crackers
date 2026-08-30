import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category, Brand

print(f'Total products in database: {Product.objects.count()}')
print(f'Active products: {Product.objects.filter(is_active=True).count()}')

print(f'\nGift box products with specific SKUs:')
gift_box_skus = ['GB-LF-20', 'GB-TB-30', 'GB-FS-40', 'GB-SF-50']
for sku in gift_box_skus:
    product = Product.objects.filter(sku=sku).first()
    if product:
        print(f'  {sku}: {product.name} - image={product.main_image}')
        # Check if image file exists
        img_path = f'media/{product.main_image}'
        if os.path.exists(img_path):
            print(f'    Image file exists: {img_path}')
        else:
            print(f'    Image file NOT found: {img_path}')
    else:
        print(f'  {sku}: Not found')

