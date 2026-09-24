from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Assign logo image to Wala and special products'

    def handle(self, *args, **options):
        wala_keywords = ['Wala', 'Chorsa', 'Giant', '24 Deluxe', '50 Deluxe', '100 Deluxe', '240 Multi Colour Fancy Shots']

        products = Product.objects.filter(is_active=True)
        wala_products = []

        for product in products:
            if any(keyword in product.name for keyword in wala_keywords):
                product.image_url = '/static/images/crackers/logo.jpg'
                product.save()
                wala_products.append(product.name)

        self.stdout.write(f'Updated {len(wala_products)} products with logo image:')
        for name in wala_products:
            self.stdout.write(f'  - {name}')
