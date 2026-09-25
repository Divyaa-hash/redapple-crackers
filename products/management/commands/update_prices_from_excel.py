import csv
import sys
import io
from decimal import Decimal
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Update product prices from Excel price list CSV'

    def handle(self, *args, **options):
        # Set UTF-8 encoding for stdout
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

        # Manual price mapping based on Excel file and actual database names
        price_mapping = {
            # Single Sound Crackers
            '2 3/4 \' Kuruvi': 10,
            '3 1/2 Lakshmi': 14,
            '4 \' Lakshmi': 20,
            '4 \' Lakshmi Deluxe': 28,
            '5\' Kumki Deluxe': 34,
            'Golden Lakshmi Deluxe': 40,
            'Deluxe Jallikattu': 50,
            'Two Sound Colour': 34,

            # Ground Chakkar
            'Ground Chakkar Big ( 25 Pcs)': 40,
            'Ground Chakkar Asoka (10 Pcs)': 50,
            'Ground Chakkar Special (10 Pcs)': 72,
            'Ground Chakkar Deluxe ( 10 Pcs)': 144,
            'Ground Chakkar Small(10 Pcs)': 86,

            # Fancy Ground Chakkar
            'WIRE CHAKKAR ( 10 PCS)': 176,
            'Lotus Wheel 4x4 ( 5 Pcs)': 176,

            # Flower Pots
            'Flower Pots Ashoka (10 Pcs)': 110,
            'Flower Pots Big (10 Pcs)': 66,
            'Flower Pots Colour Koti (10 Pcs)': 198,
            'Flower pots Colour Koti Deluxe(10 Pcs)': 352,
            'Flower Pots Small ( 10 Pcs)': 96,
            'Flower Pots Special (10 Pcs)': 84,
            'Flower pots Multi Colour Giant (10 Pcs)': 450,
            'Gypsy Colour Flower pots (5Pcs)': 176,
            'Jumbo Super Deluxe ( 10 pcs)': 440,
            'Mega Tri Colour Fountain ( 5 pcs)': 320,
            'Motu Patlu Tri Colour (5 Pcs)': 220,
            'Special Colour Koti (10 Pcs)': 250,

            # Sparklers
            '7 Cm Colour Sparklers': 20,
            '7 Cm Electric Sparklers': 10,
            '7 Cm Green Sparklers': 14,
            '7 Cm Red Sparklers': 16,
            '10 Cm Colour Sparklers': 40,
            '10 Cm Electric Sparklers': 18,
            '10 Cm Green Sparklers': 22,
            '10 Cm Red Sparklers': 24,
            '12 Cm Colour Sparklers': 46,
            '12 Cm Electric Sparklers': 28,
            '12 Cm Green Sparklers': 34,
            '12 Cm Red Sparklers': 36,
            '15 Cm Colour Sparklers': 92,
            '15 Cm Electric Sparklers': 44,
            '15 Cm Green Sparklers': 48,
            '15 Cm Red Sparklers': 50,
            '30 Cm Colour Sparklers': 92,
            '30 Cm Electric Sparklers': 44,
            '30 Cm Green Sparklers': 48,
            '30 Cm Red Sparklers': 50,
            '50 Cm Colour Sparklers': 350,
            '50 Cm Electric Sparklers': 165,

            # Pencil and Twinkling Stars
            '10 \' Pencil ( 10 Pcs)': 68,
            '1 1/2\' (Sattai) Twingling Star (10 Pcs)': 28,
            '4\' (Sattai) Twingling Star (10 Pcs)': 74,
            '7 \' Pencil ( 10 Pcs)': 32,
            'Popcorn Pencil (5 Pcs)': 230,
            'Rainbow flash Pencil (5 Pcs)': 150,
            'Sivakasi special Candle Pencil (2 Pcs)': 200,
            'Ultra Torch pencil (3 Pcs)': 72,

            # Wala
            '28 Chorsa': 26,
            '28 Giant': 26,
            '56 Giant': 58,
            '24 Deluxe': 66,
            '50 Deluxe': 110,
            '100 Deluxe': 220,
            '100 Wala': 90,
            '1000 Wala': 170,
            '1000 Wala Power': 320,
            '2000 Wala': 1750,
            '2000 Wala Power': 3200,
            '5000 Wala': 4500,
            '5000 Wala Power': 7500,
            '10000 Wala': 9000,
            '10000 Wala Power': 15000,

            # Rockets
            'Rocket bomb ( 10 Pcs)': 62,
            'Whistling Rocket (10 Pcs)': 99,

            # Night Fancy Celebration
            'Bada Peacock': 462,
            'Colour Bambaram red/green ( 10 Pcs)': 110,
            'Colour Changing Butterfly ( 10 Pcs)': 130,
            'Colour Smoke Candle Celebration big (3 Pcs)': 190,
            'Grizz colour fountain': 75,
            'Helicopter ( 5 pcs)': 110,
            'Lotus Wheel 4x4 ( 5 Pcs)': 176,
            'MAD MAX': 74,
            'Old is Gold Colour Olai Vedi ( 25 Pcs )': 100,
            'Peacock Fancy': 170,
            'Photo Flash ( 5 Pcs)': 78,
            'Shooting Gun Crackling ( 5 Pcs)': 112,

            # Night Fountain Celebrations
            '2\' Sun Feast Colour Fountain ( 5 Pcs)': 170,
            '3\' Red Sun/ ICE MAGIC Fountain': 220,
            '4\' Angry Bird Shower': 60,
            'Apple / Pogo Shower Boom ( 5 pcs)': 225,
            'Asrafi ( 5 Pcs )': 64,
            'Cocktail Dancing WALA EFECT (3 Pcs)': 175,
            'Colour Rain ( 5 Pcs)': 110,
            'Disco Shower ( 5 Pcs)': 145,
            'Feather pop Shower ( 5 Pcs)': 135,
            'Ganga Zamuna Shower( 5 Pcs)': 98,
            'Golden Shower ( 5 Pcs)': 70,
            'Mega Siren ( 3 Pcs )': 99,
            'Mini Siren( 5 pcs)': 95,
            'Tin Beer Fountain ( 1 Pc)': 94,
            'Water Falls Fountain': 225,

            # Night Fancy Celebration (Sky Shots)
            '2\' Fancy Pipe Out': 120,
            '2\' Fancy Pipe Out ( 3 Pcs )': 290,
            '3½\' Fancy Pipe Out': 160,
            '3½\' Fancy Pipe Out ( 2 Pcs)': 325,
            '3\' Fancy Pipe Out': 120,
            '4½\' Fancy Pipe Out ( 2 Pcs )': 425,
            '4 \' Fancy Pipe Out': 210,
            '4\' Fancy Pipe Out ( 2 Pcs )': 395,
            '5 \' Mega Fancy Pipe Out ( 2 Pcs )': 475,
            '7 Color Shots ( 5 Pcs)': 65,
            'Chotta Pipe Multi Colour out': 46,
            'Colour Celebration (5 pcs)': 120,
            'Sky Shot Out ( 5 Pcs)': 105,

            # New Arrivals
            '90 Digital Cracker ( 3 Pcs)': 170,
            'AK 47 Machine Gun': 230,
            'Bat & Smoke Ball': 120,
            'CYLINDER BOMB': 80,
            'Dancing Umberla': 110,
            'Emu Egg (2 Pcs)': 83,
            'GenZ Mobile Shower': 100,
            'ICE CONE FALLS (2 Pcs)': 140,
            'INFINITY STAR CRACKLING FOUNTAIN (3 Pcs)': 195,
            'Jungle Beat Sound ( 5 Pcs)': 75,
            'KADHAYUTHAM FALLS': 95,
            'Lolly Pop Flash Stick (5 Pcs)': 120,
            'Magic Digital Sound Wala': 110,
            'Selfi Stick (5 Pcs)': 80,
            'Shin chan (5 Pcs)': 75,
            'SPARKLING SWARD': 70,
            'Star Show Popcorn Crackling': 110,
            'WIRE CHAKKAR ( 10 PCS)': 110,

            # Repeating Multi Colour Fancy Shots
            '10x10 IPL Set out': 3900,
            '120 Multi Colour Fancy Shots': 820,
            '12 Multi Colour Fancy Shots': 110,
            '12 Rider Fancy Shots': 80,
            '20x 2.5\' Set out Grand Fancy': 2700,
            '240 Multi Colour Fancy Shots': 1600,
            '25 Multi Rider fancy Shots': 140,
            '30 Special Multi Colour Fancy Shots': 225,
            '30x 2.5\' Set out Grand Fancy': 1800,
            '60 Multi Colour Fancy Shots': 420,

            # Snake and Cartoon
            '3 In 1 Colour fog stick (3 Pcs)': 15,
            'Block Perpant (50 Tablets)': 14,
            'Cartoon Pots (10 Pcs)': 25,
            'Electric Stone ( 10 Pcs)': 8,
            'Kit Kat ( 10 Pcs)': 17,
            'Snake Cartoon ( 5 Pcs)': 15,
            'Zee Boomba ( 10 Pcs)': 7.5,

            # Gift Boxes
            'Family Gift Box (21 Items)': 35,
            'Family Gift Box (25 Items)': 45,
            'Family Gift Box ( 30 Items)': 55,
            'Family Gift Box ( 35 Items)': 65,
            'Family Gift Box (40 Items )': 75,
            'Family Gift Box (50 Items)': 95,
            'Family Gift Box (60 Items)': 115,
            'Premium Gift box': 80,

            # Bombs
            '555 Bomb ( 10 Pcs)': 150,
            'Atom Bomb (10 Pcs)': 75,
            'Bullet Bomb (10 Pcs)': 36,
            'Classic Bomb ( 10 Pcs)': 61,
            'Digital Deluxe Bomb (10 Pcs)': 125,
            'Dinoser Bomb ( 10 Pcs)': 112,
            'Hydro Bomb ( 10 Pcs)': 47,
            'King of King Bomb (10 Pcs)': 62,
            'Red Bijili ( 100 pcs)': 17,
            'Red Bijili ( 50 pcs)': 7.5,
            'Stripped (vari) Bijili (100 Pcs)': 20,

            # Children's Roll Cap/Gun
            'Medium Size Gun': 10,
            'Mega Gun': 17,
            'Ring Cap Gun': 10,
            'Roll Cab': 7.5,
            'Small Size Gun': 7,

            # Colour Matches
            'Deluxe Match ( 100 Sticks)': 80,
            'Hero Match (100 Sticks)': 150,
            'Mega Laptop Match ( 100 Sticks)': 125,
            'VIP Top 10 Laptop Match (100 Sticks)': 145,

            # Combo Packs
            '3000 Combo Pack': 600,
            '4000 Combo Pack': 800,
            '5000 Combo Pack': 1000,
            '7000 Combo Pack': 1400,

            # Laddu Fountain
            'Chun Mun Laddu (5 Pcs)': 110,
            'COLOUR CHANGING MAGIC STAR (5Pcs)': 225,
            'Mega Deluxe Fountain (4 Pcs )': 300,

            # Paper Bomb
            'Adiyal Paper Bomb ½ Kg': 96,
            'Adiyal Paper Bomb ¼ Kg': 48,
            'Adiyal Paper Bomb 1 Kg': 95,
            'Avadhar Paper Bomb (10 Pcs)': 125,
            'Clolour Paper Vedi (5 Pcs)': 50,
            'Crorepathy Paper Bomb (2 Pcs)': 120,
            'Money Bank (3 Pcs)': 75,

            # Special Series Fancy Sky Shots
            '4.5\' Wow Series Fancy Pipe Out': 237,
            'Digital Crackling Star': 195,
            'Double Colour Ball Out': 212,
            'Nayagara Falls Out': 185,
            'Seven Step Fancy Out': 225,
            'Trible ball Fancy Pipe Out': 120,
            'Zumba dance sky out (6Pcs)': 110,
        }

        self.stdout.write(f"Loaded {len(price_mapping)} product prices from Excel")

        # Update prices in database
        updated_count = 0
        not_found_count = 0
        error_count = 0

        for product_name, price in price_mapping.items():
            try:
                # Try to find product by name (case-insensitive)
                products = Product.objects.filter(name__iexact=product_name, is_active=True)

                if products.exists():
                    for product in products:
                        # Update the price
                        # Excel price is the SELLING price (after 80% discount)
                        # So regular_price should be price / 0.2 (to show 80% discount)
                        product.sale_price = Decimal(str(price))
                        product.regular_price = Decimal(str(price / 0.2))  # MRP for 80% discount
                        product.save()
                        updated_count += 1
                        self.stdout.write(f"Updated: {product.name} - sale={price}, regular={price/0.2}")
                else:
                    not_found_count += 1
                    self.stdout.write(f"Not found: {product_name}")

            except Exception as e:
                error_count += 1
                self.stdout.write(f"Error updating {product_name}: {e}")

        self.stdout.write(f"\nSummary:")
        self.stdout.write(f"Updated: {updated_count} products")
        self.stdout.write(f"Not found: {not_found_count} products")
        self.stdout.write(f"Errors: {error_count} products")
