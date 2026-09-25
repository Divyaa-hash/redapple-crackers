import sys
import io
from decimal import Decimal
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Update product prices from PDF price list'

    def handle(self, *args, **options):
        # Set UTF-8 encoding for stdout
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

        # Manual price mapping from PDF - focused on products in database
        price_mapping = {
            # Wala products
            '28 Chorsa': 26,
            '28 Giant': 26,
            '56 Giant': 58,
            '24 Deluxe': 66,
            '50 Deluxe': 110,
            '100 Deluxe': 220,
            '100 Wala': 176,
            '1000 Wala': 176,
            '1000 Wala Power': 352,
            '2000 Wala': 936,
            '2000 Wala Power': 1650,
            '5000 Wala': 1980,
            '5000 Wala Power': 3300,
            '10000 Wala': 3520,
            '10000 Wala Power': 7150,

            # Other products from PDF
            '7 Cm Electric Sparklers': 10,
            '7 Cm Colour Sparklers': 12,
            '7 Cm Green Sparklers': 14,
            '7 Cm Red Sparklers': 16,
            '10 Cm Electric Sparklers': 16,
            '10 Cm Colour Sparklers': 20,
            '10 Cm Green Sparklers': 22,
            '10 Cm Red Sparklers': 24,
            '15 Cm Electric Sparklers': 42,
            '15 Cm Colour Sparklers': 46,
            '15 Cm Green Sparklers': 54,
            '15 Cm Red Sparklers': 58,
            '50 Cm Electric Sparklers': 154,
            '50 Cm Colour Sparklers': 176,
            '50 cm 2 in 1 50': 198,
            'Rotating Sparklers': 242,
            'Pink Sparklers': 94,
            'Violet Sparklers': 94,
            'Super Deluxe 10 in 1': 84,
            'Royal Lamba 10 in 1': 182,
            'Royal Laptop 10 in 1': 260,
            'Roll Caps': 78,
            'Ring Cap': 12,
            'Snake Serphant Big': 40,
            'Ring Gun': 88,
            'Roll Gun': 88,
            '20 Item': 440,
            '30 Item': 660,
            '40 Item': 880,
            '50 Item': 1100,
            'Kids Pack': 3299,
            'Family Pack': 5499,
            'Thala Diwali Pack': 7699,
            'V.I.P Gold Pck': 10999,
        }

        updated_count = 0
        not_found_count = 0

        for product_name, price in price_mapping.items():
            try:
                # Try to find product by name (case-insensitive)
                products = Product.objects.filter(name__icontains=product_name)
                self.stdout.write(f"Searching for: {product_name} - Found {products.count()} matches")

                if products.exists():
                    for product in products:
                        # Update the price
                        product.regular_price = Decimal(str(price))
                        product.sale_price = Decimal(str(price * 0.2))  # 80% discount
                        product.save()
                        updated_count += 1
                        self.stdout.write(f"Updated: {product.name} - {price}")
                else:
                    not_found_count += 1
                    self.stdout.write(f"Not found: {product_name}")

            except Exception as e:
                self.stdout.write(f"Error updating {product_name}: {e}")

        self.stdout.write(f"\nSummary:")
        self.stdout.write(f"Updated: {updated_count} products")
        self.stdout.write(f"Not found: {not_found_count} products")
