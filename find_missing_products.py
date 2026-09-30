import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Products that were not found
missing_products = [
    "Sony Pixel Shot 54",
    "6' Fancy",
    "5' Fancy",
    "Univercell 30 Shots (2' Comet)",
    "New 10'10 Light Celebration",
    "Pala Sola Kii 3'10",
    "Bharat Ratna 20 Shots (2.5' Comet)",
]

print('Searching for similar products...')
print('=' * 80)

for search_name in missing_products:
    # Search for products containing parts of the name
    search_terms = search_name.split()
    for term in search_terms:
        if len(term) > 2:  # Only search for terms longer than 2 characters
            similar = Product.objects.filter(name__icontains=term)
            if similar.exists():
                print(f'\nSearch term: "{term}"')
                for p in similar:
                    print(f'  Found: {p.name} (ID: {p.id})')
