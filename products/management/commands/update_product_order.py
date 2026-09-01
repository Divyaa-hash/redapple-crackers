from django.core.management.base import BaseCommand
from products.models import Product, Category


class Command(BaseCommand):
    help = 'Update product order to match Baby Crackers website'

    def handle(self, *args, **options):
        # Baby Crackers website product order by category
        product_order = {
            'SINGLE SOUND CRACKERS': [
                '2 1/2" Kuruvi',
                '3 1/2" Lakshmi',
                '4" Lakshmi',
                '4" Lakshmi Deluxe',
                '4" Lakshmi Mega Deluxe',
                'Two Sound Crackers',
                'Gold Lakshmi',
                '5" Kamsan',
                '6" Jallikattu / Lakshmi'
            ],
            'GROUND CHAKKARS': [
                'Ground Chakkar Big (10 Pcs)',
                'Ground Chakkar Asoka (10 Pcs)',
                'Ground Chakkar Special (10 Pcs)',
                'Ground Chakkar Deluxe (10 Pcs)'
            ],
            'FANCY GROUND CHAKKARS': [
                'INF Spin Master Mini (10 Pcs)',
                'Sunflower Wheel (5 Pcs)',
                'Whistling Wheel (5 Pcs)',
                'Wire Chakkar (10 Pcs)',
                'Maska Chaska (5 Pcs)',
                'Lotus Wheel (5 Pcs)',
                'Rio Wheel ( 10 Pcs) (Orange and Purple)',
                '4*4 Wheel (5Pcs)',
                'Tiddo'
            ],
            'FLOWER POTS': [
                'Flower Pot Big (10 Pcs)',
                'Flower Pot Special (10 Pcs)',
                'Flower Pot Asoka (10 Pcs)',
                'Flower Pot Deluxe (5 Pcs)',
                'Flower Pot Super Deluxe (2 Pcs)'
            ],
            'FANCY FLOWER POTS': [
                'Colour Koti (10Pcs)',
                'Purple Cone',
                'Gypsy (5Pcs) / Lucky (5 Pcs)',
                'Scooby doo  Tri Colour Fountain(5 Pcs)',
                'Tri colour Deluxe (3 pcs)',
                'Colour Koti Deluxe (10Pcs)',
                'Pinky Pie (6 Pcs) (Pink Colour)',
                'Jelly Been Super (10Pcs)',
                'Violet Colout Koti (10 Pcs)'
            ],
            'TWINKLING STARS': [
                '1.5\' Twinkling Star',
                '4\' Twinkling Star'
            ],
            'CANDLES': [
                '12\' Silver Torch',
                'Candy Crush/Jelly Belly Candle'
            ],
            'FANCY CANDLES': [
                'Selfie stick (5 Pcs)',
                'Navrang tri colour (5 Pcs)',
                'Water falls /Pop Corn Pencil (5 Pcs)',
                'Rainbow Smoke (3 Pcs)',
                'Bat and Ball'
            ],
            'TOYS and SPRINKLERS': [
                'Try Colour Diamond (5 Pcs)',
                'Magic Pops (10 Pcs)',
                'Kit Kat / Tip Tap (10 Pcs)'
            ],
            'BIJILI CRACKERS': [
                'Red Bijili Gold (100 Pcs)',
                'Stripped Bijili (100 Pcs)',
                'Bro Bijili ( 100 Pcs)'
            ],
            'KIDS SPECIAL FANCY FOUNTAINS': [
                'Layz ( Red,Green,Silver,Gold,RandG)',
                'Kurkur( Red,Green,Silver,Gold,RandG)',
                'Asrafi Big (5 Pcs)',
                'Asrafi Small (5 Pcs)',
                'Bro (New)',
                'Kurkure (New)',
                'Hungry Colours (New)',
                'Binge Pop',
                'Mega Siren (3 Pcs)',
                'Photo Flash (5 Pcs)',
                'Kickerzzz',
                'H2O',
                'Wanted Gun (5 Pcs)',
                'Dancing Butterfly (10 Pcs)',
                'Tin Beer',
                'Bambaram (10 Pcs)',
                'Helicopter (5 Pcs)'
            ],
            'SPECIAL FANCY FOUNTAINS (5 Pcs)': [
                'Peacock Feather (5 Pcs)',
                'Disco Shower (5 Pcs)',
                'Colour Rain (5 Pcs)',
                'Silver Rain (5 pcs)',
                'Nebula (5 Pcs)',
                'Fire Feather (5 Pcs)'
            ],
            'PEACOCK SERIES': [
                'Mini Peacock',
                'Magical Peacock (5 Face)',
                'Belly Belly Peacock (3 Face)',
                'Bada Peacock (5 Face)'
            ],
            'SPECIAL KIDS FOUNTAINS': [
                'Money In The Bank',
                'Sound Marriage',
                'Little Dove',
                '90 Watts',
                'Shinchan',
                'Kickerzzz',
                '900 CC',
                'Emu Egg',
                'Water Queen',
                '20-20 Fountain',
                'Pistal 5G',
                'Pop Corn New',
                'Popoye (5 Pcs)',
                'Party Canon/ Magic Show (2 Pcs)',
                'Power Puff Girls ( 5 pcs)'
            ],
            'MULTISTEP SPL FANCY FOUNTAINS': [
                'Lemon tree 2 in 1',
                'Hybrid 2 in1 New',
                'Jungle Series 2 in 1 New',
                'Motu Patlu 2 in 1',
                'Mumbo Jumbo 2 in 1',
                'Mad Angles 3 in 1',
                'Helo Panda 5 in 1',
                'Arjun Tank 3 in 1 New',
                'Water Melon 3 in 1 New'
            ],
            'NEW ARRIVAL - 2026': [
                'Sword',
                'Smiley Mushroom',
                'Cylinder Bomb',
                'Purple Cone',
                'Jolly Bobby Asok Brand',
                'Car  (2 Pcs)',
                'Taka tak Crackling ( 3pcs )',
                'Vajra - Handshot'
            ],
            'BOMBS': [
                'Hydro Bomb Greeen (10 Pcs)',
                'King Of King Green (10 Pcs)',
                'Classic Bomb (10 Pcs)',
                'Agni Bomb',
                'Digital Bomb (10 Pcs)'
            ],
            'PAPER BOMB': [
                'Joker Bomb- 1/4 kg',
                'Mega Paper Bomb- 1/2 kg',
                'Bada Paper Bomb- 1 kg',
                'Avatar 2'
            ],
            'GARLAND CRACKERS': [
                '28 Giant',
                '56 Giant',
                '24 Deluxe',
                '50 Deluxe',
                '100 Deluxe',
                '1H Wala',
                '1k wala',
                '2k wala',
                '5k wala',
                '10k wala',
                '1k wala spl',
                '2k wala spl',
                '5k wala spl',
                '10k wala spl'
            ],
            'ROCKETS': [
                'Rocket Bomb',
                'Colour Rocket',
                'Lunik Express (10 Pcs)',
                'Whistling Rocket (10 Pcs)'
            ],
            'MINI AREIAL FANCY': [
                'MINI AREIAL FANCY',
                'Chotta Fancy (2 Pcs)',
                'Sevenshot (5 Pcs)',
                'Sky Shot (5 pcs)',
                'Coco Loco (2 Pcs)',
                'Dup Tip (3 Pcs)',
                'Army Force ( 5 pcs)',
                'Beast Show ( 5 pcs)',
                'Seeti maar 30 Shot Missiles',
                'Avengers ( 5 pcs)'
            ],
            'NIGHT MEGA AREIAL FANCY': [
                '2\' Fancy',
                '2\' Fancy (3 Pcs)',
                '2\' Violet Fancy',
                '2\' Pink Fancy',
                '2 1/2\' Three Step',
                '2 1/2\' INF Love All (3 Pcs)',
                '3\' Fancy',
                '3 1/2\' Fancy',
                '3 1/2\' Fancy Kingfisher',
                '3 1/2\' Fancy Sevenstep',
                '3 1/2\' Fancy Nayagara Falls',
                '3 1/2\' Fancy (2 Pcs)',
                '4\' Fancy',
                '4\' 12 Step',
                '4\' Fancy Double Ball',
                '4\' Fancy (2 Pcs)',
                '5\' Fancy',
                '6\' Fancy'
            ],
            'LOVELY SPECIAL FANCY SERIES (1 Pcs)': [
                'Crunch',
                'Festi',
                'Rockers/Sprinkles',
                'Flower Power'
            ],
            'LOVELY SPECIAL FANCY SERIES (2 Pcs)': [
                'Pop Up (2 Pcs)',
                'Orange Fancy (2 Pcs)',
                'Zoom Pink (2 Pcs)',
                'INF Unique Shells (2 pcs)',
                'INF Triple Treat (3 pcs)',
                'Sony Oscar Ring Series (2 Pcs)'
            ],
            'AERIAL REPEATING SHOTS': [
                '12 Shot Raider',
                '12 Shot Multicolour',
                '12 shot Whistling',
                '25 Shot Colour Volcano',
                '10 Shot ( Green/Red Tail With Multicolour)'
            ],
            'FESTIVAL DISPLAY SHOTS': [
                '15 Shot Multi Colour',
                '30 Shot Multi Colour',
                '30 Shot Multi Colour - Special',
                '50 Shot Multi Colour Full Crackling',
                '60 Shot Multi Colour- mini',
                '60 Shot Multi Colour - Special',
                '120 Shot Multi Colour- mini',
                '120 Shot Multi Colour - Special',
                '240 Shot Multi Colour - Special',
                '500 Shot Multi Colour - Special'
            ],
            'NEW ARRIVAL FANTASTIC AERIAL SHOTS': [
                '25 Shot Whistling Sound',
                'Peacock Dance - 30 Shots',
                'Blue Fantasy - 25 Shots',
                '30 Shots Zomato Full Crackling',
                'INF Double Delight 2 in 1'
            ],
            'FESTIVAL MEGA DISPLAY SHOTS': [
                'Sony Pixel Shot 5*4',
                'Bharat Ratna 20 Shots (2.5\' Comet)',
                'Pala Sola Kii 3*10',
                'New 10*10 Light Celebration',
                'Univercell 30 Shots (2\' Comet)',
                'INF Colour Rainbow 10*10',
                'INF Pyro Gems 36 Shots (2\' Comet)',
                'INF Digital Rain 10*7',
                'INF OSCAR'
            ],
            'SPARKLERS': [
                '7 Cm Electric Sparklers',
                '7 Cm Colour Sparklers',
                '7 Cm Green Sparklers',
                '7 Cm Red Sparklers',
                '10 Cm Electric Sparklers',
                '10 Cm Colour Sparklers',
                '10 Cm Green Sparklers',
                '10 Cm Red Sparklers',
                '15 Cm Electric Sparklers',
                '15 Cm Colour Sparklers',
                '15 Cm Green Sparklers',
                '15 Cm Red Sparklers',
                '30 Cm Electric Sparklers',
                '30 Cm Colour Sparklers',
                '30 Cm Green Sparklers',
                '30 Cm Red Sparklers',
                '50 Cm Electric Sparklers',
                '50 Cm Colour Sparklers',
                '50 cm 2 in 1',
                'Rotating Sparklers'
            ],
            'FANCY COLOUR SPARKLERS': [
                'Pink Sparklers',
                'Violet Sparklers'
            ],
            'COLOUR MATCHES and ROLL CAPS': [
                'Super Deluxe 10 in 1',
                'Royal Lamba 10 in 1',
                'Royal Laptop 10 in 1',
                'Roll Caps',
                'Ring Cap',
                'Snake Serphant Big',
                'Ring Gun',
                'Roll Gun'
            ],
            'GIFT BOXES': [
                '20 Item',
                '30 Item',
                '40 Item',
                '50 Item'
            ],
            'FESTIVAL FAMILY PACK SPECIAL': [
                'Kids Pack',
                'Family Pack',
                'Thala Diwali Pack',
                'V.I.P Gold Pck'
            ]
        }
        
        updated_count = 0
        not_found_count = 0
        
        for category_name, product_names in product_order.items():
            # Find or create category
            category = Category.objects.filter(name__icontains=category_name).first()
            if not category:
                self.stdout.write(self.style.WARNING(f'Category not found: {category_name}'))
                continue
            
            # Update order for each product in this category
            for order_index, product_name in enumerate(product_names):
                # Try to find product by name (case-insensitive)
                product = Product.objects.filter(name__icontains=product_name, category=category).first()
                
                if product:
                    # Update product order
                    product.order = order_index
                    product.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated order: {product_name} -> {order_index} (Category: {category_name})'
                        )
                    )
                else:
                    not_found_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'Not found: {product_name} (Category: {category_name})'
                        )
                    )
        
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Updated product orders: {updated_count}'))
        self.stdout.write(self.style.WARNING(f'Not found: {not_found_count}'))
        self.stdout.write(self.style.SUCCESS('Product order update completed!'))
