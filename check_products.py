import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category, Brand

print(f'Gift box products with specific SKUs:')
gift_box_skus = ['GB-LF-20', 'GB-TB-30', 'GB-FS-40', 'GB-SF-50']
for sku in gift_box_skus:
    product = Product.objects.filter(sku=sku).first()
    if product:
        print(f'  {sku}: {product.name} - image={product.main_image}')
    else:
        print(f'  {sku}: Not found')

