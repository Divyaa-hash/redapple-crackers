import os
import django
from datetime import datetime, timedelta
import random
from django.utils.text import slugify
import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category, Brand, Festival

# Create categories
categories = [
    {'name': 'Sparklers', 'description': 'Beautiful sparklers for all occasions'},
    {'name': 'Rockets', 'description': 'High-flying rockets for spectacular displays'},
    {'name': 'Fountains', 'description': 'Colorful fountain fireworks'},
    {'name': 'Crackers', 'description': 'Traditional crackers for celebrations'},
    {'name': 'Gift Boxes', 'description': 'Premium gift box collections'},
    {'name': 'Combos', 'description': 'Combo packs for best value'},
]

for cat_data in categories:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'description': cat_data['description'],
            'slug': slugify(cat_data['name']) + str(random.randint(1, 1000))
        }
    )
    if created:
        print(f"Created category: {category.name}")

# Create brands
brand, _ = Brand.objects.get_or_create(
    name='RedApple Premium',
    defaults={'description': 'Premium quality fireworks from RedApple'}
)

# Create festival
from datetime import datetime, timedelta

festival, _ = Festival.objects.get_or_create(
    name='Diwali',
    defaults={
        'description': 'Festival of Lights',
        'start_date': datetime.now().date() + timedelta(days=30),
        'end_date': datetime.now().date() + timedelta(days=32),
        'is_active': True
    }
)

# Create products
products_data = [
    {
        'name': 'Premium Sky Rocket',
        'description': 'High-quality sky rocket with brilliant display',
        'regular_price': 299,
        'category': 'Rockets',
        'stock': 50,
        'is_active': True,
        'is_trending': True,
        'is_featured': True,
    },
    {
        'name': 'Golden Sparkler Set',
        'description': 'Premium golden sparklers pack of 25',
        'regular_price': 199,
        'category': 'Sparklers',
        'stock': 100,
        'is_active': True,
        'is_new': True,
    },
    {
        'name': 'Colorful Fountain',
        'description': 'Multi-color fountain firework with 5-minute display',
        'regular_price': 499,
        'sale_price': 399,
        'category': 'Fountains',
        'stock': 30,
        'is_active': True,
    },
    {
        'name': 'Premium Cracker Box',
        'description': 'Box of 50 premium crackers for celebrations',
        'regular_price': 599,
        'category': 'Crackers',
        'stock': 20,
        'is_active': True,
        'is_bestseller': True,
    },
    {
        'name': 'Diwali Special Gift Box',
        'description': 'Complete Diwali celebration gift box',
        'regular_price': 1499,
        'category': 'Gift Boxes',
        'stock': 25,
        'is_active': True,
        'is_featured': True,
    },
    {
        'name': 'Ultimate Combo Pack',
        'description': 'Best value combo with rockets, sparklers, and fountains',
        'regular_price': 999,
        'category': 'Combos',
        'stock': 15,
        'is_active': True,
        'is_bestseller': True,
    },
    {
        'name': 'Rainbow Sparklers',
        'description': 'Color-changing sparklers pack',
        'regular_price': 249,
        'category': 'Sparklers',
        'stock': 75,
        'is_active': True,
        'is_new': True,
    },
    {
        'name': 'Night Sky Rocket',
        'description': 'Long-lasting rocket with golden sparks',
        'regular_price': 399,
        'category': 'Rockets',
        'stock': 40,
        'is_active': True,
        'is_trending': True,
    },
    {
        'name': 'Premium Flower Pot',
        'description': 'Beautiful flower pot firework',
        'regular_price': 349,
        'category': 'Fountains',
        'stock': 45,
        'is_active': True,
        'is_new': True,
    },
    {
        'name': 'Mega Rocket Set',
        'description': 'Set of 10 premium rockets',
        'regular_price': 2499,
        'sale_price': 1999,
        'category': 'Rockets',
        'stock': 18,
        'is_active': True,
        'is_featured': True,
    },
    {
        'name': 'Celebration Crackers',
        'description': 'Premium crackers for celebrations',
        'regular_price': 449,
        'category': 'Crackers',
        'stock': 35,
        'is_active': True,
        'is_trending': True,
    },
    {
        'name': 'Wedding Gift Box',
        'description': 'Special wedding celebration pack',
        'regular_price': 2999,
        'category': 'Gift Boxes',
        'stock': 12,
        'is_active': True,
        'is_featured': True,
    },
]

for product_data in products_data:
    category = Category.objects.get(name=product_data['category'])
    
    # Generate unique SKU and slug
    sku = f"RA-{category.name[:3].upper()}-{random.randint(1000, 9999)}"
    slug = slugify(product_data['name']) + f"-{random.randint(100, 999)}"
    
    # Download AI-style image from Unsplash
    image_urls = {
        'Rockets': 'https://images.unsplash.com/photo-1512496732179-4ecb94b36b92?w=400&h=300&fit=crop',
        'Sparklers': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400&h=300&fit=crop',
        'Fountains': 'https://images.unsplash.com/photo-1524779072457-46349b03d7ce?w=400&h=300&fit=crop',
        'Crackers': 'https://images.unsplash.com/photo-1533929388968-2b9b8dc43521?w=400&h=300&fit=crop',
        'Gift Boxes': 'https://images.unsplash.com/photo-1513885535751-8b9238bd345a?w=400&h=300&fit=crop',
        'Combos': 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=400&h=300&fit=crop',
    }
    
    try:
        response = requests.get(image_urls.get(category.name, image_urls['Rockets']))
        image_file = SimpleUploadedFile(
            f"{slug}.jpg",
            response.content,
            content_type="image/jpeg"
        )
    except:
        # Fallback to placeholder
        img = Image.new('RGB', (400, 300), color=(239, 68, 68))
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        image_file = SimpleUploadedFile("placeholder.jpg", img_io.read(), content_type="image/jpeg")
    
    product, created = Product.objects.get_or_create(
        sku=sku,
        defaults={
            'name': product_data['name'],
            'slug': slug,
            'description': product_data['description'],
            'regular_price': product_data['regular_price'],
            'sale_price': product_data.get('sale_price'),
            'category': category,
            'brand': brand,
            'festival': festival,
            'stock': product_data['stock'],
            'main_image': image_file,
            'is_active': product_data['is_active'],
            'is_trending': product_data.get('is_trending', False),
            'is_featured': product_data.get('is_featured', False),
            'is_bestseller': product_data.get('is_bestseller', False),
            'is_new': product_data.get('is_new', False),
        }
    )
    
    if created:
        print(f"Created product: {product.name} (SKU: {product.sku})")
    else:
        print(f"Product already exists: {product.name}")

print("\nProducts added successfully!")
print(f"Total products: {Product.objects.count()}")