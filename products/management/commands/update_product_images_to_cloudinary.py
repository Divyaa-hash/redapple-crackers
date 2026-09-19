from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Update product images to Cloudinary URLs'

    def handle(self, *args, **options):
        products = Product.objects.filter(main_image__isnull=False).exclude(main_image='')
        updated_count = 0
        skipped_count = 0
        
        for product in products:
            # Convert ImageFieldFile to string for checking
            image_path = str(product.main_image) if product.main_image else ''
            
            # Check if current image is a local path (not a URL)
            if image_path and not image_path.startswith('http'):
                # Generate Cloudinary URL based on product slug
                # Use the slug to create a consistent Cloudinary URL
                cloudinary_url = f'https://res.cloudinary.com/agkeucqd/image/upload/products/{product.slug}'
                
                # Update to Cloudinary URL
                product.main_image = cloudinary_url
                product.save(update_fields=['main_image'])
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'Updated: {product.name} -> {cloudinary_url}'))
            elif image_path and image_path.startswith('http'):
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f'Skipped (already Cloudinary): {product.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nUpdated {updated_count} products to Cloudinary URLs'))
        self.stdout.write(self.style.WARNING(f'Skipped {skipped_count} products'))
