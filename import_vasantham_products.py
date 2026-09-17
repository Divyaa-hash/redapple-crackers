import os
import django
import random
import string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product
from decimal import Decimal

# Product data from vasanthamcrackersworld.com
product_data = {
    "One sound crackers": [
        ("4' Lakshmi", 180, 18, "PKT"),
        ("3 1/2 Lakshmi", 140, 14, "PKT"),
        ("4' Lakshmi Deluxe", 300, 30, "PKT"),
        ("Golden Lakshmi Deluxe", 340, 34, "PKT"),
        ("5' Kumki Deluxe", 440, 44, "PKT"),
        ("Deluxe Jallikattu", 500, 50, "PKT"),
        ("Two Sound Colour", 440, 44, "PKT"),
        ("2 3/4' Kuruvi", 80, 8, "PKT"),
    ],
    "PENCIL and (Sattai) TWINGLING STARS": [
        ("1 1/2' (Sattai) Twingling Star (10 Pcs)", 280, 28, "BOX"),
        ("4' (Sattai) Twingling Star (10 Pcs)", 740, 74, "BOX"),
        ("7' Pencil (10 Pcs)", 320, 32, "BOX"),
        ("10' Pencil (10 Pcs)", 680, 68, "BOX"),
        ("Ultra Torch pencil (3 Pcs)", 720, 72, "BOX"),
        ("Rainbow flash Pencil (5 Pcs)", 1500, 150, "BOX"),
        ("Sivakasi special Candle Pencil (2 Pcs)", 2000, 200, "BOX"),
        ("Popcorn Pencil (5 Pcs)", 2300, 230, "BOX"),
    ],
    "SPARKLERS": [
        ("7 Cm Electric Sparklers", 100, 10, "BOX"),
        ("7 Cm Colour Sparklers", 120, 12, "BOX"),
        ("7 Cm Green Sparklers", 140, 14, "BOX"),
        ("7 Cm Red Sparklers", 160, 16, "BOX"),
        ("10 Cm Electric Sparklers", 180, 18, "BOX"),
        ("10 Cm Colour Sparklers", 200, 20, "BOX"),
        ("10 Cm Green Sparklers", 220, 22, "BOX"),
        ("10 Cm Red Sparklers", 240, 24, "BOX"),
        ("12 Cm Electric Sparklers", 280, 28, "BOX"),
        ("12 Cm Colour Sparklers", 300, 30, "BOX"),
        ("12 Cm Green Sparklers", 340, 34, "BOX"),
        ("12 Cm Red Sparklers", 360, 36, "BOX"),
        ("15 Cm Electric Sparklers", 440, 44, "BOX"),
        ("15 Cm Colour Sparklers", 460, 46, "BOX"),
        ("15 Cm Green Sparklers", 480, 48, "BOX"),
        ("15 Cm Red Sparklers", 500, 50, "BOX"),
        ("30 Cm Electric Sparklers", 440, 44, "BOX"),
        ("30 Cm Colour Sparklers", 460, 46, "BOX"),
        ("30 Cm Green Sparklers", 480, 48, "BOX"),
        ("30 Cm Red Sparklers", 500, 50, "BOX"),
        ("50 Cm Electric Sparklers", 1650, 165, "BOX"),
        ("50 Cm Colour Sparklers", 1750, 175, "BOX"),
    ],
    "FLOWER POTS": [
        ("Flower Pots Small (10 Pcs)", 480, 48, "BOX"),
        ("Flower Pots Big (10 Pcs)", 780, 78, "BOX"),
        ("Flower Pots Special (10 Pcs)", 1200, 120, "BOX"),
        ("Flower Pots Ashoka (10 Pcs)", 1500, 150, "BOX"),
        ("Flower Pots Colour Koti (10 Pcs)", 2100, 210, "BOX"),
        ("Special Colour Koti (10 Pcs)", 2500, 250, "BOX"),
        ("Flower pots Colour Koti Deluxe (10 Pcs)", 3900, 390, "BOX"),
        ("Motu Patlu Tri Colour (5 Pcs)", 2200, 220, "BOX"),
        ("Mega Tri Colour Fountain (5 pcs)", 3200, 320, "BOX"),
        ("Jumbo Super Deluxe (10 pcs)", 4400, 440, "BOX"),
        ("Flower pots Multi Colour Giant (10 Pcs)", 4500, 450, "BOX"),
        ("Gypsy Colour Flower pots (5Pcs)", 1900, 190, "BOX"),
    ],
    "GROUND CHAKKARS": [
        ("Ground Chakkar Small (10 Pcs)", 430, 43, "BOX"),
        ("Ground Chakkar Big (25 Pcs)", 1100, 110, "BOX"),
        ("Ground Chakkar Ashoka (10 Pcs)", 800, 80, "BOX"),
        ("Ground Chakkar Special (10 Pcs)", 1200, 120, "BOX"),
        ("Ground Chakkar Deluxe (10 Pcs)", 1600, 160, "BOX"),
        ("Disco Wheel (5 Pcs)", 700, 70, "BOX"),
        ("Whizzling Wheel (5 Pcs)", 1500, 150, "BOX"),
        ("Chakkar Spinner Deluxe (10Pcs)", 1800, 180, "BOX"),
    ],
    "SKY ROCKETS": [
        ("Baby Rocket (10 Pcs)", 350, 35, "BOX"),
        ("Rocket bomb (10 Pcs)", 800, 80, "BOX"),
        ("Lunix /2 Sound Rocket (10 Pcs)", 1500, 150, "BOX"),
        ("Whistling Rocket (10 Pcs)", 1700, 170, "BOX"),
    ],
    "BIJILI/ BOMB ITEMS": [
        ("Red Bijili (50 pcs)", 150, 15, "PKT"),
        ("Red Bijili (100 pcs)", 350, 35, "PKT"),
        ("Bullet Bomb (10 Pcs)", 360, 36, "BOX"),
        ("Atom Bomb (10 Pcs)", 750, 75, "BOX"),
        ("Hydro Bomb (10 Pcs)", 950, 95, "BOX"),
        ("King of King Bomb (10 Pcs)", 1250, 125, "BOX"),
        ("Classic Bomb (10 Pcs)", 1500, 150, "BOX"),
        ("Dinoser Bomb (10 Pcs)", 2250, 225, "BOX"),
        ("555 Bomb (10 Pcs)", 1500, 150, "BOX"),
        ("Digital Deluxe Bomb (10 Pcs)", 2500, 250, "BOX"),
        ("Stripped (vari) Bijili (100 Pcs)", 400, 40, "PKT"),
    ],
    "PAPER BOMB": [
        ("Adiyal Paper Bomb ¼ Kg", 480, 48, "1PIECE"),
        ("Adiyal Paper Bomb ½ Kg", 960, 96, "1PIECE"),
        ("Clolour Paper Vedi (5 Pcs)", 1000, 100, "1PKT"),
        ("Avadhar Paper Bomb (10 Pcs)", 2500, 250, "BOX"),
        ("Crorepathy Paper Bomb (2 Pcs)", 2400, 240, "BOX"),
        ("Adiyal Paper Bomb 1 Kg", 1900, 190, "1PIECE"),
        ("Money Bank (3 Pcs)", 1500, 150, "BOX"),
    ],
    "Wala": [
        ("28 Chorsa", 180, 18, "BOX"),
        ("28 Giant", 300, 30, "BOX"),
        ("56 Giant", 500, 50, "BOX"),
        ("24 Deluxe", 600, 60, "PKT"),
        ("50 Deluxe", 1300, 130, "PKT"),
        ("100 Deluxe", 2600, 260, "BOX"),
        ("100 Wala", 450, 45, "BOX"),
        ("1000 Wala", 1700, 170, "BOX"),
        ("1000 Wala Power", 3200, 320, "BOX"),
        ("2000 Wala", 3500, 350, "BOX"),
        ("2000 Wala Power", 6400, 640, "BOX"),
        ("5000 Wala", 9000, 900, "BOX"),
        ("5000 Wala Power", 15000, 1500, "BOX"),
        ("10000 Wala", 18000, 1800, "BOX"),
        ("10000 Wala Power", 30000, 3000, "BOX"),
    ],
    "SKY NIGHT FANCY CELEBRATIONS": [
        ("Chotta Pipe Multi Colour out", 460, 46, "1Piece"),
        ("7 Color Shots (5 Pcs)", 1300, 130, "BOX"),
        ("Sky Shot Out (5 Pcs)", 2100, 210, "BOX"),
        ("Colour Celebration (5 pcs)", 2400, 240, "BOX"),
        ("2' Fancy Pipe Out", 1200, 120, "1piece"),
        ("2' Fancy Pipe Out (3 Pcs)", 2900, 290, "BOX"),
        ("3' Fancy Pipe Out", 2400, 240, "1piece"),
        ("3½' Fancy Pipe Out", 3200, 320, "1piece"),
        ("3½' Fancy Pipe Out (2 Pcs)", 6500, 650, "BOX"),
        ("4' Fancy Pipe Out", 4200, 420, "1Piece"),
        ("4' Fancy Pipe Out (2 Pcs)", 7900, 790, "BOX"),
        ("4½' Fancy Pipe Out (2 Pcs)", 8500, 850, "BOX"),
        ("5' Mega Fancy Pipe Out (2 Pcs)", 9500, 950, "BOX"),
    ],
    "REPEATING MULTI COLOUR FANCY SHOTS": [
        ("12 Rider Fancy Shots", 1600, 160, "BOX"),
        ("12 Multi Colour Fancy Shots", 2200, 220, "BOX"),
        ("30 Multi Colour Fancy Shots", 3800, 380, "BOX"),
        ("30 Special Multi Colour Fancy Shots", 4500, 450, "BOX"),
        ("60 Multi Colour Fancy Shots", 8400, 840, "BOX"),
        ("120 Multi Colour Fancy Shots", 16400, 1640, "BOX"),
        ("20x 2.5' Set out Grand Fancy", 27000, 2700, "BOX"),
        ("30x 2.5' Set out Grand Fancy", 36000, 3600, "BOX"),
        ("10x10 IPL Set out", 39000, 3900, "BOX"),
        ("25 Multi Rider fancy Shots", 2800, 280, "BOX"),
    ],
    "NIGHT FOUNTAIN CELEBRATIONS": [
        ("4' Angry Bird Shower", 600, 60, "1piece"),
        ("Asrafi (5 Pcs)", 640, 64, "BOX"),
        ("Ganga Zamuna Shower (5 Pcs)", 980, 98, "BOX"),
        ("Colour Rain (5 Pcs)", 1300, 130, "BOX"),
        ("Feather pop Shower (5 Pcs)", 1350, 135, "BOX"),
        ("Golden Shower (5 Pcs)", 1400, 140, "BOX"),
        ("Disco Shower (5 Pcs)", 1450, 145, "BOX"),
        ("2' Sun Feast Colour Fountain (5 Pcs)", 1700, 170, "BOX"),
        ("Mini Siren (5 pcs)", 1900, 190, "BOX"),
        ("Mega Siren (3 Pcs)", 1980, 198, "BOX"),
        ("3' Red Sun/ ICE MAGIC Fountain", 2200, 220, "BOX"),
        ("Tin Beer Fountain (1 Pc)", 1100, 110, "1Piece"),
        ("Apple / Pogo Shower Boom (5 pcs)", 2250, 225, "BOX"),
        ("Cocktail Dancing WALA EFECT (3 Pcs)", 3500, 350, "BOX"),
        ("Water Falls Fountain", 2250, 225, "1Piece"),
    ],
    "NIGHT FANCY CELEBRATION": [
        ("Photo Flash (5 Pcs)", 780, 78, "BOX"),
        ("Colour Changing Butterfly (10 Pcs)", 1300, 130, "BOX"),
        ("Colour Smoke Candle Celebration big (3 Pcs)", 1900, 190, "BOX"),
        ("Helicopter (5 pcs)", 1100, 110, "BOX"),
        ("Colour Bambaram red/green (10 Pcs)", 1500, 150, "BOX"),
        ("Peacock Fancy", 1700, 170, "1Piece"),
        ("Bada Peacock", 3900, 390, "1Piece"),
        ("Flying Drone (5 Pcs)", 1500, 150, "BOX"),
        ("Lotus Wheel 4x4 (5 Pcs)", 2200, 220, "1Pack"),
        ("Old is Gold Colour Olai Vedi (25 Pcs)", 2000, 200, "1Pack"),
        ("Shooting Gun Crackling (5 Pcs)", 2250, 225, "1Pack"),
        ("MAD MAX", 740, 74, "BOX"),
        ("Grizz colour fountain", 750, 75, "1 Piece"),
    ],
    "LADDU FOUNTAIN": [
        ("Chun Mun Laddu (5 Pcs)", 2200, 220, "BOX"),
        ("Mega Deluxe Fountain (4 Pcs)", 6000, 600, "BOX"),
        ("COLOUR CHANGING MAGIC STAR (5Pcs)", 4500, 450, "BOX"),
    ],
    "SNAKE and CARTOON": [
        ("3 In 1 Colour fog stick (3 Pcs)", 300, 30, "BOX"),
        ("Zee Boomba (10 Pcs)", 150, 15, "BOX"),
        ("Electric Stone (10 Pcs)", 160, 16, "BOX"),
        ("Cartoon Pots (10 Pcs)", 250, 25, "BOX"),
        ("Snake Cartoon (5 Pcs)", 300, 30, "BOX"),
        ("Block Perpant (50 Tablets)", 280, 28, "BOX"),
        ("Kit Kat (10 Pcs)", 350, 35, "BOX"),
    ],
    "CHILDRENS ROLL CAP/GUN": [
        ("Roll Cab", 76, 76, "BOX"),
        ("Small Size Gun", 70, 70, "BOX"),
        ("Medium Size Gun", 100, 100, "BOX"),
        ("Mega Gun", 170, 170, "BOX"),
        ("Ring Cap Gun", 100, 100, "BOX"),
    ],
    "COLOUR MATCHES": [
        ("Deluxe Match (100 Sticks)", 800, 80, "BOX"),
        ("Hero Match (100 Sticks)", 1500, 150, "BOX"),
        ("Mega Laptop Match (100 Sticks)", 2500, 250, "BOX"),
        ("VIP Top 10 Laptop Match (100 Sticks)", 2900, 290, "BOX"),
    ],
    "NEW ARRIVALS": [
        ("Jungle Beat Sound (5 Pcs)", 1500, 150, "BOX"),
        ("Shin chan (5 Pcs)", 1500, 150, "BOX"),
        ("90 Digital Cracker (3 Pcs)", 1700, 170, "BOX"),
        ("Emu Egg (2 Pcs)", 2500, 250, "BOX"),
        ("Dancing Umberla", 2200, 220, "1Piece"),
        ("Lolly Pop Flash Stick (5 Pcs)", 2400, 240, "BOX"),
        ("WIRE CHAKKAR (10 PCS)", 2200, 220, "BOX"),
        ("AK 47 Machine Gun", 2300, 230, "1Piece"),
        ("Selfi Stick (5 Pcs)", 1600, 160, "BOX"),
        ("Bat & Smoke Ball", 2400, 240, "1Piece"),
        ("Magic Digital Sound Wala", 2200, 220, "1Piece"),
        ("Star Show Popcorn Crackling", 2200, 220, "1Piece"),
        ("ICE CONE FALLS (2 Pcs)", 2800, 280, "BOX"),
        ("GenZ Mobile Shower", 2000, 200, "1 Piece"),
        ("KADHAYUTHAM FALLS", 1900, 190, "1 Piece"),
        ("CYLINDER BOMB", 1600, 160, "BOX"),
        ("SPARKLING SWARD", 1400, 140, "BOX"),
        ("INFINITY STAR CRACKLING FOUNTAIN (3 Pcs)", 3900, 390, "BOX"),
        ("Popcorn Crackling Star", 2200, 220, "1Piece"),
    ],
    "GIFT BOXES": [
        ("Family Gift Box (21 Items)", 350, 350, "BOX"),
        ("Premium Gift box", 1600, 1600, "1CASE"),
        ("Family Gift Box (25 Items)", 450, 450, "BOX"),
        ("Family Gift Box (30 Items)", 550, 550, "BOX"),
        ("Family Gift Box (35 Items)", 650, 650, "BOX"),
        ("Family Gift Box (40 Items)", 750, 750, "BOX"),
        ("Family Gift Box (50 Items)", 950, 950, "BOX"),
        ("Family Gift Box (60 Items)", 1150, 1150, "BOX"),
    ],
    "COMBO PACKS": [
        ("3000 Combo Pack", 3000, 3000, "1CASE"),
        ("4000 Combo Pack", 4000, 4000, "1CASE"),
        ("5000 Combo Pack", 5000, 5000, "1CASE"),
        ("7000 Combo Pack", 7000, 7000, "1CASE"),
    ],
    "SPECIAL SERIES FANCY SKY SHOTS": [
        ("Trible ball Fancy Pipe Out", 2400, 240, "1piece"),
        ("Nayagara Falls Out", 3700, 370, "1piece"),
        ("Double Colour Ball Out", 4250, 425, "1Piece"),
        ("Seven Step Fancy Out", 4500, 450, "1Piece"),
        ("Digital Crackling Star", 3900, 390, "1piece"),
        ("Zumba dance sky out (6Pcs)", 2200, 220, "Box"),
        ("4.5' Wow Series Fancy Pipe Out", 4750, 475, "1Piece"),
    ],
}

