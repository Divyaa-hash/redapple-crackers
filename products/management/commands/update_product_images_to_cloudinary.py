from django.core.management.base import BaseCommand
from products.models import Product
import json
import os


class Command(BaseCommand):
    help = 'Update product images to Cloudinary URLs using actual uploaded URLs'

    def handle(self, *args, **options):
        # Load the actual Cloudinary URL mapping
        # File is in project root
        import django
        from django.conf import settings
        mapping_file = os.path.join(settings.BASE_DIR, 'cloudinary_url_mapping.json')
        
        try:
            with open(mapping_file, 'r') as f:
                url_mapping = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Could not find cloudinary_url_mapping.json at {mapping_file}'))
            return
        
        products = Product.objects.filter(main_image__isnull=False).exclude(main_image='')
        updated_count = 0
        skipped_count = 0
        not_found_count = 0
        
        for product in products:
            # Convert ImageFieldFile to string for checking
            image_path = str(product.main_image) if product.main_image else ''
            
            # Check if current image is a local path (not a URL)
            if image_path and not image_path.startswith('http'):
                # Try to find the product in the mapping
                if product.slug in url_mapping:
                    cloudinary_url = url_mapping[product.slug]
                    # Update to Cloudinary URL
                    product.main_image = cloudinary_url
                    product.save(update_fields=['main_image'])
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Updated: {product.name} -> {cloudinary_url}'))
                else:
                    not_found_count += 1
                    self.stdout.write(self.style.WARNING(f'Not found in mapping: {product.name} (slug: {product.slug})'))
            elif image_path and image_path.startswith('http'):
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f'Skipped (already Cloudinary): {product.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nUpdated {updated_count} products to Cloudinary URLs'))
        self.stdout.write(self.style.WARNING(f'Skipped {skipped_count} products (already Cloudinary)'))
        self.stdout.write(self.style.WARNING(f'Not found in mapping: {not_found_count} products'))
