import os
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.serializers import deserialize
from products.models import Product, Category


@receiver(post_migrate)
def seed_products_and_categories(sender, **kwargs):
    """Auto-seed products and categories after migrations"""
    if sender.name == 'products':
        # Check if products already exist
        if Product.objects.exists():
            print("Products already exist, skipping seed")
            return

        # Get base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Load categories
        categories_file = os.path.join(base_dir, 'categories_fixture.json')
        if os.path.exists(categories_file):
            try:
                with open(categories_file, 'r', encoding='utf-8') as f:
                    categories_data = f.read()
                
                Category.objects.all().delete()
                for obj in deserialize('json', categories_data):
                    obj.save()
                
                print(f"Loaded {Category.objects.count()} categories")
            except Exception as e:
                print(f"Error loading categories: {e}")
        else:
            print(f"Categories file not found: {categories_file}")

        # Load products
        products_file = os.path.join(base_dir, 'products_fixture.json')
        if os.path.exists(products_file):
            try:
                with open(products_file, 'r', encoding='utf-8') as f:
                    products_data = f.read()
                
                Product.objects.all().delete()
                for obj in deserialize('json', products_data):
                    obj.save()
                
                print(f"Loaded {Product.objects.count()} products")
            except Exception as e:
                print(f"Error loading products: {e}")
        else:
            print(f"Products file not found: {products_file}")
