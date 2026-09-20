import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product

# Categories to keep (from user's shop page)
categories_to_keep = [
    "One sound crackers",
    "PENCIL and (Sattai) TWINGLING STARS",
    "SPARKLERS",
    "FLOWER POTS",
    "GROUND CHAKKARS",
    "SKY ROCKETS",
    "BIJILI/ BOMB ITEMS",
    "PAPER BOMB",
    "Wala",
    "SKY NIGHT FANCY CELEBRATIONS",
    "REPEATING MULTI COLOUR FANCY SHOTS",
    "NIGHT FOUNTAIN CELEBRATIONS",
    "NIGHT FANCY CELEBRATION",
    "LADDU FOUNTAIN",
    "SNAKE and CARTOON",
    "CHILDRENS ROLL CAP/GUN",
    "COLOUR MATCHES",
    "NEW ARRIVALS",
    "GIFT BOXES",
    "COMBO PACKS",
    "SPECIAL SERIES FANCY SKY SHOTS",
]

print(f'Total categories before: {Category.objects.count()}')
print(f'Total products before: {Product.objects.count()}')

# Delete categories not in the keep list
deleted_categories = 0
deleted_products = 0

for category in Category.objects.all():
    if category.name not in categories_to_keep:
        product_count = category.products.count()
        category.delete()
        deleted_categories += 1
        deleted_products += product_count
        print(f'Deleted category: {category.name} ({product_count} products)')

print(f'\nDeleted {deleted_categories} categories')
print(f'Deleted {deleted_products} products')
print(f'\nTotal categories after: {Category.objects.count()}')
print(f'Total products after: {Product.objects.count()}')

print('\nRemaining categories:')
for category in Category.objects.all():
    print(f'  - {category.name} ({category.products.count()} products)')
