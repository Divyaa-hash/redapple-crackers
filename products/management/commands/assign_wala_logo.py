from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Assign logo image to Wala and special products'

    def handle(self, *args, **options):
        logo_keywords = [
            'COLOUR CHANGING MAGIC STAR',
            'Stripped (vari) Bijili (100 Pcs)'
        ]

        products = Product.objects.filter(is_active=True)
        logo_products = []

        for product in products:
            if any(keyword in product.name for keyword in logo_keywords):
                product.image_url = '/static/images/crackers/logo.jpg'
                product.save()
                logo_products.append(product.name)

        self.stdout.write(f'Updated {len(logo_products)} products with logo image:')
        for name in logo_products:
            self.stdout.write(f'  - {name}')
