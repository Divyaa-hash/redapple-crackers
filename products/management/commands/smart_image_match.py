import sys
import io
import os
import re
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Smart image matching for Excel products'

    def handle(self, *args, **options):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

        image_dir = 'static/images/crackers/'
        if not os.path.exists(image_dir):
            self.stdout.write(f"Image directory not found: {image_dir}")
            return

        # Get all image files
        image_files = []
        for file in os.listdir(image_dir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                image_files.append(file)

        self.stdout.write(f"Found {len(image_files)} image files")

        # Get only Excel products
        products = Product.objects.filter(order__gt=0).order_by('order')
        self.stdout.write(f"Processing {products.count()} Excel products")

        updated_count = 0
        logo_count = 0

        for product in products:
            matched_image = self.smart_match(product.name, image_files)
            
            if matched_image:
                product.image_url = f'images/crackers/{matched_image}'
                product.save()
                updated_count += 1
                self.stdout.write(f"MATCHED: {product.name} -> {matched_image}")
            else:
                product.image_url = 'images/crackers/logo.jpg'
                product.save()
                logo_count += 1
                self.stdout.write(f"LOGO: {product.name} -> logo.jpg")

        self.stdout.write(f"\nSummary:")
        self.stdout.write(f"Matched: {updated_count} products")
        self.stdout.write(f"Logo fallback: {logo_count} products")
        self.stdout.write(f"Total: {updated_count + logo_count} products")

    def smart_match(self, product_name, image_files):
        """Smart matching strategy"""
        # Clean product name
        clean_product = self.clean_name(product_name)
        
        # Strategy 1: Exact match (case-insensitive)
        for image in image_files:
            clean_image = self.clean_name(image)
            if clean_product == clean_image:
                return image
        
        # Strategy 2: Partial match (product name in image name)
        for image in image_files:
            clean_image = self.clean_name(image)
            if len(clean_product) > 3 and clean_product in clean_image:
                return image
        
        # Strategy 3: Image name in product name
        for image in image_files:
            clean_image = self.clean_name(image)
            if len(clean_image) > 3 and clean_image in clean_product:
                return image
        
        # Strategy 4: Keyword matching
        product_keywords = self.extract_keywords(product_name)
        if len(product_keywords) >= 2:
            for image in image_files:
                clean_image = self.clean_name(image)
                image_keywords = self.extract_keywords(image)
                matched = sum(1 for kw in product_keywords if kw in clean_image)
                if matched >= 2:
                    return image
        
        return None

    def clean_name(self, name):
        """Clean name for comparison"""
        # Remove extension
        name = re.sub(r'\.(jpg|jpeg|png|webp|gif)$', '', name, flags=re.IGNORECASE)
        # Lowercase
        name = name.lower()
        # Remove special chars and spaces
        name = re.sub(r'[^\w]', '', name)
        return name

    def extract_keywords(self, name):
        """Extract meaningful keywords"""
        # Remove common words
        ignore = ['pcs', 'box', 'pkt', 'the', 'and', 'or', 'with', 'for', 'in', 'on', 'at', 'of', 'new', 'big', 'small']
        words = re.findall(r'\b\w+\b', name.lower())
        keywords = [w for w in words if w not in ignore and len(w) > 2]
        return keywords
