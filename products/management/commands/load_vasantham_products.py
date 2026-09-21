from django.core.management.base import BaseCommand
from products.models import Product, Category, Brand, Festival
from decimal import Decimal
from django.utils import timezone


class Command(BaseCommand):
    help = 'Load correct Vasantham crackers products from website data'

    def handle(self, *args, **options):
        self.stdout.write('Loading correct Vasantham crackers products...')
        
        # Clear existing data
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write('Cleared existing data')
        
        # Define categories from the website
        categories_data = [
            {'name': 'One sound crackers', 'slug': 'one-sound-crackers', 'order': 1},
            {'name': 'PENCIL and (Sattai) TWINGLING STARS', 'slug': 'pencil-sattai-twinkling-stars', 'order': 2},
            {'name': 'SPARKLERS', 'slug': 'sparklers', 'order': 3},
            {'name': 'FLOWER POTS', 'slug': 'flower-pots', 'order': 4},
            {'name': 'GROUND CHAKKARS', 'slug': 'ground-chakkars', 'order': 5},
            {'name': 'SKY ROCKETS', 'slug': 'sky-rockets', 'order': 6},
            {'name': 'BIJILI/ BOMB ITEMS', 'slug': 'bijili-bomb-items', 'order': 7},
            {'name': 'PAPER BOMB', 'slug': 'paper-bomb', 'order': 8},
            {'name': 'Wala', 'slug': 'wala', 'order': 9},
            {'name': 'SKY NIGHT FANCY CELEBRATIONS', 'slug': 'sky-night-fancy-celebrations', 'order': 10},
            {'name': 'REPEATING MULTI COLOUR FANCY SHOTS', 'slug': 'repeating-multi-colour-fancy-shots', 'order': 11},
            {'name': 'NIGHT FOUNTAIN CELEBRATIONS', 'slug': 'night-fountain-celebrations', 'order': 12},
            {'name': 'NIGHT FANCY CELEBRATION', 'slug': 'night-fancy-celebration', 'order': 13},
            {'name': 'LADDU FOUNTAIN', 'slug': 'laddu-fountain', 'order': 14},
            {'name': 'SNAKE and CARTOON', 'slug': 'snake-cartoon', 'order': 15},
            {'name': 'CHILDRENS ROLL CAP/GUN', 'slug': 'children-roll-cap-gun', 'order': 16},
            {'name': 'COLOUR MATCHES', 'slug': 'colour-matches', 'order': 17},
            {'name': 'NEW ARRIVALS', 'slug': 'new-arrivals', 'order': 18},
            {'name': 'GIFT BOXES', 'slug': 'gift-boxes', 'order': 19},
            {'name': 'COMBO PACKS', 'slug': 'combo-packs', 'order': 20},
            {'name': 'SPECIAL SERIES FANCY SKY SHOTS', 'slug': 'special-series-fancy-sky-shots', 'order': 21},
        ]
        
        # Create categories
        category_map = {}
        for cat_data in categories_data:
            category = Category.objects.create(
                name=cat_data['name'],
                slug=cat_data['slug'],
                description=f'{cat_data["name"]} products',
                order=cat_data['order'],
                is_active=True
            )
            category_map[cat_data['name']] = category
            self.stdout.write(f'Created category: {cat_data["name"]}')
        
        # Create brand
        brand, _ = Brand.objects.get_or_create(
            name='Vasantham',
            defaults={'slug': 'vasantham', 'is_featured': True}
        )
        
        # Create festival
        festival, _ = Festival.objects.get_or_create(
            name='Diwali',
            defaults={
                'slug': 'diwali',
                'description': 'Festival of Lights',
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date(),
                'is_active': True
            }
        )
        
        # Define products from the website
        products_data = [
            # One sound crackers
            {'name': "4' Lakshmi", 'category': 'One sound crackers', 'original_price': 180, 'discount_price': 18, 'unit': 'PKT'},
            {'name': "3 1/2 Lakshmi", 'category': 'One sound crackers', 'original_price': 140, 'discount_price': 14, 'unit': 'PKT'},
            {'name': "4' Lakshmi Deluxe", 'category': 'One sound crackers', 'original_price': 300, 'discount_price': 30, 'unit': 'PKT'},
            {'name': "Golden Lakshmi Deluxe", 'category': 'One sound crackers', 'original_price': 340, 'discount_price': 34, 'unit': 'PKT'},
            {'name': "5' Kumki Deluxe", 'category': 'One sound crackers', 'original_price': 440, 'discount_price': 44, 'unit': 'PKT'},
            {'name': "Deluxe Jallikattu", 'category': 'One sound crackers', 'original_price': 500, 'discount_price': 50, 'unit': 'PKT'},
            {'name': "Two Sound Colour", 'category': 'One sound crackers', 'original_price': 440, 'discount_price': 44, 'unit': 'PKT'},
            {'name': "2 3/4' Kuruvi", 'category': 'One sound crackers', 'original_price': 80, 'discount_price': 8, 'unit': 'PKT'},
            
            # PENCIL and (Sattai) TWINGLING STARS
            {'name': "1 1/2' (Sattai) Twingling Star (10 Pcs)", 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'original_price': 280, 'discount_price': 28, 'unit': 'BOX'},
            {'name': "4' (Sattai) Twingling Star (10 Pcs)", 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'original_price': 740, 'discount_price': 74, 'unit': 'BOX'},
            {'name': "7' Pencil (10 Pcs)", 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'original_price': 320, 'discount_price': 32, 'unit': 'BOX'},
            {'name': "10' Pencil (10 Pcs)", 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'original_price': 680, 'discount_price': 68, 'unit': 'BOX'},
            {'name': "Ultra Torch pencil (3 Pcs)", 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'original_price': 720, 'discount_price': 72, 'unit': 'BOX'},
            {'name': "Rainbow flash Pencil (5 Pcs)", 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            {'name': "Sivakasi special Candle Pencil (2 Pcs)", 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'original_price': 2000, 'discount_price': 200, 'unit': 'BOX'},
            {'name': "Popcorn Pencil (5 Pcs)", 'category': 'PENCIL and (Sattai) TWINGLING STARS', 'original_price': 2300, 'discount_price': 230, 'unit': 'BOX'},
            
            # SPARKLERS
            {'name': "7 Cm Electric Sparklers", 'category': 'SPARKLERS', 'original_price': 100, 'discount_price': 10, 'unit': 'BOX'},
            {'name': "7 Cm Colour Sparklers", 'category': 'SPARKLERS', 'original_price': 120, 'discount_price': 12, 'unit': 'BOX'},
            {'name': "7 Cm Green Sparklers", 'category': 'SPARKLERS', 'original_price': 140, 'discount_price': 14, 'unit': 'BOX'},
            {'name': "7 Cm Red Sparklers", 'category': 'SPARKLERS', 'original_price': 160, 'discount_price': 16, 'unit': 'BOX'},
            {'name': "10 Cm Electric Sparklers", 'category': 'SPARKLERS', 'original_price': 180, 'discount_price': 18, 'unit': 'BOX'},
            {'name': "10 Cm Colour Sparklers", 'category': 'SPARKLERS', 'original_price': 200, 'discount_price': 20, 'unit': 'BOX'},
            {'name': "10 Cm Green Sparklers", 'category': 'SPARKLERS', 'original_price': 220, 'discount_price': 22, 'unit': 'BOX'},
            {'name': "10 Cm Red Sparklers", 'category': 'SPARKLERS', 'original_price': 240, 'discount_price': 24, 'unit': 'BOX'},
            {'name': "12 Cm Electric Sparklers", 'category': 'SPARKLERS', 'original_price': 280, 'discount_price': 28, 'unit': 'BOX'},
            {'name': "12 Cm Colour Sparklers", 'category': 'SPARKLERS', 'original_price': 300, 'discount_price': 30, 'unit': 'BOX'},
            {'name': "12 Cm Green Sparklers", 'category': 'SPARKLERS', 'original_price': 340, 'discount_price': 34, 'unit': 'BOX'},
            {'name': "12 Cm Red Sparklers", 'category': 'SPARKLERS', 'original_price': 360, 'discount_price': 36, 'unit': 'BOX'},
            {'name': "15 Cm Electric Sparklers", 'category': 'SPARKLERS', 'original_price': 440, 'discount_price': 44, 'unit': 'BOX'},
            {'name': "15 Cm Colour Sparklers", 'category': 'SPARKLERS', 'original_price': 460, 'discount_price': 46, 'unit': 'BOX'},
            {'name': "15 Cm Green Sparklers", 'category': 'SPARKLERS', 'original_price': 480, 'discount_price': 48, 'unit': 'BOX'},
            {'name': "15 Cm Red Sparklers", 'category': 'SPARKLERS', 'original_price': 500, 'discount_price': 50, 'unit': 'BOX'},
            {'name': "30 Cm Electric Sparklers", 'category': 'SPARKLERS', 'original_price': 440, 'discount_price': 44, 'unit': 'BOX'},
            {'name': "30 Cm Colour Sparklers", 'category': 'SPARKLERS', 'original_price': 460, 'discount_price': 46, 'unit': 'BOX'},
            {'name': "30 Cm Green Sparklers", 'category': 'SPARKLERS', 'original_price': 480, 'discount_price': 48, 'unit': 'BOX'},
            {'name': "30 Cm Red Sparklers", 'category': 'SPARKLERS', 'original_price': 500, 'discount_price': 50, 'unit': 'BOX'},
            {'name': "50 Cm Electric Sparklers", 'category': 'SPARKLERS', 'original_price': 1650, 'discount_price': 165, 'unit': 'BOX'},
            {'name': "50 Cm Colour Sparklers", 'category': 'SPARKLERS', 'original_price': 1750, 'discount_price': 175, 'unit': 'BOX'},
            
            # FLOWER POTS
            {'name': "Flower Pots Small (10 Pcs)", 'category': 'FLOWER POTS', 'original_price': 480, 'discount_price': 48, 'unit': 'BOX'},
            {'name': "Flower Pots Big (10 Pcs)", 'category': 'FLOWER POTS', 'original_price': 780, 'discount_price': 78, 'unit': 'BOX'},
            {'name': "Flower Pots Special (10 Pcs)", 'category': 'FLOWER POTS', 'original_price': 1200, 'discount_price': 120, 'unit': 'BOX'},
            {'name': "Flower Pots Ashoka (10 Pcs)", 'category': 'FLOWER POTS', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            {'name': "Flower Pots Colour Koti (10 Pcs)", 'category': 'FLOWER POTS', 'original_price': 2100, 'discount_price': 210, 'unit': 'BOX'},
            {'name': "Special Colour Koti (10 Pcs)", 'category': 'FLOWER POTS', 'original_price': 2500, 'discount_price': 250, 'unit': 'BOX'},
            {'name': "Flower pots Colour Koti Deluxe(10 Pcs)", 'category': 'FLOWER POTS', 'original_price': 3900, 'discount_price': 390, 'unit': 'BOX'},
            {'name': "Motu Patlu Tri Colour (5 Pcs)", 'category': 'FLOWER POTS', 'original_price': 2200, 'discount_price': 220, 'unit': 'BOX'},
            {'name': "Mega Tri Colour Fountain (5 pcs)", 'category': 'FLOWER POTS', 'original_price': 3200, 'discount_price': 320, 'unit': 'BOX'},
            {'name': "Jumbo Super Deluxe (10 pcs)", 'category': 'FLOWER POTS', 'original_price': 4400, 'discount_price': 440, 'unit': 'BOX'},
            {'name': "Flower pots Multi Colour Giant (10 Pcs)", 'category': 'FLOWER POTS', 'original_price': 4500, 'discount_price': 450, 'unit': 'BOX'},
            {'name': "Gypsy Colour Flower pots (5Pcs)", 'category': 'FLOWER POTS', 'original_price': 1900, 'discount_price': 190, 'unit': 'BOX'},
            
            # GROUND CHAKKARS
            {'name': "Ground Chakkar Small(10 Pcs)", 'category': 'GROUND CHAKKARS', 'original_price': 430, 'discount_price': 43, 'unit': 'BOX'},
            {'name': "Ground Chakkar Big (25 Pcs)", 'category': 'GROUND CHAKKARS', 'original_price': 1100, 'discount_price': 110, 'unit': 'BOX'},
            {'name': "Ground Chakkar Ashoka (10 Pcs)", 'category': 'GROUND CHAKKARS', 'original_price': 800, 'discount_price': 80, 'unit': 'BOX'},
            {'name': "Ground Chakkar Special (10 Pcs)", 'category': 'GROUND CHAKKARS', 'original_price': 1200, 'discount_price': 120, 'unit': 'BOX'},
            {'name': "Ground Chakkar Deluxe (10 Pcs)", 'category': 'GROUND CHAKKARS', 'original_price': 1600, 'discount_price': 160, 'unit': 'BOX'},
            {'name': "Disco Wheel (5 Pcs)", 'category': 'GROUND CHAKKARS', 'original_price': 700, 'discount_price': 70, 'unit': 'BOX'},
            {'name': "Whizzling Wheel (5 Pcs)", 'category': 'GROUND CHAKKARS', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            {'name': "Chakkar Spinner Deluxe (10Pcs)", 'category': 'GROUND CHAKKARS', 'original_price': 1800, 'discount_price': 180, 'unit': 'BOX'},
            
            # SKY ROCKETS
            {'name': "Baby Rocket (10 Pcs)", 'category': 'SKY ROCKETS', 'original_price': 350, 'discount_price': 35, 'unit': 'BOX'},
            {'name': "Rocket bomb (10 Pcs)", 'category': 'SKY ROCKETS', 'original_price': 800, 'discount_price': 80, 'unit': 'BOX'},
            {'name': "Lunix /2 Sound Rocket(10 Pcs)", 'category': 'SKY ROCKETS', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            {'name': "Whistling Rocket (10 Pcs)", 'category': 'SKY ROCKETS', 'original_price': 1700, 'discount_price': 170, 'unit': 'BOX'},
            
            # BIJILI/ BOMB ITEMS
            {'name': "Red Bijili (50 pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 150, 'discount_price': 15, 'unit': 'PKT'},
            {'name': "Red Bijili (100 pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 350, 'discount_price': 35, 'unit': 'PKT'},
            {'name': "Bullet Bomb (10 Pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 360, 'discount_price': 36, 'unit': 'BOX'},
            {'name': "Atom Bomb (10 Pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 750, 'discount_price': 75, 'unit': 'BOX'},
            {'name': "Hydro Bomb (10 Pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 950, 'discount_price': 95, 'unit': 'BOX'},
            {'name': "King of King Bomb (10 Pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 1250, 'discount_price': 125, 'unit': 'BOX'},
            {'name': "Classic Bomb (10 Pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            {'name': "Dinoser Bomb (10 Pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 2250, 'discount_price': 225, 'unit': 'BOX'},
            {'name': "555 Bomb (10 Pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            {'name': "Digital Deluxe Bomb (10 Pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 2500, 'discount_price': 250, 'unit': 'BOX'},
            {'name': "Stripped (vari) Bijili (100 Pcs)", 'category': 'BIJILI/ BOMB ITEMS', 'original_price': 400, 'discount_price': 40, 'unit': 'PKT'},
            
            # PAPER BOMB
            {'name': "Adiyal Paper Bomb ¼ Kg", 'category': 'PAPER BOMB', 'original_price': 480, 'discount_price': 48, 'unit': '1PIECE'},
            {'name': "Adiyal Paper Bomb ½ Kg", 'category': 'PAPER BOMB', 'original_price': 960, 'discount_price': 96, 'unit': '1PIECE'},
            {'name': "Clolour Paper Vedi (5 Pcs)", 'category': 'PAPER BOMB', 'original_price': 1000, 'discount_price': 100, 'unit': '1PKT'},
            {'name': "Avadhar Paper Bomb (10 Pcs)", 'category': 'PAPER BOMB', 'original_price': 2500, 'discount_price': 250, 'unit': 'BOX'},
            {'name': "Crorepathy Paper Bomb (2 Pcs)", 'category': 'PAPER BOMB', 'original_price': 2400, 'discount_price': 240, 'unit': 'BOX'},
            {'name': "Adiyal Paper Bomb 1 Kg", 'category': 'PAPER BOMB', 'original_price': 1900, 'discount_price': 190, 'unit': '1PIECE'},
            {'name': "Money Bank (3 Pcs)", 'category': 'PAPER BOMB', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            
            # Wala
            {'name': "28 Chorsa", 'category': 'Wala', 'original_price': 180, 'discount_price': 18, 'unit': 'BOX'},
            {'name': "28 Giant", 'category': 'Wala', 'original_price': 300, 'discount_price': 30, 'unit': 'BOX'},
            {'name': "56 Giant", 'category': 'Wala', 'original_price': 500, 'discount_price': 50, 'unit': 'BOX'},
            {'name': "24 Deluxe", 'category': 'Wala', 'original_price': 600, 'discount_price': 60, 'unit': 'PKT'},
            {'name': "50 Deluxe", 'category': 'Wala', 'original_price': 1300, 'discount_price': 130, 'unit': 'PKT'},
            {'name': "100 Deluxe", 'category': 'Wala', 'original_price': 2600, 'discount_price': 260, 'unit': 'BOX'},
            {'name': "100 Wala", 'category': 'Wala', 'original_price': 450, 'discount_price': 45, 'unit': 'BOX'},
            {'name': "1000 Wala", 'category': 'Wala', 'original_price': 1700, 'discount_price': 170, 'unit': 'BOX'},
            {'name': "1000 Wala Power", 'category': 'Wala', 'original_price': 3200, 'discount_price': 320, 'unit': 'BOX'},
            {'name': "2000 Wala", 'category': 'Wala', 'original_price': 3500, 'discount_price': 350, 'unit': 'BOX'},
            {'name': "2000 Wala Power", 'category': 'Wala', 'original_price': 6400, 'discount_price': 640, 'unit': 'BOX'},
            {'name': "5000 Wala", 'category': 'Wala', 'original_price': 9000, 'discount_price': 900, 'unit': 'BOX'},
            {'name': "5000 Wala Power", 'category': 'Wala', 'original_price': 15000, 'discount_price': 1500, 'unit': 'BOX'},
            {'name': "10000 Wala", 'category': 'Wala', 'original_price': 18000, 'discount_price': 1800, 'unit': 'BOX'},
            {'name': "10000 Wala Power", 'category': 'Wala', 'original_price': 30000, 'discount_price': 3000, 'unit': 'BOX'},
            
            # SKY NIGHT FANCY CELEBRATIONS
            {'name': "Chotta Pipe Multi Colour out", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 460, 'discount_price': 46, 'unit': '1Piece'},
            {'name': "7 Color Shots (5 Pcs)", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 1300, 'discount_price': 130, 'unit': 'BOX'},
            {'name': "Sky Shot Out (5 Pcs)", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 2100, 'discount_price': 210, 'unit': 'BOX'},
            {'name': "Colour Celebration (5 pcs)", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 2400, 'discount_price': 240, 'unit': 'BOX'},
            {'name': "2' Fancy Pipe Out", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 1200, 'discount_price': 120, 'unit': '1piece'},
            {'name': "2' Fancy Pipe Out (3 Pcs)", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 2900, 'discount_price': 290, 'unit': 'BOX'},
            {'name': "3' Fancy Pipe Out", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 2400, 'discount_price': 240, 'unit': '1piece'},
            {'name': "3½' Fancy Pipe Out", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 3200, 'discount_price': 320, 'unit': '1piece'},
            {'name': "3½' Fancy Pipe Out (2 Pcs)", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 6500, 'discount_price': 650, 'unit': 'BOX'},
            {'name': "4' Fancy Pipe Out", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 4200, 'discount_price': 420, 'unit': '1Piece'},
            {'name': "4' Fancy Pipe Out (2 Pcs)", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 7900, 'discount_price': 790, 'unit': 'BOX'},
            {'name': "4½' Fancy Pipe Out (2 Pcs)", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 8500, 'discount_price': 850, 'unit': 'BOX'},
            {'name': "5' Mega Fancy Pipe Out (2 Pcs)", 'category': 'SKY NIGHT FANCY CELEBRATIONS', 'original_price': 9500, 'discount_price': 950, 'unit': 'BOX'},
            
            # REPEATING MULTI COLOUR FANCY SHOTS
            {'name': "12 Rider Fancy Shots", 'category': 'REPEATING MULTI COLOUR FANCY SHOTS', 'original_price': 1600, 'discount_price': 160, 'unit': 'BOX'},
            {'name': "12 Multi Colour Fancy Shots", 'category': 'REPEATING MULTI COLOUR FANCY SHOTS', 'original_price': 2200, 'discount_price': 220, 'unit': 'BOX'},
            {'name': "30 Special Multi Colour Fancy Shots", 'category': 'REPEATING MULTI COLOUR FANCY SHOTS', 'original_price': 4500, 'discount_price': 450, 'unit': 'BOX'},
            {'name': "60 Multi Colour Fancy Shots", 'category': 'REPEATING MULTI COLOUR FANCY SHOTS', 'original_price': 8400, 'discount_price': 840, 'unit': 'BOX'},
            {'name': "120 Multi Colour Fancy Shots", 'category': 'REPEATING MULTI COLOUR FANCY SHOTS', 'original_price': 16400, 'discount_price': 1640, 'unit': 'BOX'},
            {'name': "240 Multi Colour Fancy Shots", 'category': 'REPEATING MULTI COLOUR FANCY SHOTS', 'original_price': 32000, 'discount_price': 3200, 'unit': 'BOX'},
            {'name': "20x 2.5' Set out Grand Fancy", 'category': 'REPEATING MULTI COLOUR FANCY SHOTS', 'original_price': 27000, 'discount_price': 2700, 'unit': 'BOX'},
            {'name': "30x 2.5' Set out Grand Fancy", 'category': 'REPEATING MULTI COLOUR FANCY SHOTS', 'original_price': 36000, 'discount_price': 3600, 'unit': 'BOX'},
            {'name': "10x10 IPL Set out", 'category': 'REPEATING MULTI COLOUR FANCY SHOTS', 'original_price': 39000, 'discount_price': 3900, 'unit': 'BOX'},
            {'name': "25 Multi Rider fancy Shots", 'category': 'REPEATING MULTI COLOUR FANCY SHOTS', 'original_price': 2800, 'discount_price': 280, 'unit': 'BOX'},
            
            # NIGHT FOUNTAIN CELEBRATIONS
            {'name': "4' Angry Bird Shower", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 600, 'discount_price': 60, 'unit': '1piece'},
            {'name': "Asrafi (5 Pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 640, 'discount_price': 64, 'unit': 'BOX'},
            {'name': "Ganga Zamuna Shower(5 Pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 980, 'discount_price': 98, 'unit': 'BOX'},
            {'name': "Colour Rain (5 Pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 1300, 'discount_price': 130, 'unit': 'BOX'},
            {'name': "Feather pop Shower (5 Pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 1350, 'discount_price': 135, 'unit': 'BOX'},
            {'name': "Golden Shower (5 Pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 1400, 'discount_price': 140, 'unit': 'BOX'},
            {'name': "Disco Shower (5 Pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 1450, 'discount_price': 145, 'unit': 'BOX'},
            {'name': "2' Sun Feast Colour Fountain (5 Pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 1700, 'discount_price': 170, 'unit': 'BOX'},
            {'name': "Mini Siren(5 pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 1900, 'discount_price': 190, 'unit': 'BOX'},
            {'name': "Mega Siren (3 Pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 1980, 'discount_price': 198, 'unit': 'BOX'},
            {'name': "3' Red Sun/ ICE MAGIC Fountain", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 2200, 'discount_price': 220, 'unit': 'BOX'},
            {'name': "Tin Beer Fountain (1 Pc)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 1100, 'discount_price': 110, 'unit': '1Piece'},
            {'name': "Apple / Pogo Shower Boom (5 pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 2250, 'discount_price': 225, 'unit': 'BOX'},
            {'name': "Cocktail Dancing WALA EFECT (3 Pcs)", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 3500, 'discount_price': 350, 'unit': 'BOX'},
            {'name': "Water Falls Fountain", 'category': 'NIGHT FOUNTAIN CELEBRATIONS', 'original_price': 2250, 'discount_price': 225, 'unit': '1Piece'},
            
            # NIGHT FANCY CELEBRATION
            {'name': "Photo Flash (5 Pcs)", 'category': 'NIGHT FANCY CELEBRATION', 'original_price': 780, 'discount_price': 78, 'unit': 'BOX'},
            {'name': "Colour Changing Butterfly (10 Pcs)", 'category': 'NIGHT FANCY CELEBRATION', 'original_price': 1300, 'discount_price': 130, 'unit': 'BOX'},
            {'name': "Colour Smoke Candle Celebration big (3 Pcs)", 'category': 'NIGHT FANCY CELEBRATION', 'original_price': 1900, 'discount_price': 190, 'unit': 'BOX'},
            {'name': "Helicopter (5 pcs)", 'category': 'NIGHT FANCY CELEBRATION', 'original_price': 1100, 'discount_price': 110, 'unit': 'BOX'},
            {'name': "Colour Bambaram red/green (10 Pcs)", 'category': 'NIGHT FANCY CELEBRATION', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            {'name': "Peacock Fancy", 'category': 'NIGHT FANCY CELEBRATION', 'original_price': 1700, 'discount_price': 170, 'unit': '1Piece'},
            {'name': "Bada Peacock", 'category': 'NIGHT FANCY CELEBRATION', 'original_price': 3900, 'discount_price': 390, 'unit': '1Piece'},
            {'name': "Lotus Wheel 4x4 (5 Pcs)", 'category': 'NIGHT FANCY CELEBRATION', 'original_price': 2200, 'discount_price': 220, 'unit': '1Pack'},
            {'name': "Old is Gold Colour Olai Vedi (25 Pcs)", 'category': 'NIGHT FANCY CELEBRATION', 'original_price': 2000, 'discount_price': 200, 'unit': '1Pack'},
            {'name': "Shooting Gun Crackling (5 Pcs)", 'category': 'NIGHT FANCY CELEBRATION', 'original_price': 2250, 'discount_price': 225, 'unit': '1Pack'},
            
            # LADDU FOUNTAIN
            {'name': "Chun Mun Laddu (5 Pcs)", 'category': 'LADDU FOUNTAIN', 'original_price': 2200, 'discount_price': 220, 'unit': 'BOX'},
            {'name': "Mega Deluxe Fountain (4 Pcs)", 'category': 'LADDU FOUNTAIN', 'original_price': 6000, 'discount_price': 600, 'unit': 'BOX'},
            {'name': "COLOUR CHANGING MAGIC STAR (5Pcs)", 'category': 'LADDU FOUNTAIN', 'original_price': 4500, 'discount_price': 450, 'unit': 'BOX'},
            
            # SNAKE and CARTOON
            {'name': "3 In 1 Colour fog stick (3 Pcs)", 'category': 'SNAKE and CARTOON', 'original_price': 300, 'discount_price': 30, 'unit': 'BOX'},
            {'name': "Zee Boomba (10 Pcs)", 'category': 'SNAKE and CARTOON', 'original_price': 150, 'discount_price': 15, 'unit': 'BOX'},
            {'name': "Electric Stone (10 Pcs)", 'category': 'SNAKE and CARTOON', 'original_price': 160, 'discount_price': 16, 'unit': 'BOX'},
            {'name': "Cartoon Pots (10 Pcs)", 'category': 'SNAKE and CARTOON', 'original_price': 250, 'discount_price': 25, 'unit': 'BOX'},
            {'name': "Snake Cartoon (5 Pcs)", 'category': 'SNAKE and CARTOON', 'original_price': 300, 'discount_price': 30, 'unit': 'BOX'},
            {'name': "Block Perpant (50 Tablets)", 'category': 'SNAKE and CARTOON', 'original_price': 280, 'discount_price': 28, 'unit': 'BOX'},
            {'name': "Kit Kat (10 Pcs)", 'category': 'SNAKE and CARTOON', 'original_price': 350, 'discount_price': 35, 'unit': 'BOX'},
            
            # CHILDRENS ROLL CAP/GUN
            {'name': "Roll Cab", 'category': 'CHILDRENS ROLL CAP/GUN', 'original_price': 76, 'discount_price': 0, 'unit': 'BOX'},
            {'name': "Small Size Gun", 'category': 'CHILDRENS ROLL CAP/GUN', 'original_price': 70, 'discount_price': 0, 'unit': 'BOX'},
            {'name': "Medium Size Gun", 'category': 'CHILDRENS ROLL CAP/GUN', 'original_price': 100, 'discount_price': 0, 'unit': 'BOX'},
            {'name': "Mega Gun", 'category': 'CHILDRENS ROLL CAP/GUN', 'original_price': 170, 'discount_price': 0, 'unit': 'BOX'},
            {'name': "Ring Cap Gun", 'category': 'CHILDRENS ROLL CAP/GUN', 'original_price': 100, 'discount_price': 0, 'unit': 'BOX'},
            
            # COLOUR MATCHES
            {'name': "Deluxe Match (100 Sticks)", 'category': 'COLOUR MATCHES', 'original_price': 800, 'discount_price': 80, 'unit': 'BOX'},
            {'name': "Hero Match (100 Sticks)", 'category': 'COLOUR MATCHES', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            {'name': "Mega Laptop Match (100 Sticks)", 'category': 'COLOUR MATCHES', 'original_price': 2500, 'discount_price': 250, 'unit': 'BOX'},
            {'name': "VIP Top 10 Laptop Match (100 Sticks)", 'category': 'COLOUR MATCHES', 'original_price': 2900, 'discount_price': 290, 'unit': 'BOX'},
            
            # NEW ARRIVALS
            {'name': "Jungle Beat Sound (5 Pcs)", 'category': 'NEW ARRIVALS', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            {'name': "Shin chan (5 Pcs)", 'category': 'NEW ARRIVALS', 'original_price': 1500, 'discount_price': 150, 'unit': 'BOX'},
            {'name': "90 Digital Cracker (3 Pcs)", 'category': 'NEW ARRIVALS', 'original_price': 1700, 'discount_price': 170, 'unit': 'BOX'},
            {'name': "Emu Egg (2 Pcs)", 'category': 'NEW ARRIVALS', 'original_price': 2500, 'discount_price': 250, 'unit': 'BOX'},
            {'name': "Dancing Umberla", 'category': 'NEW ARRIVALS', 'original_price': 2200, 'discount_price': 220, 'unit': '1Piece'},
            {'name': "Lolly Pop Flash Stick (5 Pcs)", 'category': 'NEW ARRIVALS', 'original_price': 2400, 'discount_price': 240, 'unit': 'BOX'},
            {'name': "WIRE CHAKKAR (10 PCS)", 'category': 'NEW ARRIVALS', 'original_price': 2200, 'discount_price': 220, 'unit': 'BOX'},
            {'name': "AK 47 Machine Gun", 'category': 'NEW ARRIVALS', 'original_price': 2300, 'discount_price': 230, 'unit': '1Piece'},
            {'name': "Selfi Stick (5 Pcs)", 'category': 'NEW ARRIVALS', 'original_price': 1600, 'discount_price': 160, 'unit': 'BOX'},
            {'name': "Bat & Smoke Ball", 'category': 'NEW ARRIVALS', 'original_price': 2400, 'discount_price': 240, 'unit': '1Piece'},
            {'name': "Magic Digital Sound Wala", 'category': 'NEW ARRIVALS', 'original_price': 2200, 'discount_price': 220, 'unit': '1Piece'},
            {'name': "Star Show Popcorn Crackling", 'category': 'NEW ARRIVALS', 'original_price': 2200, 'discount_price': 220, 'unit': '1Piece'},
            {'name': "ICE CONE FALLS (2 Pcs)", 'category': 'NEW ARRIVALS', 'original_price': 2800, 'discount_price': 280, 'unit': 'BOX'},
            {'name': "GenZ Mobile Shower", 'category': 'NEW ARRIVALS', 'original_price': 2000, 'discount_price': 200, 'unit': '1 Piece'},
            {'name': "KADHAYUTHAM FALLS", 'category': 'NEW ARRIVALS', 'original_price': 1900, 'discount_price': 190, 'unit': '1 Piece'},
            {'name': "CYLINDER BOMB", 'category': 'NEW ARRIVALS', 'original_price': 1600, 'discount_price': 160, 'unit': 'BOX'},
            {'name': "SPARKLING SWARD", 'category': 'NEW ARRIVALS', 'original_price': 1400, 'discount_price': 140, 'unit': 'BOX'},
            {'name': "INFINITY STAR CRACKLING FOUNTAIN (3 Pcs)", 'category': 'NEW ARRIVALS', 'original_price': 3900, 'discount_price': 390, 'unit': 'BOX'},
            {'name': "Popcorn Crackling Star", 'category': 'NEW ARRIVALS', 'original_price': 2200, 'discount_price': 220, 'unit': '1Piece'},
            
            # GIFT BOXES
            {'name': "Family Gift Box (21 Items)", 'category': 'GIFT BOXES', 'original_price': 350, 'discount_price': 0, 'unit': 'BOX'},
            {'name': "Premium Gift box", 'category': 'GIFT BOXES', 'original_price': 1600, 'discount_price': 0, 'unit': '1CASE'},
            {'name': "Family Gift Box (25 Items)", 'category': 'GIFT BOXES', 'original_price': 450, 'discount_price': 0, 'unit': 'BOX'},
            {'name': "Family Gift Box (30 Items)", 'category': 'GIFT BOXES', 'original_price': 550, 'discount_price': 0, 'unit': 'BOX'},
            {'name': "Family Gift Box (35 Items)", 'category': 'GIFT BOXES', 'original_price': 650, 'discount_price': 0, 'unit': 'BOX'},
            {'name': "Family Gift Box (40 Items)", 'category': 'GIFT BOXES', 'original_price': 750, 'discount_price': 0, 'unit': 'BOX'},
            {'name': "Family Gift Box (50 Items)", 'category': 'GIFT BOXES', 'original_price': 950, 'discount_price': 0, 'unit': 'BOX'},
            {'name': "Family Gift Box (60 Items)", 'category': 'GIFT BOXES', 'original_price': 1150, 'discount_price': 0, 'unit': 'BOX'},
            
            # COMBO PACKS
            {'name': "3000 Combo Pack", 'category': 'COMBO PACKS', 'original_price': 3000, 'discount_price': 0, 'unit': '1CASE'},
            {'name': "4000 Combo Pack", 'category': 'COMBO PACKS', 'original_price': 4000, 'discount_price': 0, 'unit': '1CASE'},
            {'name': "5000 Combo Pack", 'category': 'COMBO PACKS', 'original_price': 5000, 'discount_price': 0, 'unit': '1CASE'},
            {'name': "7000 Combo Pack", 'category': 'COMBO PACKS', 'original_price': 7000, 'discount_price': 0, 'unit': '1CASE'},
            
            # SPECIAL SERIES FANCY SKY SHOTS
            {'name': "Trible ball Fancy Pipe Out", 'category': 'SPECIAL SERIES FANCY SKY SHOTS', 'original_price': 2400, 'discount_price': 240, 'unit': '1piece'},
            {'name': "Nayagara Falls Out", 'category': 'SPECIAL SERIES FANCY SKY SHOTS', 'original_price': 3700, 'discount_price': 370, 'unit': '1piece'},
            {'name': "Double Colour Ball Out", 'category': 'SPECIAL SERIES FANCY SKY SHOTS', 'original_price': 4250, 'discount_price': 425, 'unit': '1Piece'},
            {'name': "Seven Step Fancy Out", 'category': 'SPECIAL SERIES FANCY SKY SHOTS', 'original_price': 4500, 'discount_price': 450, 'unit': '1Piece'},
            {'name': "Digital Crackling Star", 'category': 'SPECIAL SERIES FANCY SKY SHOTS', 'original_price': 3900, 'discount_price': 390, 'unit': '1piece'},
            {'name': "Zumba dance sky out (6Pcs)", 'category': 'SPECIAL SERIES FANCY SKY SHOTS', 'original_price': 2200, 'discount_price': 220, 'unit': 'Box'},
            {'name': "4.5' Wow Series Fancy Pipe Out", 'category': 'SPECIAL SERIES FANCY SKY SHOTS', 'original_price': 4750, 'discount_price': 475, 'unit': '1Piece'},
            {'name': "MAD MAX", 'category': 'SPECIAL SERIES FANCY SKY SHOTS', 'original_price': 740, 'discount_price': 74, 'unit': 'BOX'},
            {'name': "Grizz colour fountain", 'category': 'SPECIAL SERIES FANCY SKY SHOTS', 'original_price': 750, 'discount_price': 75, 'unit': '1 Piece'},
        ]
        
        # Create products
        created_count = 0
        for i, prod_data in enumerate(products_data):
            category = category_map.get(prod_data['category'])
            if not category:
                self.stdout.write(f'Category not found: {prod_data["category"]}, skipping')
                continue
            
            # Generate slug
            slug = prod_data['name'].lower().replace(' ', '-').replace('/', '-').replace('&', 'and').replace('(', '').replace(')', '').replace(',', '').replace('"', '').replace("'", '').replace("'", '')
            
            # Generate SKU
            sku = f'VAS-{i + 1:03d}'
            
            # Determine product type based on category
            product_type = 'single'
            if 'GIFT BOXES' in prod_data['category']:
                product_type = 'gift_box'
            elif 'COMBO PACKS' in prod_data['category']:
                product_type = 'combo'
            elif 'BOX' in prod_data['unit'] or 'Pcs' in prod_data['unit']:
                product_type = 'box'
            
            # Determine safety level
            safety_level = 'medium'
            if any(word in prod_data['category'] for word in ['BOMB', 'ROCKET', 'CHAKKAR']):
                safety_level = 'high'
            elif any(word in prod_data['category'] for word in ['SPARKLERS', 'CANDLE', 'PENCIL']):
                safety_level = 'low'
            
            # Calculate prices (90% discount)
            regular_price = Decimal(str(prod_data['original_price']))
            sale_price = Decimal(str(prod_data['discount_price'])) if prod_data['discount_price'] > 0 else None
            
            # Set pieces based on unit
            pieces = 1
            if '10 Pcs' in prod_data['unit']:
                pieces = 10
            elif '5 Pcs' in prod_data['unit']:
                pieces = 5
            elif '25 Pcs' in prod_data['unit']:
                pieces = 25
            
            Product.objects.create(
                name=prod_data['name'],
                slug=slug,
                sku=sku,
                category=category,
                brand=brand,
                product_type=product_type,
                safety_level=safety_level,
                short_description=f'{prod_data["name"]} - {prod_data["category"]}',
                description=f'{prod_data["name"]} from {prod_data["category"]}. High quality crackers from Vasantham Crackers World with 90% discount offer.',
                regular_price=regular_price,
                sale_price=sale_price,
                stock=100,
                pieces=pieces,
                is_active=True,
                is_featured=False,
                is_new=False,
                is_bestseller=False,
                is_trending=False,
                main_image='images/crackers/placeholder.jpg',
                image_url='images/crackers/placeholder.jpg',
                additional_images=[],
            )
            created_count += 1
            
            if created_count % 20 == 0:
                self.stdout.write(f'Created {created_count} products...')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created_count} Vasantham products'))
        self.stdout.write(f'Total categories: {Category.objects.count()}')
        self.stdout.write(f'Total products: {Product.objects.count()}')