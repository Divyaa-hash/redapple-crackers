import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category

# Define the category order from user's shop page
category_order = [
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
    "NEWMAD MAX",
    "LADDU FOUNTAIN",
    "SNAKE and CARTOON",
    "CHILDRENS ROLL CAP/GUN",
    "COLOUR MATCHES",
    "NEW ARRIVALS",
    "GIFT BOXES",
    "COMBO PACKS",
    "SPECIAL SERIES FANCY SKY SHOTS",
]

# Update category order
for index, category_name in enumerate(category_order):
    try:
        category = Category.objects.get(name=category_name)
        category.order = index
        category.save()
        print(f'Updated {category_name} to order {index}')
    except Category.DoesNotExist:
        print(f'Category not found: {category_name}')

print('\nCategory order updated successfully!')
