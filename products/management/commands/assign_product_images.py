import sys
import io
import os
import re
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Assign correct images to products based on available images'

    def handle(self, *args, **options):
        # Set UTF-8 encoding for stdout
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

        # Get all available images
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

        # Image name to product name mapping
        # This will help match images to products
        updated_count = 0
        not_found_count = 0

        for product in Product.objects.filter(is_active=True, order__gt=0):
            try:
                # Try to find matching image for this product
                matched_image = self.find_matching_image(product.name, image_files)

                if matched_image:
                    # Update product image
                    product.image_url = f'images/crackers/{matched_image}'
                    product.save()
                    updated_count += 1
                    self.stdout.write(f"Updated: {product.name} -> {matched_image}")
                else:
                    not_found_count += 1
                    self.stdout.write(f"No image found: {product.name}")

            except Exception as e:
                self.stdout.write(f"Error updating {product.name}: {e}")

        self.stdout.write(f"\nSummary:")
        self.stdout.write(f"Updated: {updated_count} products")
        self.stdout.write(f"Not found: {not_found_count} products")

    def find_matching_image(self, product_name, image_files):
        """Find the best matching image for a product"""
        # Clean product name for matching
        clean_name = product_name.lower()
        clean_name = re.sub(r'[^\w\s-]', '', clean_name)  # Remove special chars
        clean_name = re.sub(r'\s+', '-', clean_name)  # Replace spaces with hyphens

        # Try exact match first
        for ext in ['.webp', '.jpg', '.jpeg', '.png']:
            exact_match = f"{clean_name}{ext}"
            if exact_match in image_files:
                return exact_match

        # Try partial match (contains product name)
        for image in image_files:
            image_clean = image.lower()
            image_clean = re.sub(r'[^\w\s-]', '', image_clean)
            image_clean = re.sub(r'\s+', '-', image_clean)

            # Check if image name contains product name
            if clean_name in image_clean or image_clean in clean_name:
                return image

        # Try matching key words
        keywords = self.extract_keywords(product_name)
        for image in image_files:
            image_lower = image.lower()
            matched_keywords = 0
            for keyword in keywords:
                if keyword.lower() in image_lower:
                    matched_keywords += 1
            # If more than 1 keyword matches, it's a good match
            if matched_keywords >= 1:
                return image

        return None

    def extract_keywords(self, product_name):
        """Extract key words from product name for matching"""
        # Remove common words and special characters
        ignore_words = ['pcs', 'box', 'pkt', 'the', 'and', 'or', 'with', 'for', 'in', 'on', 'at']
        words = re.findall(r'\b\w+\b', product_name.lower())
        keywords = [word for word in words if word not in ignore_words and len(word) > 2]
        return keywords
