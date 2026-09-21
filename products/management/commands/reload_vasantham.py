from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = 'Clear all products and reload correct Vasantham products'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('CLEARING ALL PRODUCTS AND CATEGORIES...'))
        
        # Count before
        product_count_before = Product.objects.count()
        category_count_before = Category.objects.count()
        self.stdout.write(f'Before: {product_count_before} products, {category_count_before} categories')
        
        # Clear all data
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared all products and categories'))
        
        # Load Vasantham products
        self.stdout.write('Loading Vasantham products...')
        
        # Import the Vasantham product data
        vasantham_data = [
            # One sound crackers
            ("4 ' Lakshmi", "One sound crackers", 180, 18, "PKT"),
            ("3 1/2 Lakshmi", "One sound crackers", 140, 14, "PKT"),
            ("4 ' Lakshmi Deluxe", "One sound crackers", 300, 30, "PKT"),
            ("Golden Lakshmi Deluxe", "One sound crackers", 340, 34, "PKT"),
            ("5' Kumki Deluxe", "One sound crackers", 440, 44, "PKT"),
            ("Deluxe Jallikattu", "One sound crackers", 500, 50, "PKT"),
            ("Two Sound Colour", "One sound crackers", 440, 44, "PKT"),
            ("2 3/4 ' Kuruvi", "One sound crackers", 80, 8, "PKT"),
            # PENCIL and (Sattai) TWINGLING STARS
            ("1 1/2' (Sattai) Twingling Star (10 Pcs)", "PENCIL and (Sattai) TWINGLING STARS", 280, 28, "BOX"),
            ("4' (Sattai) Twingling Star (10 Pcs)", "PENCIL and (Sattai) TWINGLING STARS", 740, 74, "BOX"),
            ("7 ' Pencil ( 10 Pcs)", "PENCIL and (Sattai) TWINGLING STARS", 320, 32, "BOX"),
            ("10 ' Pencil ( 10 Pcs)", "PENCIL and (Sattai) TWINGLING STARS", 680, 68, "BOX"),
            ("Ultra Torch pencil (3 Pcs)", "PENCIL and (Sattai) TWINGLING STARS", 720, 72, "BOX"),
            ("Rainbow flash Pencil (5 Pcs)", "PENCIL and (Sattai) TWINGLING STARS", 1500, 150, "BOX"),
            ("Sivakasi special Candle Pencil (2 Pcs)", "PENCIL and (Sattai) TWINGLING STARS", 2000, 200, "BOX"),
            ("Popcorn Pencil (5 Pcs)", "PENCIL and (Sattai) TWINGLING STARS", 2300, 230, "BOX"),
            # SPARKLERS
            ("7 Cm Electric Sparklers", "SPARKLERS", 100, 10, "BOX"),
            ("7 Cm Colour Sparklers", "SPARKLERS", 120, 12, "BOX"),
            ("7 Cm Green Sparklers", "SPARKLERS", 140, 14, "BOX"),
            ("7 Cm Red Sparklers", "SPARKLERS", 160, 16, "BOX"),
            ("10 Cm Electric Sparklers", "SPARKLERS", 180, 18, "BOX"),
            ("10 Cm Colour Sparklers", "SPARKLERS", 200, 20, "BOX"),
            ("10 Cm Green Sparklers", "SPARKLERS", 220, 22, "BOX"),
            ("10 Cm Red Sparklers", "SPARKLERS", 240, 24, "BOX"),
            ("12 Cm Electric Sparklers", "SPARKLERS", 280, 28, "BOX"),
            ("12 Cm Colour Sparklers", "SPARKLERS", 300, 30, "BOX"),
            ("12 Cm Green Sparklers", "SPARKLERS", 340, 34, "BOX"),
            ("12 Cm Red Sparklers", "SPARKLERS", 360, 36, "BOX"),
            ("15 Cm Electric Sparklers", "SPARKLERS", 440, 44, "BOX"),
            ("15 Cm Colour Sparklers", "SPARKLERS", 460, 46, "BOX"),
            ("15 Cm Green Sparklers", "SPARKLERS", 480, 48, "BOX"),
            ("15 Cm Red Sparklers", "SPARKLERS", 500, 50, "BOX"),
            ("30 Cm Electric Sparklers", "SPARKLERS", 440, 44, "BOX"),
            ("30 Cm Colour Sparklers", "SPARKLERS", 460, 46, "BOX"),
            ("30 Cm Green Sparklers", "SPARKLERS", 480, 48, "BOX"),
            ("30 Cm Red Sparklers", "SPARKLERS", 500, 50, "BOX"),
            ("50 Cm Electric Sparklers", "SPARKLERS", 1650, 165, "BOX"),
            ("50 Cm Colour Sparklers", "SPARKLERS", 1750, 175, "BOX"),
            # FLOWER POTS
            ("Flower Pots Small ( 10 Pcs)", "FLOWER POTS", 480, 48, "BOX"),
            ("Flower Pots Big (10 Pcs)", "FLOWER POTS", 780, 78, "BOX"),
            ("Flower Pots Special (10 Pcs)", "FLOWER POTS", 1200, 120, "BOX"),
            ("Flower Pots Ashoka (10 Pcs)", "FLOWER POTS", 1500, 150, "BOX"),
            ("Flower Pots Colour Koti (10 Pcs)", "FLOWER POTS", 2100, 210, "BOX"),
            ("Special Colour Koti (10 Pcs)", "FLOWER POTS", 2500, 250, "BOX"),
            ("Flower pots Colour Koti Deluxe(10 Pcs)", "FLOWER POTS", 3900, 390, "BOX"),
            ("Motu Patlu Tri Colour (5 Pcs)", "FLOWER POTS", 2200, 220, "BOX"),
            ("Mega Tri Colour Fountain ( 5 pcs)", "FLOWER POTS", 3200, 320, "BOX"),
            ("Jumbo Super Deluxe ( 10 pcs)", "FLOWER POTS", 4400, 440, "BOX"),
            ("Flower pots Multi Colour Giant (10 Pcs)", "FLOWER POTS", 4500, 450, "BOX"),
            ("Gypsy Colour Flower pots (5Pcs)", "FLOWER POTS", 1900, 190, "Box"),
            # GROUND CHAKKARS
            ("Ground Chakkar Small(10 Pcs)", "GROUND CHAKKARS", 430, 43, "BOX"),
            ("Ground Chakkar Big ( 25 Pcs)", "GROUND CHAKKARS", 1100, 110, "BOX"),
            ("Ground Chakkar Ashoka (10 Pcs)", "GROUND CHAKKARS", 800, 80, "BOX"),
            ("Ground Chakkar Special (10 Pcs)", "GROUND CHAKKARS", 1200, 120, "BOX"),
            ("Ground Chakkar Deluxe ( 10 Pcs)", "GROUND CHAKKARS", 1600, 160, "BOX"),
            ("Disco Wheel ( 5 Pcs)", "GROUND CHAKKARS", 700, 70, "BOX"),
            ("Whizzling Wheel ( 5 Pcs)", "GROUND CHAKKARS", 1500, 150, "BOX"),
            ("Chakkar Spinner Deluxe (10Pcs)", "GROUND CHAKKARS", 1800, 180, "BOX"),
            # SKY ROCKETS
            ("Baby Rocket ( 10 Pcs)", "SKY ROCKETS", 350, 35, "BOX"),
            ("Rocket bomb ( 10 Pcs)", "SKY ROCKETS", 800, 80, "BOX"),
            ("Lunix /2 Sound Rocket(10 Pcs)", "SKY ROCKETS", 1500, 150, "BOX"),
            ("Whistling Rocket (10 Pcs)", "SKY ROCKETS", 1700, 170, "BOX"),
            # BIJILI/ BOMB ITEMS
            ("Red Bijili ( 50 pcs)", "BIJILI/ BOMB ITEMS", 150, 15, "PKT"),
            ("Red Bijili ( 100 pcs)", "BIJILI/ BOMB ITEMS", 350, 35, "PKT"),
            ("Bullet Bomb (10 Pcs)", "BIJILI/ BOMB ITEMS", 360, 36, "BOX"),
            ("Atom Bomb (10 Pcs)", "BIJILI/ BOMB ITEMS", 750, 75, "BOX"),
            ("Hydro Bomb ( 10 Pcs)", "BIJILI/ BOMB ITEMS", 950, 95, "BOX"),
            ("King of King Bomb (10 Pcs)", "BIJILI/ BOMB ITEMS", 1250, 125, "BOX"),
            ("Classic Bomb ( 10 Pcs)", "BIJILI/ BOMB ITEMS", 1500, 150, "BOX"),
            ("Dinoser Bomb ( 10 Pcs)", "BIJILI/ BOMB ITEMS", 2250, 225, "BOX"),
            ("555 Bomb ( 10 Pcs)", "BIJILI/ BOMB ITEMS", 1500, 150, "BOX"),
            ("Digital Deluxe Bomb (10 Pcs)", "BIJILI/ BOMB ITEMS", 2500, 250, "BOX"),
            ("Stripped (vari) Bijili (100 Pcs)", "BIJILI/ BOMB ITEMS", 400, 40, "PKT"),
            # PAPER BOMB
            ("Adiyal Paper Bomb ¼ Kg", "PAPER BOMB", 480, 48, "1PIECE"),
            ("Adiyal Paper Bomb ½ Kg", "PAPER BOMB", 960, 96, "1PIECE"),
            ("Clolour Paper Vedi (5 Pcs)", "PAPER BOMB", 1000, 100, "1PKT"),
            ("Avadhar Paper Bomb (10 Pcs)", "PAPER BOMB", 2500, 250, "BOX"),
            ("Crorepathy Paper Bomb (2 Pcs)", "PAPER BOMB", 2400, 240, "BOX"),
            ("Adiyal Paper Bomb 1 Kg", "PAPER BOMB", 1900, 190, "1PIECE"),
            ("Money Bank (3 Pcs)", "PAPER BOMB", 1500, 150, "BOX"),
            # Wala
            ("28 Chorsa", "Wala", 180, 18, "BOX"),
            ("28 Giant", "Wala", 300, 30, "BOX"),
            ("56 Giant", "Wala", 500, 50, "BOX"),
            ("24 Deluxe", "Wala", 600, 60, "PKT"),
            ("50 Deluxe", "Wala", 1300, 130, "PKT"),
            ("100 Deluxe", "Wala", 2600, 260, "BOX"),
            ("100 Wala", "Wala", 450, 45, "BOX"),
            ("1000 Wala", "Wala", 1700, 170, "BOX"),
            ("1000 Wala Power", "Wala", 3200, 320, "BOX"),
            ("2000 Wala", "Wala", 3500, 350, "BOX"),
            ("2000 Wala Power", "Wala", 6400, 640, "BOX"),
            ("5000 Wala", "Wala", 9000, 900, "BOX"),
            ("5000 Wala Power", "Wala", 15000, 1500, "BOX"),
            ("10000 Wala", "Wala", 18000, 1800, "BOX"),
            ("10000 Wala Power", "Wala", 30000, 3000, "BOX"),
            # SKY NIGHT FANCY CELEBRATIONS
            ("Chotta Pipe Multi Colour out", "SKY NIGHT FANCY CELEBRATIONS", 460, 46, "1Piece"),
            ("7 Color Shots ( 5 Pcs)", "SKY NIGHT FANCY CELEBRATIONS", 1300, 130, "BOX"),
            ("Sky Shot Out ( 5 Pcs)", "SKY NIGHT FANCY CELEBRATIONS", 2100, 210, "BOX"),
            ("Colour Celebration (5 pcs)", "SKY NIGHT FANCY CELEBRATIONS", 2400, 240, "BOX"),
            ("2' Fancy Pipe Out", "SKY NIGHT FANCY CELEBRATIONS", 1200, 120, "1piece"),
            ("2' Fancy Pipe Out ( 3 Pcs )", "SKY NIGHT FANCY CELEBRATIONS", 2900, 290, "BOX"),
            ("3' Fancy Pipe Out", "SKY NIGHT FANCY CELEBRATIONS", 2400, 240, "1piece"),
            ("3½' Fancy Pipe Out", "SKY NIGHT FANCY CELEBRATIONS", 3200, 320, "1piece"),
            ("3½' Fancy Pipe Out ( 2 Pcs)", "SKY NIGHT FANCY CELEBRATIONS", 6500, 650, "BOX"),
            ("4 ' Fancy Pipe Out", "SKY NIGHT FANCY CELEBRATIONS", 4200, 420, "1Piece"),
            ("4' Fancy Pipe Out ( 2 Pcs )", "SKY NIGHT FANCY CELEBRATIONS", 7900, 790, "BOX"),
            ("4½' Fancy Pipe Out ( 2 Pcs )", "SKY NIGHT FANCY CELEBRATIONS", 8500, 850, "BOX"),
            ("5 ' Mega Fancy Pipe Out ( 2 Pcs )", "SKY NIGHT FANCY CELEBRATIONS", 9500, 950, "BOX"),
            # REPEATING MULTI COLOUR FANCY SHOTS
            ("12 Rider Fancy Shots", "REPEATING MULTI COLOUR FANCY SHOTS", 1600, 160, "BOX"),
            ("12 Multi Colour Fancy Shots", "REPEATING MULTI COLOUR FANCY SHOTS", 2200, 220, "BOX"),
            ("30 Special Multi Colour Fancy Shots", "REPEATING MULTI COLOUR FANCY SHOTS", 4500, 450, "BOX"),
            ("60 Multi Colour Fancy Shots", "REPEATING MULTI COLOUR FANCY SHOTS", 8400, 840, "BOX"),
            ("120 Multi Colour Fancy Shots", "REPEATING MULTI COLOUR FANCY SHOTS", 16400, 1640, "BOX"),
            ("240 Multi Colour Fancy Shots", "REPEATING MULTI COLOUR FANCY SHOTS", 32000, 3200, "BOX"),
            ("20x 2.5' Set out Grand Fancy", "REPEATING MULTI COLOUR FANCY SHOTS", 27000, 2700, "BOX"),
            ("30x 2.5' Set out Grand Fancy", "REPEATING MULTI COLOUR FANCY SHOTS", 36000, 3600, "BOX"),
            ("10x10 IPL Set out", "REPEATING MULTI COLOUR FANCY SHOTS", 39000, 3900, "BOX"),
            ("25 Multi Rider fancy Shots", "REPEATING MULTI COLOUR FANCY SHOTS", 2800, 280, "BOX"),
            # NIGHT FOUNTAIN CELEBRATIONS
            ("4' Angry Bird Shower", "NIGHT FOUNTAIN CELEBRATIONS", 600, 60, "1piece"),
            ("Asrafi ( 5 Pcs )", "NIGHT FOUNTAIN CELEBRATIONS", 640, 64, "BOX"),
            ("Ganga Zamuna Shower( 5 Pcs)", "NIGHT FOUNTAIN CELEBRATIONS", 980, 98, "BOX"),
            ("Colour Rain ( 5 Pcs)", "NIGHT FOUNTAIN CELEBRATIONS", 1300, 130, "BOX"),
            ("Feather pop Shower ( 5 Pcs)", "NIGHT FOUNTAIN CELEBRATIONS", 1350, 135, "BOX"),
            ("Golden Shower ( 5 Pcs)", "NIGHT FOUNTAIN CELEBRATIONS", 1400, 140, "BOX"),
            ("Disco Shower ( 5 Pcs)", "NIGHT FOUNTAIN CELEBRATIONS", 1450, 145, "BOX"),
            ("2' Sun Feast Colour Fountain ( 5 Pcs)", "NIGHT FOUNTAIN CELEBRATIONS", 1700, 170, "BOX"),
            ("Mini Siren( 5 pcs)", "NIGHT FOUNTAIN CELEBRATIONS", 1900, 190, "BOX"),
            ("Mega Siren ( 3 Pcs )", "NIGHT FOUNTAIN CELEBRATIONS", 1980, 198, "BOX"),
            ("3' Red Sun/ ICE MAGIC Fountain", "NIGHT FOUNTAIN CELEBRATIONS", 2200, 220, "BOX"),
            ("Tin Beer Fountain ( 1 Pc)", "NIGHT FOUNTAIN CELEBRATIONS", 1100, 110, "1Piece"),
            ("Apple / Pogo Shower Boom ( 5 pcs)", "NIGHT FOUNTAIN CELEBRATIONS", 2250, 225, "BOX"),
            ("Cocktail Dancing WALA EFECT (3 Pcs)", "NIGHT FOUNTAIN CELEBRATIONS", 3500, 350, "BOX"),
            ("Water Falls Fountain", "NIGHT FOUNTAIN CELEBRATIONS", 2250, 225, "1Piece"),
            # NIGHT FANCY CELEBRATION
            ("Photo Flash ( 5 Pcs)", "NIGHT FANCY CELEBRATION", 780, 78, "BOX"),
            ("Colour Changing Butterfly ( 10 Pcs)", "NIGHT FANCY CELEBRATION", 1300, 130, "BOX"),
            ("Colour Smoke Candle Celebration big (3 Pcs)", "NIGHT FANCY CELEBRATION", 1900, 190, "BOX"),
            ("Helicopter ( 5 pcs)", "NIGHT FANCY CELEBRATION", 1100, 110, "BOX"),
            ("Colour Bambaram red/green ( 10 Pcs)", "NIGHT FANCY CELEBRATION", 1500, 150, "BOX"),
            ("Peacock Fancy", "NIGHT FANCY CELEBRATION", 1700, 170, "1Piece"),
            ("Bada Peacock", "NIGHT FANCY CELEBRATION", 3900, 390, "1Piece"),
            ("Lotus Wheel 4x4 ( 5 Pcs)", "NIGHT FANCY CELEBRATION", 2200, 220, "1Pack"),
            ("Old is Gold Colour Olai Vedi ( 25 Pcs )", "NIGHT FANCY CELEBRATION", 2000, 200, "1Pack"),
            ("Shooting Gun Crackling ( 5 Pcs)", "NIGHT FANCY CELEBRATION", 2250, 225, "1Pack"),
            ("MAD MAX", "NIGHT FANCY CELEBRATION", 740, 74, "BOX"),
            ("Grizz colour fountain", "NIGHT FANCY CELEBRATION", 750, 75, "1 Piece"),
            # LADDU FOUNTAIN
            ("Chun Mun Laddu (5 Pcs)", "LADDU FOUNTAIN", 2200, 220, "BOX"),
            ("Mega Deluxe Fountain (4 Pcs )", "LADDU FOUNTAIN", 6000, 600, "BOX"),
            ("COLOUR CHANGING MAGIC STAR (5Pcs)", "LADDU FOUNTAIN", 4500, 450, "BOX"),
            # SNAKE and CARTOON
            ("3 In 1 Colour fog stick (3 Pcs)", "SNAKE and CARTOON", 300, 30, "BOX"),
            ("Zee Boomba ( 10 Pcs)", "SNAKE and CARTOON", 150, 15, "BOX"),
            ("Electric Stone ( 10 Pcs)", "SNAKE and CARTOON", 160, 16, "BOX"),
            ("Cartoon Pots (10 Pcs)", "SNAKE and CARTOON", 250, 25, "BOX"),
            ("Snake Cartoon ( 5 Pcs)", "SNAKE and CARTOON", 300, 30, "BOX"),
            ("Block Perpant (50 Tablets)", "SNAKE and CARTOON", 280, 28, "BOX"),
            ("Kit Kat ( 10 Pcs)", "SNAKE and CARTOON", 350, 35, "BOX"),
            # CHILDRENS ROLL CAP/GUN
            ("Roll Cab", "CHILDRENS ROLL CAP/GUN", 76, 76, "BOX"),
            ("Small Size Gun", "CHILDRENS ROLL CAP/GUN", 70, 70, "BOX"),
            ("Medium Size Gun", "CHILDRENS ROLL CAP/GUN", 100, 100, "BOX"),
            ("Mega Gun", "CHILDRENS ROLL CAP/GUN", 170, 170, "BOX"),
            ("Ring Cap Gun", "CHILDRENS ROLL CAP/GUN", 100, 100, "BOX"),
            # COLOUR MATCHES
            ("Deluxe Match ( 100 Sticks)", "COLOUR MATCHES", 800, 80, "BOX"),
            ("Hero Match (100 Sticks)", "COLOUR MATCHES", 1500, 150, "BOX"),
            ("Mega Laptop Match ( 100 Sticks)", "COLOUR MATCHES", 2500, 250, "BOX"),
            ("VIP Top 10 Laptop Match (100 Sticks)", "COLOUR MATCHES", 2900, 290, "BOX"),
            # NEW ARRIVALS
            ("Jungle Beat Sound ( 5 Pcs)", "NEW ARRIVALS", 1500, 150, "BOX"),
            ("Shin chan (5 Pcs)", "NEW ARRIVALS", 1500, 150, "BOX"),
            ("90 Digital Cracker ( 3 Pcs)", "NEW ARRIVALS", 1700, 170, "BOX"),
            ("Emu Egg (2 Pcs)", "NEW ARRIVALS", 2500, 250, "BOX"),
            ("Dancing Umberla", "NEW ARRIVALS", 2200, 220, "1Piece"),
            ("Lolly Pop Flash Stick (5 Pcs)", "NEW ARRIVALS", 2400, 240, "BOX"),
            ("WIRE CHAKKAR ( 10 PCS)", "NEW ARRIVALS", 2200, 220, "BOX"),
            ("AK 47 Machine Gun", "NEW ARRIVALS", 2300, 230, "1Piece"),
            ("Selfi Stick (5 Pcs)", "NEW ARRIVALS", 1600, 160, "BOX"),
            ("Bat & Smoke Ball", "NEW ARRIVALS", 2400, 240, "1Piece"),
            ("Magic Digital Sound Wala", "NEW ARRIVALS", 2200, 220, "1Piece"),
            ("Star Show Popcorn Crackling", "NEW ARRIVALS", 2200, 220, "1Piece"),
            ("ICE CONE FALLS (2 Pcs)", "NEW ARRIVALS", 2800, 280, "BOX"),
            ("GenZ Mobile Shower", "NEW ARRIVALS", 2000, 200, "1 Piece"),
            ("KADHAYUTHAM FALLS", "NEW ARRIVALS", 1900, 190, "1 Piece"),
            ("CYLINDER BOMB", "NEW ARRIVALS", 1600, 160, "BOX"),
            ("SPARKLING SWARD", "NEW ARRIVALS", 1400, 140, "BOX"),
            ("INFINITY STAR CRACKLING FOUNTAIN (3 Pcs)", "NEW ARRIVALS", 3900, 390, "BOX"),
            ("Popcorn Crackling Star", "NEW ARRIVALS", 2200, 220, "1Piece"),
            # GIFT BOXES
            ("Family Gift Box (21 Items)", "GIFT BOXES", 350, 350, "BOX"),
            ("Premium Gift box", "GIFT BOXES", 1600, 1600, "1CASE"),
            ("Family Gift Box (25 Items)", "GIFT BOXES", 450, 450, "BOX"),
            ("Family Gift Box ( 30 Items)", "GIFT BOXES", 550, 550, "BOX"),
            ("Family Gift Box ( 35 Items)", "GIFT BOXES", 650, 650, "BOX"),
            ("Family Gift Box (40 Items )", "GIFT BOXES", 750, 750, "BOX"),
            ("Family Gift Box (50 Items)", "GIFT BOXES", 950, 950, "BOX"),
            ("Family Gift Box (60 Items)", "GIFT BOXES", 1150, 1150, "BOX"),
            # COMBO PACKS
            ("3000 Combo Pack", "COMBO PACKS", 3000, 3000, "1CASE"),
            ("4000 Combo Pack", "COMBO PACKS", 4000, 4000, "1CASE"),
            ("5000 Combo Pack", "COMBO PACKS", 5000, 5000, "1CASE"),
            ("7000 Combo Pack", "COMBO PACKS", 7000, 7000, "1CASE"),
            # SPECIAL SERIES FANCY SKY SHOTS
            ("Trible ball Fancy Pipe Out", "SPECIAL SERIES FANCY SKY SHOTS", 2400, 240, "1piece"),
            ("Nayagara Falls Out", "SPECIAL SERIES FANCY SKY SHOTS", 3700, 370, "1piece"),
            ("Double Colour Ball Out", "SPECIAL SERIES FANCY SKY SHOTS", 4250, 425, "1Piece"),
            ("Seven Step Fancy Out", "SPECIAL SERIES FANCY SKY SHOTS", 4500, 450, "1Piece"),
            ("Digital Crackling Star", "SPECIAL SERIES FANCY SKY SHOTS", 3900, 390, "1piece"),
            ("Zumba dance sky out (6Pcs)", "SPECIAL SERIES FANCY SKY SHOTS", 2200, 220, "Box"),
            ("4.5' Wow Series Fancy Pipe Out", "SPECIAL SERIES FANCY SKY SHOTS", 4750, 475, "1Piece"),
        ]
        
        # Create categories first
        categories = set([item[1] for item in vasantham_data])
        category_objects = {}
        for cat_name in categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'slug': cat_name.lower().replace(' ', '-').replace('/', '-'),
                    'is_active': True,
                    'order': 0
                }
            )
            category_objects[cat_name] = category
            if created:
                self.stdout.write(f'+ Created category: {cat_name}')
        
        # Create products
        for name, category_name, regular_price, sale_price, unit in vasantham_data:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'slug': name.lower().replace(' ', '-').replace('/', '-').replace("'", ''),
                    'sku': name[:50].replace(' ', '-').upper(),
                    'category': category_objects[category_name],
                    'regular_price': regular_price,
                    'sale_price': sale_price,
                    'stock': 100,
                    'is_active': True,
                    'short_description': f'{name} - {category_name} ({unit})',
                    'description': f'{name} from {category_name} category. Original price: ₹{regular_price}, Discount price: ₹{sale_price}',
                }
            )
            if created:
                self.stdout.write(f'+ Created product: {name}')
        
        # Count after
        product_count_after = Product.objects.count()
        category_count_after = Category.objects.count()
        
        self.stdout.write(self.style.SUCCESS('Vasantham products loaded successfully'))
        self.stdout.write(f'After: {product_count_after} products, {category_count_after} categories')
        self.stdout.write(self.style.SUCCESS(f'+ Products added: {product_count_after}'))
        self.stdout.write(self.style.SUCCESS(f'+ Categories added: {category_count_after}'))
