import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category
from decimal import Decimal

# Get or create gift box category
gift_category, _ = Category.objects.get_or_create(
    id=5,
    defaults={'name': 'Gift Boxes', 'slug': 'gift-boxes'}
)

# Gift box data from Excel with 10% markup
gift_boxes = [
    {
        'name': 'Love Feast - 20 Item',
        'sku': 'GB-LF-20',
        'price': Decimal('385'),  # 350 + 10%
        'original': Decimal('1750')
    },
    {
        'name': 'Turbo - 30 Item',
        'sku': 'GB-TB-30',
        'price': Decimal('605'),  # 550 + 10%
        'original': Decimal('2750')
    },
    {
        'name': 'Fun Special - 40 Item',
        'sku': 'GB-FS-40',
        'price': Decimal('825'),  # 750 + 10%
        'original': Decimal('3750')
    },
    {
        'name': 'Spectra Festive - 50 Item',
        'sku': 'GB-SF-50',
        'price': Decimal('1210'),  # 1100 + 10%
        'original': Decimal('5500')
    }
]

for gb in gift_boxes:
    product, created = Product.objects.get_or_create(
        sku=gb['sku'],
        defaults={
            'name': gb['name'],
            'slug': gb['sku'].lower(),
            'category': gift_category,
            'regular_price': gb['original'],
            'sale_price': gb['price'],
            'product_type': 'gift_box',
            'short_description': f'{gb["name"]} - Premium Gift Box',
            'description': f'{gb["name"]} - Premium Gift Box with assorted crackers',
            'stock': 50,
            'is_active': True
        }
    )
    print(f'{gb["name"]}: {"Created" if created else "Exists"}')
