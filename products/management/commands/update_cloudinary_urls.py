"""
Django management command to update Product main_image fields with Cloudinary URLs.
Reads from cloudinary_image_mapping.txt and updates database records.
"""

from django.core.management.base import BaseCommand
from products.models import Product
from pathlib import Path


class Command(BaseCommand):
    help = 'Update Product main_image URLs from Cloudinary mapping file'

    def handle(self, *args, **options):
        mapping_file = Path('cloudinary_image_mapping.txt')
        
        if not mapping_file.exists():
            self.stdout.write(
                self.style.ERROR(f'Mapping file not found: {mapping_file}')
            )
            return
        
        # Read mapping file
        mappings = {}
        with open(mapping_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '|' in line and not line.startswith('Product'):
                    parts = line.split('|')
                    if len(parts) == 2:
                        slug = parts[0].strip()
                        url = parts[1].strip()
                        mappings[slug] = url
        
        self.stdout.write(f'Loaded {len(mappings)} URL mappings from file')
        
        # Update products
        updated_count = 0
        not_found_count = 0
        
        for slug, cloudinary_url in mappings.items():
            try:
                product = Product.objects.filter(slug=slug).first()
                if product:
                    product.main_image = cloudinary_url
                    product.save(update_fields=['main_image'])
                    updated_count += 1
                    self.stdout.write(f'✅ Updated: {product.name} -> {cloudinary_url[:50]}...')
                else:
                    not_found_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'⚠️  Product not found: {slug}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error updating {slug}: {str(e)}')
                )
        
        self.stdout.write(self.style.SUCCESS(
            f'\n{"="*50}\n'
            f'Update complete!\n'
            f'✅ Successfully updated: {updated_count}\n'
            f'⚠️  Products not found: {not_found_count}\n'
            f'{"="*50}'
        ))
