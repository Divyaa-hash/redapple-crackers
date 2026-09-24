from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Assign actual Wala and special product images'

    def handle(self, *args, **options):
        # Mapping of product names to their image files
        wala_image_mapping = {
            '28 Chorsa': '28 Chorsa.jpg',
            '28 Giant': '28 Giant.jpg',
            '56 Giant': '56 Giant.jpg',
            '24 Deluxe': '24 Deluxe.jpg',
            '50 Deluxe': '50 Deluxe.jpg',
            '100 Deluxe': '100 Deluxe.jpg',
            '100 Wala': '100 Wala.jpg',
            '1000 Wala': '1000 Wala.jpg',
            '1000 Wala Power': '1000 Wala Power.jpg',
            '2000 Wala': '2000 Wala.jpg',
            '2000 Wala Power': '2000 Wala Power.jpg',
            '5000 Wala': '5000 Wala.jpg',
            '5000 Wala Power': '5000 Wala Power.jpg',
            '10000 Wala': '10000 Wala.jpg',
            '10000 Wala Power': '10000 Wala Power.jpg',
            '240 Multi Colour Fancy Shots': '240 Multi Colour Fancy Shots.jpg',
            'Tin Beer Fountain ( 1 Pc)': 'Tin Beer Fountain ( 1 Pc).jpg',
            'Zee Boomba ( 10 Pcs)': 'Zee Boomba ( 10 Pcs).jpg',
            'Electric Stone ( 10 Pcs)': 'Electric Stone ( 10 Pcs).jpg',
            'AK 47 Machine Gun': 'AK 47 Machine Gun.jpg',
            'Popcorn Crackling Star': 'Popcorn Crackling Star.jpg',
            'Star Show Popcorn Crackling': 'Star Show Popcorn Crackling.jpg',
            '3000 Combo Pack': '3000 Combo Pack.jpg',
            '4000 Combo Pack': '4000 Combo Pack.jpg',
            '5000 Combo Pack': '5000 Combo Pack.jpg',
            '7000 Combo Pack': '7000 Combo Pack.jpg',
        }

        products = Product.objects.filter(is_active=True)
        updated_products = []

        for product in products:
            if product.name in wala_image_mapping:
                image_file = wala_image_mapping[product.name]
                product.image_url = f'/static/images/crackers/{image_file}'
                product.save()
                updated_products.append(product.name)

        self.stdout.write(f'Updated {len(updated_products)} Wala products with actual images:')
        for name in updated_products:
            self.stdout.write(f'  - {name}')