def generate_sku(product_name):
    """Generate a unique SKU from product name"""
    # Take first 3 words and convert to uppercase, remove special chars
    words = product_name.split()[:3]
    sku = ''.join([word.upper()[:3] for word in words])
    # Add random suffix for uniqueness
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"{sku}{suffix}"

def generate_slug(product_name):
    """Generate a unique slug from_product name"""
    base_slug = product_name.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace("'", "")
    # Add random suffix for uniqueness
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"{base_slug}-{suffix}"

def import_products():
    for category_name, products in product_data.items():
        # Get or create category
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={
                'slug': category_name.lower().replace(' ', '-').replace('/', '-'),
                'is_active': True
            }
        )
        if created:
            print(f"Created category: {category_name}")
        
        # Import products
        for product_name, original_price, discounted_price, unit in products:
            # Check if product already exists
            existing_product = Product.objects.filter(name=product_name).first()
            if existing_product:
                print(f"Product already exists: {product_name}")
                continue
            
            # Generate unique SKU and slug
            sku = generate_sku(product_name)
            slug = generate_slug(product_name)
            
            # Create product
            product = Product.objects.create(
                name=product_name,
                slug=slug,
                sku=sku,
                category=category,
                regular_price=Decimal(str(original_price)),
                sale_price=Decimal(str(discounted_price)),
                stock=100,
                is_active=True,
                description=f"{product_name} - {unit}. High quality crackers from Vasantham Crackers World with 90% discount offer.",
                short_description=f"{product_name} - {unit}",
                product_type='box',
                safety_level='medium'
            )
            print(f"Created product: {product_name} - ₹{original_price} (Discount: ₹{discounted_price})")

if __name__ == "__main__":
    import_products()
    print("Import completed!")
