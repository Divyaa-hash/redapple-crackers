import sys
import io
import re
from decimal import Decimal
from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = 'Add missing products from Excel file with Red Apple logo'

    def handle(self, *args, **options):
        # Set UTF-8 encoding for stdout
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

        # Get categories
        categories = {c.name: c for c in Category.objects.all()}

        # Missing products with their categories, prices, and descriptions
        missing_products = [
            # Single Sound Crackers
            {'name': '2 1/2" Kuruvi', 'category': 'One sound crackers', 'price': 10, 'description': 'Single sound cracker'},
            {'name': '3 1/2" Lakshmi', 'category': 'One sound crackers', 'price': 14, 'description': 'Single sound cracker'},
            {'name': '4" Lakshmi', 'category': 'One sound crackers', 'price': 20, 'description': 'Single sound cracker'},
            {'name': '4" Lakshmi Deluxe', 'category': 'One sound crackers', 'price': 28, 'description': 'Single sound cracker'},
            {'name': '4" Lakshmi Mega Deluxe', 'category': 'One sound crackers', 'price': 34, 'description': 'Single sound cracker'},
            {'name': 'Two Sound Crackers', 'category': 'One sound crackers', 'price': 34, 'description': 'Two sound cracker'},
            {'name': 'Gold Lakshmi', 'category': 'One sound crackers', 'price': 40, 'description': 'Single sound cracker'},
            {'name': '5" Kamsan', 'category': 'One sound crackers', 'price': 62, 'description': 'Single sound cracker'},
            {'name': '6" Jallikattu / Lakshmi', 'category': 'One sound crackers', 'price': 72, 'description': 'Single sound cracker'},

            # Ground Chakkar
            {'name': 'Ground Chakkar Asoka (10 Pcs)', 'category': 'GROUND CHAKKARS', 'price': 50, 'description': 'Ground chakkar with special effect'},
            {'name': 'INF Spin Master Mini (10 Pcs)', 'category': 'GROUND CHAKKARS', 'price': 88, 'description': 'Spinning ground chakkar'},
            {'name': 'Sunflower Wheel (5 Pcs)', 'category': 'GROUND CHAKKARS', 'price': 116, 'description': 'Flower shaped ground chakkar'},
            {'name': 'Whistling Wheel (5 Pcs)', 'category': 'GROUND CHAKKARS', 'price': 122, 'description': 'Whistling ground chakkar'},
            {'name': 'Maska Chaska (5 Pcs)', 'category': 'GROUND CHAKKARS', 'price': 166, 'description': 'Special ground chakkar'},
            {'name': 'Rio Wheel (10 Pcs)', 'category': 'GROUND CHAKKARS', 'price': 242, 'description': 'Multi-color ground chakkar'},
            {'name': '4*4 Wheel (5 Pcs)', 'category': 'GROUND CHAKKARS', 'price': 176, 'description': '4x4 spinning wheel'},
            {'name': 'Tiddo', 'category': 'GROUND CHAKKARS', 'price': 132, 'description': 'Ground chakkar'},

            # Flower Pots
            {'name': 'Flower Pot Big (10 Pcs)', 'category': 'FLOWER POTS', 'price': 66, 'description': 'Large flower pot'},
            {'name': 'Flower Pot Special (10 Pcs)', 'category': 'FLOWER POTS', 'price': 84, 'description': 'Special flower pot'},
            {'name': 'Flower Pot Asoka (10 Pcs)', 'category': 'FLOWER POTS', 'price': 110, 'description': 'Asoka flower pot'},
            {'name': 'Flower Pot Deluxe (5 Pcs)', 'category': 'FLOWER POTS', 'price': 176, 'description': 'Deluxe flower pot'},
            {'name': 'Flower Pot Super Deluxe (2 Pcs)', 'category': 'FLOWER POTS', 'price': 122, 'description': 'Super deluxe flower pot'},
            {'name': 'Purple Cone', 'category': 'FLOWER POTS', 'price': 198, 'description': 'Purple colored flower pot'},
            {'name': 'Scooby Doo Tri Colour Fountain (5 Pcs)', 'category': 'FLOWER POTS', 'price': 198, 'description': 'Tri-color fountain'},
            {'name': 'Tri Colour Deluxe (3 Pcs)', 'category': 'FLOWER POTS', 'price': 232, 'description': 'Tri-color deluxe'},
            {'name': 'Pinky Pie (6 Pcs)', 'category': 'FLOWER POTS', 'price': 396, 'description': 'Pink colored flower pot'},
            {'name': 'Jelly Been Super (10 Pcs)', 'category': 'FLOWER POTS', 'price': 474, 'description': 'Super flower pot'},
            {'name': 'Violet Colour Koti (10 Pcs)', 'category': 'FLOWER POTS', 'price': 770, 'description': 'Violet colored flower pot'},

            # Twinkling Stars
            {'name': '1.5\' Twinkling Star', 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'price': 28, 'description': 'Small twinkling star'},
            {'name': '4\' Twinkling Star', 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'price': 66, 'description': 'Medium twinkling star'},

            # Candles
            {'name': '12" Silver Torch', 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'price': 78, 'description': 'Silver torch candle'},
            {'name': 'Candy Crush / Jelly Belly Candle', 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'price': 132, 'description': 'Colorful candle'},

            # Bijili
            {'name': 'Red Bijili Gold (100 Pcs)', 'category': 'BIJILI/ BOMB ITEMS', 'price': 40, 'description': 'Red sparklers'},
            {'name': 'Stripped Bijili (100 Pcs)', 'category': 'BIJILI/ BOMB ITEMS', 'price': 44, 'description': 'Stripped sparklers'},
            {'name': 'Bro Bijili (100 Pcs)', 'category': 'BIJILI/ BOMB ITEMS', 'price': 44, 'description': 'Bro sparklers'},
            {'name': 'Layz (Red, Green, Silver, Gold, R&G)', 'category': 'BIJILI/ BOMB ITEMS', 'price': 44, 'description': 'Multi-color sparklers'},
            {'name': 'Kurkur (Red, Green, Silver, Gold, R&G)', 'category': 'BIJILI/ BOMB ITEMS', 'price': 44, 'description': 'Multi-color sparklers'},

            # Night Fountain
            {'name': 'Asrafi Big (5 Pcs)', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 176, 'description': 'Asrafi fountain'},
            {'name': 'Asrafi Small (5 Pcs)', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Small asrafi fountain'},
            {'name': 'Bro (New)', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Bro fountain'},
            {'name': 'Kurkure (New)', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Kurkure fountain'},
            {'name': 'Hungry Colours (New)', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Colorful fountain'},
            {'name': 'Binge Pop', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Pop fountain'},
            {'name': 'Kickerzzz', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Kicker fountain'},
            {'name': 'H2O', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Water fountain'},
            {'name': 'Silver Rain (5 Pcs)', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Silver rain fountain'},
            {'name': 'Nebula (5 Pcs)', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Nebula fountain'},
            {'name': 'Fire Feather (5 Pcs)', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Fire feather fountain'},
            {'name': 'Mini Peacock', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Mini peacock fountain'},
            {'name': 'Magical Peacock (5 Face)', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Magical peacock'},
            {'name': 'Belly Belly Peacock (3 Face)', 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'price': 128, 'description': 'Belly peacock'},

            # New Arrivals
            {'name': 'Money In The Bank', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Money bank cracker'},
            {'name': 'Sound Marriage', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Marriage sound cracker'},
            {'name': 'Little Dove', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Dove cracker'},
            {'name': '90 Watts', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Sound cracker'},
            {'name': 'Shinchan', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Shinchan cracker'},
            {'name': '900 CC', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'CC sound cracker'},
            {'name': 'Water Queen', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Water fountain'},
            {'name': '20-20 Fountain', 'category': 'NEW ARRIVALS', 'price': 128, 'description': '20-20 fountain'},
            {'name': 'Pistal 5G', 'category': 'NEW ARRIVALS', 'price': 128, 'description': '5G cracker'},
            {'name': 'Pop Corn New', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Pop corn cracker'},
            {'name': 'Popoye (5 Pcs)', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Popoye cracker'},
            {'name': 'Party Canon / Magic Show (2 Pcs)', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Party canon'},
            {'name': 'Power Puff Girls (5 Pcs)', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Power puff girls'},
            {'name': 'Lemon Tree 2 in 1', 'category': 'NEW ARRIVALS', 'price': 128, 'description': '2 in 1 fountain'},
            {'name': 'Hybrid 2 in 1 New', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Hybrid 2 in 1'},
            {'name': 'Jungle Series 2 in 1 New', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Jungle 2 in 1'},
            {'name': 'Motu Patlu 2 in 1', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Motu Patlu 2 in 1'},
            {'name': 'Mumbo Jumbo 2 in 1', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Mumbo Jumbo 2 in 1'},
            {'name': 'Mad Angles 3 in 1', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Mad angles 3 in 1'},
            {'name': 'Helo Panda 5 in 1', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Panda 5 in 1'},
            {'name': 'Arjun Tank 3 in 1 New', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Arjun tank 3 in 1'},
            {'name': 'Water Melon 3 in 1 New', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Water melon 3 in 1'},
            {'name': 'Sword', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Sword cracker'},
            {'name': 'Smiley Mushroom', 'category': 'NEW ARRIVALS', 'price': 128, 'description': 'Mushroom cracker'},

            # Bombs
            {'name': 'Jolly Bobby Asok Brand', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Jolly Bobby bomb'},
            {'name': 'Taka Tak Crackling (3 Pcs)', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Crackling bomb'},
            {'name': 'Vajra - Handshot', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Handshot bomb'},
            {'name': 'Hydro Bomb Green (10 Pcs)', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Green hydro bomb'},
            {'name': 'King Of King Green (10 Pcs)', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Green king bomb'},
            {'name': 'Agni Bomb', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Agni bomb'},
            {'name': 'Digital Bomb (10 Pcs)', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Digital bomb'},
            {'name': 'Joker Bomb - 1/4 kg', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Joker bomb'},
            {'name': 'Mega Paper Bomb - 1/2 kg', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Mega paper bomb'},
            {'name': 'Bada Paper Bomb - 1 kg', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Large paper bomb'},
            {'name': 'Avatar 2', 'category': 'BIJILI/ BOMB ITEMS', 'price': 128, 'description': 'Avatar bomb'},

            # Wala
            {'name': '1H Wala', 'category': 'Wala', 'price': 128, 'description': '1 hour wala'},
            {'name': '1k Wala', 'category': 'Wala', 'price': 128, 'description': '1000 shots wala'},
            {'name': '2k Wala', 'category': 'Wala', 'price': 128, 'description': '2000 shots wala'},
            {'name': '5k Wala', 'category': 'Wala', 'price': 128, 'description': '5000 shots wala'},
            {'name': '10k Wala', 'category': 'Wala', 'price': 128, 'description': '10000 shots wala'},
            {'name': '1k Wala Spl', 'category': 'Wala', 'price': 128, 'description': '1000 shots special wala'},
            {'name': '2k Wala Spl', 'category': 'Wala', 'price': 128, 'description': '2000 shots special wala'},
            {'name': '5k Wala Spl', 'category': 'Wala', 'price': 128, 'description': '5000 shots special wala'},
            {'name': '10k Wala Spl', 'category': 'Wala', 'price': 128, 'description': '10000 shots special wala'},

            # Rockets
            {'name': 'Colour Rocket', 'category': 'SKY ROCKETS', 'price': 128, 'description': 'Color rocket'},
            {'name': 'Lunik Express (10 Pcs)', 'category': 'SKY ROCKETS', 'price': 128, 'description': 'Lunik rocket'},

            # Sky Shots
            {'name': 'Chotta Fancy (2 Pcs)', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': 'Chotta fancy'},
            {'name': 'Sevenshot (5 Pcs)', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': 'Seven shot'},
            {'name': 'Coco Loco (2 Pcs)', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': 'Coco loco'},
            {'name': 'Dup Tip (3 Pcs)', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': 'Dup tip'},
            {'name': 'Army Force (5 Pcs)', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': 'Army force'},
            {'name': 'Beast Show (5 Pcs)', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': 'Beast show'},
            {'name': 'Seeti Maar 30 Shot Missiles', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': '30 shot missiles'},
            {'name': 'Avengers (5 Pcs)', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': 'Avengers'},
            {'name': '2" Fancy', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': '2 inch fancy'},
            {'name': '2" Fancy (3 Pcs)', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': '2 inch fancy'},
            {'name': '2" Violet Fancy', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': 'Violet fancy'},
            {'name': '2" Pink Fancy', 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'price': 128, 'description': 'Pink fancy'},

            # Night Fancy
            {'name': 'Peacock Feather (5 Pcs)', 'category': 'NIGHT FANCY CELEBRATION', 'price': 128, 'description': 'Peacock feather'},
            {'name': 'Wanted Gun (5 Pcs)', 'category': 'NIGHT FANCY CELEBRATION', 'price': 128, 'description': 'Wanted gun'},
            {'name': 'Dancing Butterfly (10 Pcs)', 'category': 'NIGHT FANCY CELEBRATION', 'price': 128, 'description': 'Dancing butterfly'},
        ]

        self.stdout.write(f"Adding {len(missing_products)} missing products")

        added_count = 0
        skipped_count = 0
        error_count = 0

        for product_data in missing_products:
            try:
                # Check if product already exists
                if Product.objects.filter(name__iexact=product_data['name']).exists():
                    skipped_count += 1
                    self.stdout.write(f"Skipped (already exists): {product_data['name']}")
                    continue

                # Get category
                category = categories.get(product_data['category'])
                if not category:
                    error_count += 1
                    self.stdout.write(f"Error: Category not found for {product_data['name']}: {product_data['category']}")
                    continue

                # Create product
                # Generate unique slug
                slug = product_data['name'].lower()
                slug = re.sub(r'[^a-z0-9\s-]', '', slug)  # Remove special chars
                slug = re.sub(r'[-\s]+', '-', slug)  # Replace spaces/hyphens with single hyphen
                slug = slug[:200]  # Truncate to 200 chars

                # Make slug unique
                base_slug = slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                # Generate unique SKU
                sku = product_data['name'][:45]  # Leave room for counter
                base_sku = sku
                sku_counter = 1
                while Product.objects.filter(sku=sku).exists():
                    sku = f"{base_sku[:45]}-{sku_counter}"
                    sku_counter += 1

                product = Product.objects.create(
                    name=product_data['name'],
                    category=category,
                    sku=sku,
                    regular_price=Decimal(str(product_data['price'])),
                    sale_price=Decimal(str(product_data['price'] * 0.2)),  # 80% discount
                    short_description=product_data['description'],
                    description=product_data['description'],
                    pieces=1,  # Default pieces
                    stock=100,
                    is_active=True,
                    image_url='images/crackers/logo.jpg',  # Red Apple logo
                    slug=slug
                )

                added_count += 1
                self.stdout.write(f"Added: {product_data['name']} - {product_data['price']}")

            except Exception as e:
                error_count += 1
                self.stdout.write(f"Error adding {product_data['name']}: {e}")

        self.stdout.write(f"\nSummary:")
        self.stdout.write(f"Added: {added_count} products")
        self.stdout.write(f"Skipped: {skipped_count} products (already exist)")
        self.stdout.write(f"Errors: {error_count} products")
