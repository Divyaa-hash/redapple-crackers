from django.core.management.base import BaseCommand
from products.models import Product, Category
import re


class Command(BaseCommand):
    help = 'Update products from Baby Crackers catalog data'

    def handle(self, *args, **options):
        # Baby Crackers product data
        baby_crackers_data = """
SINGLE SOUND CRACKERS
2 1/2" Kuruvi|1Pkt|40
3 1/2" Lakshmi|1Pkt|60
4" Lakshmi|1Pkt|85
4" Lakshmi Deluxe|1Pkt|125
4" Lakshmi Mega Deluxe|1Pkt|150
Two Sound Crackers|1Pkt|150
Gold Lakshmi|1Pkt|175
5" Kamsan|1Pkt|250
6" Jallikattu / Lakshmi|1Pkt|300

GROUND CHAKKARS
Ground Chakkar Big (10 Pcs)|1Box|175
Ground Chakkar Asoka (10 Pcs)|1Box|225
Ground Chakkar Special (10 Pcs)|1Box|325
Ground Chakkar Deluxe (10 Pcs)|1Box|650

FANCY GROUND CHAKKARS
INF Spin Master Mini (10 Pcs)|1Box|400
Sunflower Wheel (5 Pcs)|1Box|525
Whistling Wheel (5 Pcs)|1Box|550
Wire Chakkar (10 Pcs)|1Box|800
Maska Chaska (5 Pcs)|1Box|750
Lotus Wheel (5 Pcs)|1Box|800
Rio Wheel ( 10 Pcs) (Orange and Purple)|1Box|1100
4*4 Wheel (5Pcs)|1Box|800
Tiddo|1Box|600

FLOWER POTS
Flower Pot Big (10 Pcs)|1Box|300
Flower Pot Special (10 Pcs)|1Box|375
Flower Pot Asoka (10 Pcs)|1Box|500
Flower Pot Deluxe (5 Pcs)|1Box|800
Flower Pot Super Deluxe (2 Pcs)|1Box|550

FANCY FLOWER POTS
Colour Koti (10Pcs)|1Box|900
Purple Cone|1Box|900
Gypsy (5Pcs) / Lucky (5 Pcs)|1Box|800
Scooby doo  Tri Colour Fountain(5 Pcs)|1Box|900
Tri colour Deluxe (3 pcs)|1Box|1050
Colour Koti Deluxe (10Pcs)|1Box|1600
Pinky Pie (6 Pcs) (Pink Colour)|1Box|1800
Jelly Been Super (10Pcs)|1Box|2150
Violet Colout Koti (10 Pcs)|1Box|3500

TWINKLING STARS
1.5' Twinkling Star|1Box|125
4' Twinkling Star|1Box|300

CANDLES
12' Silver Torch|1Box|350
Candy Crush/Jelly Belly Candle|1Box|600

FANCY CANDLES
Selfie stick (5 Pcs)|1Box|750
Navrang tri colour (5 Pcs)|1Box|750
Water falls /Pop Corn Pencil (5 Pcs)|1Box|900
Rainbow Smoke (3 Pcs)|1Box|750
Bat and Ball|1Box|1200

TOYS and SPRINKLERS
Try Colour Diamond (5 Pcs)|1Box|75
Magic Pops (10 Pcs)|1Box|75
Kit Kat / Tip Tap (10 Pcs)|1Box|150

BIJILI CRACKERS
Red Bijili Gold (100 Pcs)|1Pkt|175
Stripped Bijili (100 Pcs)|1Pkt|200
Bro Bijili ( 100 Pcs)|1Pkt|250

KIDS SPECIAL FANCY FOUNTAINS
Layz ( Red,Green,Silver,Gold,RandG)|1Box|150
Kurkur( Red,Green,Silver,Gold,RandG)|1Box|275
Asrafi Big (5 Pcs)|1Box|200
Asrafi Small (5 Pcs)|1Box|150
Bro (New)|1Box|450
Kurkure (New)|1Box|450
Hungry Colours (New)|1Box|450
Binge Pop|1Box|800
Mega Siren (3 Pcs)|1Box|1000
Photo Flash (5 Pcs)|1Box|350
Kickerzzz|1Box|600
H2O|1Box|650
Wanted Gun (5 Pcs)|1Box|750
Dancing Butterfly (10 Pcs)|1Box|325
Tin Beer|1Box|425
Bambaram (10 Pcs)|1Box|500
Helicopter (5 Pcs)|1Box|400

SPECIAL FANCY FOUNTAINS (5 Pcs)
Peacock Feather (5 Pcs)|1Box|495
Disco Shower (5 Pcs)|1Box|495
Colour Rain (5 Pcs)|1Box|495
Silver Rain (5 pcs)|1Box|495
Nebula (5 Pcs)|1Box|600
Fire Feather (5 Pcs)|1Box|600

PEACOCK SERIES
Mini Peacock|1Box|495
Magical Peacock (5 Face)|1Box|650
Belly Belly Peacock (3 Face)|1Box|800
Bada Peacock (5 Face)|1Box|1900

SPECIAL KIDS FOUNTAINS
Money In The Bank|1Box|300
Sound Marriage|1Box|275
Little Dove|1Box|300
90 Watts|1Box|495
Shinchan|1Box|425
Kickerzzz|1Box|600
900 CC|1Box|600
Emu Egg|1Box|750
Water Queen|1Box|750
20-20 Fountain|1Box|600
Pistal 5G|1Box|900
Pop Corn New|1Box|600
Popoye (5 Pcs)|1Box|800
Party Canon/ Magic Show (2 Pcs)|1Box|1100
Power Puff Girls ( 5 pcs)|1Box|800

MULTISTEP SPL FANCY FOUNTAINS
Lemon tree 2 in 1|1Box|650
Hybrid 2 in1 New|1Box|750
Jungle Series 2 in 1 New|1Box|1000
Motu Patlu 2 in 1|1Box|1100
Mumbo Jumbo 2 in 1|1Box|1150
Mad Angles 3 in 1|1Box|1250
Helo Panda 5 in 1|1Box|1750
Arjun Tank 3 in 1 New|1Box|2000
Water Melon 3 in 1 New|1Box|1400

NEW ARRIVAL - 2026
Sword|1Box|1250
Smiley Mushroom|1Box|750
Cylinder Bomb|1Box|800
Purple Cone|1Box|1000
Jolly Bobby Asok Brand|1Box|1100
Car  (2 Pcs)|1Box|1250
Taka tak Crackling ( 3pcs )|1Box|1400
Vajra - Handshot|1Box|7000

BOMBS
Hydro Bomb Greeen (10 Pcs)|1Box|325
King Of King Green (10 Pcs)|1Box|425
Classic Bomb (10 Pcs)|1Box|550
Agni Bomb|1Box|850
Digital Bomb (10 Pcs)|1Box|1100

PAPER BOMB
Joker Bomb- 1/4 kg|1Box|250
Mega Paper Bomb- 1/2 kg|1Box|500
Bada Paper Bomb- 1 kg|1Box|1000
Avatar 2|1Box|1750

GARLAND CRACKERS
28 Giant|1Pkt|75
56 Giant|1Pkt|250
24 Deluxe|1Pkt|300
50 Deluxe|1Pkt|500
100 Deluxe|1Pkt|1000
1H Wala|1Pkt|175
1k wala|1Box|800
2k wala|1Box|1600
5k wala|1Box|4000
10k wala|1Box|7500
1k wala spl|1Box|1500
2k wala spl|1Box|3000
5k wala spl|1Box|7500
10k wala spl|1Box|14000

ROCKETS
Rocket Bomb|1Box|275
Colour Rocket|1Box|300
Lunik Express (10 Pcs)|1Box|600
Whistling Rocket (10 Pcs)|1Box|600

MINI AREIAL FANCY
MINI AREIAL FANCY|1Box|900
Chotta Fancy (2 Pcs)|1Box|400
Sevenshot (5 Pcs)|1Box|375
Sky Shot (5 pcs)|1Box|550
Coco Loco (2 Pcs)|1Box|600
Dup Tip (3 Pcs)|1Box|600
Army Force ( 5 pcs)|1Box|600
Beast Show ( 5 pcs)|1Box|600
Seeti maar 30 Shot Missiles|1Box|800
Avengers ( 5 pcs)|1Box|1200

NIGHT MEGA AREIAL FANCY
2' Fancy|1Box|450
2' Fancy (3 Pcs)|1Box|1200
2' Violet Fancy|1Box|1200
2' Pink Fancy|1Box|1200
2 1/2' Three Step|1Box|1100
2 1/2' INF Love All (3 Pcs)|1Box|2250
3' Fancy|1Box|1100
3 1/2' Fancy|1Box|1200
3 1/2' Fancy Kingfisher|1Box|1400
3 1/2' Fancy Sevenstep|1Box|1400
3 1/2' Fancy Nayagara Falls|1Box|1400
3 1/2' Fancy (2 Pcs)|1Box|2750
4' Fancy|1Box|1700
4' 12 Step|1Box|2000
4' Fancy Double Ball|1Box|2000
4' Fancy (2 Pcs)|1Box|3500
5' Fancy|1Box|2750
6' Fancy|1Box|4000

LOVELY SPECIAL FANCY SERIES (1 Pcs)
Crunch|1Box|2250
Festi|1Box|2250
Rockers/Sprinkles|1Box|2000
Flower Power|1Box|2750

LOVELY SPECIAL FANCY SERIES (2 Pcs)
Pop Up (2 Pcs)|1Box|4750
Orange Fancy (2 Pcs)|1Box|4750
Zoom Pink (2 Pcs)|1Box|4750
INF Unique Shells (2 pcs)|1Box|6000
INF Triple Treat (3 pcs)|1Box|5000
Sony Oscar Ring Series (2 Pcs)|1Box|4750

AERIAL REPEATING SHOTS
12 Shot Raider|1Box|495
12 Shot Multicolour|1Box|1100
12 shot Whistling|1Box|1750
25 Shot Colour Volcano|1Box|1000
10 Shot ( Green/Red Tail With Multicolour)|1Box|900

FESTIVAL DISPLAY SHOTS
15 Shot Multi Colour|1Box|1300
30 Shot Multi Colour|1Box|1900
30 Shot Multi Colour - Special|1Box|2150
50 Shot Multi Colour Full Crackling|1Box|3600
60 Shot Multi Colour- mini|1Box|3800
60 Shot Multi Colour - Special|1Box|4300
120 Shot Multi Colour- mini|1Box|7600
120 Shot Multi Colour - Special|1Box|8600
240 Shot Multi Colour - Special|1Box|16000
500 Shot Multi Colour - Special|1Box|32000

NEW ARRIVAL FANTASTIC AERIAL SHOTS
25 Shot Whistling Sound|1Box|3250
Peacock Dance - 30 Shots|1Box|2250
Blue Fantasy - 25 Shots|1Box|2250
30 Shots Zomato Full Crackling|1Box|2750
INF Double Delight 2 in 1|1Box|3750

FESTIVAL MEGA DISPLAY SHOTS
Sony Pixel Shot 5*4|1Box|6000
Bharat Ratna 20 Shots (2.5' Comet)|1Box|14000
Pala Sola Kii 3*10|1Box|14000
New 10*10 Light Celebration|1Box|18000
Univercell 30 Shots (2' Comet)|1Box|19000
INF Colour Rainbow 10*10|1Box|20000
INF Pyro Gems 36 Shots (2' Comet)|1Box|25000
INF Digital Rain 10*7|1Box|9000
INF OSCAR|1Box|37500

SPARKLERS
7 Cm Electric Sparklers|1Box|40
7 Cm Colour Sparklers|1Box|50
7 Cm Green Sparklers|1Box|60
7 Cm Red Sparklers|1Box|70
10 Cm Electric Sparklers|1Box|70
10 Cm Colour Sparklers|1Box|85
10 Cm Green Sparklers|1Box|100
10 Cm Red Sparklers|1Box|100
15 Cm Electric Sparklers|1Box|150
15 Cm Colour Sparklers|1Box|175
15 Cm Green Sparklers|1Box|200
15 Cm Red Sparklers|1Box|200
30 Cm Electric Sparklers|1Box|150
30 Cm Colour Sparklers|1Box|175
30 Cm Green Sparklers|1Box|200
30 Cm Red Sparklers|1Box|200
50 Cm Electric Sparklers|1Box|700
50 Cm Colour Sparklers|1Box|800
50 cm 2 in 1|1Box|900
Rotating Sparklers|1Box|1100

FANCY COLOUR SPARKLERS
Pink Sparklers|1Box|400
Violet Sparklers|1Box|400

COLOUR MATCHES and ROLL CAPS
Super Deluxe 10 in 1|1Box|350
Royal Lamba 10 in 1|1Box|800
Royal Laptop 10 in 1|1Box|1150
Roll Caps|1Box|300
Ring Cap|1Box|50
Snake Serphant Big|1Box|150
Ring Gun|1Box|350
Roll Gun|1Box|350

GIFT BOXES
20 Item|1Box|1750
30 Item|1Box|2750
40 Item|1Box|750
50 Item|1Box|5000

FESTIVAL FAMILY PACK SPECIAL
Kids Pack|1Pack|15000
Family Pack|1Pack|25000
Thala Diwali Pack|1Pack|35000
V.I.P Gold Pck|1Pack|50000
"""
        
        updated_count = 0
        created_count = 0
        current_category = 'GENERAL'
        
        lines = baby_crackers_data.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a category header (no pipe separator)
            if '|' not in line:
                current_category = line
                self.stdout.write(self.style.WARNING(f'Category: {current_category}'))
                continue
            
            # Parse product data: Name|Unit|Price
            parts = line.split('|')
            if len(parts) >= 3:
                product_name = parts[0].strip()
                unit = parts[1].strip()
                original_price = parts[2].strip()
                
                try:
                    original_price = float(original_price)
                except (ValueError, TypeError):
                    self.stdout.write(self.style.WARNING(f'Skipped: {product_name} - Invalid price'))
                    continue
                
                # Apply 10% markup
                new_price = original_price * 1.1
                
                # Try to find existing product by name (case-insensitive)
                product = Product.objects.filter(name__icontains=product_name).first()
                
                if product:
                    # Update existing product
                    old_name = product.name
                    old_price = product.regular_price
                    
                    product.name = product_name
                    product.regular_price = new_price
                    product.save()
                    
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated: {old_name} -> {product_name} | '
                            f'Price: ₹{old_price} -> ₹{new_price:.2f}'
                        )
                    )
                else:
                    # Try to find or create category
                    category = Category.objects.filter(name__icontains=current_category).first()
                    if not category:
                        category = Category.objects.create(
                            name=current_category,
                            slug=current_category.lower().replace(' ', '-').replace('/', '-'),
                            is_active=True
                        )
                        self.stdout.write(self.style.WARNING(f'Created category: {current_category}'))
                    
                    # Create new product
                    slug = product_name.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace('"', '').replace("'", '')
                    sku = slug[:50]
                    
                    # Ensure slug is unique
                    base_slug = slug
                    counter = 1
                    while Product.objects.filter(slug=slug).exists():
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    
                    # Ensure sku is unique
                    base_sku = sku
                    sku_counter = 1
                    while Product.objects.filter(sku=sku).exists():
                        sku = f"{base_sku}-{sku_counter}"
                        sku_counter += 1
                    
                    product = Product.objects.create(
                        name=product_name,
                        slug=slug,
                        sku=sku,
                        category=category,
                        regular_price=new_price,
                        short_description=f'{product_name} - Premium quality crackers',
                        description=f'{product_name} from {current_category}. Premium quality fireworks for your celebrations.',
                        stock=100,
                        is_active=True,
                        is_new=True
                    )
                    
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created: {product_name} | Price: ₹{new_price:.2f} | Category: {current_category}'
                        )
                    )
        
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Updated products: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'Created products: {created_count}'))
        self.stdout.write(self.style.SUCCESS('Baby Crackers product update completed with 10% markup applied!'))
