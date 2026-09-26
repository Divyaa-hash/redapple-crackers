import sys
import io
import os
import re
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Match Excel products to images using actual product names'

    def handle(self, *args, **options):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

        image_dir = 'static/images/crackers/'
        if not os.path.exists(image_dir):
            self.stdout.write(f"Image directory not found: {image_dir}")
            return

        # Get all image files and create normalized mapping
        image_files = []
        image_mapping = {}
        
        for file in os.listdir(image_dir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                image_files.append(file)
                # Create normalized name for matching
                normalized = self.normalize_name(file)
                image_mapping[normalized] = file

        self.stdout.write(f"Found {len(image_files)} image files")
        self.stdout.write(f"Created {len(image_mapping)} normalized mappings")

        # Get only Excel products (with order field)
        products = Product.objects.filter(order__gt=0).order_by('order')
        self.stdout.write(f"Processing {products.count()} Excel products")

        updated_count = 0
        logo_count = 0
        not_found_count = 0

        for product in products:
            # Normalize product name for matching
            product_normalized = self.normalize_name(product.name)
            
            # Try exact match first
            if product_normalized in image_mapping:
                product.image_url = f'images/crackers/{image_mapping[product_normalized]}'
                product.save()
                updated_count += 1
                self.stdout.write(f"MATCHED: {product.name} -> {image_mapping[product_normalized]}")
                continue
            
            # Try partial match
            matched = False
            for norm_image, image_file in image_mapping.items():
                # Check if product name is contained in image name or vice versa
                if (product_normalized in norm_image and len(product_normalized) > 5) or \
                   (norm_image in product_normalized and len(norm_image) > 5):
                    product.image_url = f'images/crackers/{image_file}'
                    product.save()
                    updated_count += 1
                    self.stdout.write(f"PARTIAL: {product.name} -> {image_file}")
                    matched = True
                    break
            
            if matched:
                continue
            
            # No match found - use Red Apple logo
            product.image_url = 'images/crackers/logo.jpg'
            product.save()
            logo_count += 1
            self.stdout.write(f"LOGO: {product.name} -> logo.jpg")

        self.stdout.write(f"\nSummary:")
        self.stdout.write(f"Matched: {updated_count} products")
        self.stdout.write(f"Logo fallback: {logo_count} products")
        self.stdout.write(f"Total: {updated_count + logo_count} products")

    def normalize_name(self, name):
        """Normalize name for matching - remove special chars, spaces, extensions"""
        # Remove file extension
        name = re.sub(r'\.(jpg|jpeg|png|webp|gif)$', '', name, flags=re.IGNORECASE)
        
        # Convert to lowercase
        name = name.lower()
        
        # Remove special characters and spaces
        name = re.sub(r'[^\w\s-]', '', name)
        name = re.sub(r'\s+', '', name)
        name = re.sub(r'-', '', name)
        
        # Remove common words
        ignore_words = ['pcs', 'box', 'pkt', 'the', 'and', 'or', 'with', 'for', 'in', 'on', 'at', 'of']
        words = name.split()
        words = [w for w in words if w not in ignore_words and len(w) > 2]
        
        return ''.join(words)
