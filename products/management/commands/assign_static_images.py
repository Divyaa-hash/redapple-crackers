from django.core.management.base import BaseCommand
from products.models import Product
import os

class Command(BaseCommand):
    help = 'Assign static images to products based on available image files'

    def handle(self, *args, **options):
        self.stdout.write('Assigning static images to products...')
        
        # Get all image files from static folder
        static_path = 'static/images/crackers'
        if not os.path.exists(static_path):
            self.stdout.write(self.style.ERROR(f'Static path not found: {static_path}'))
            return
        
        # Get all image files
        image_files = []
        for filename in os.listdir(static_path):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                image_files.append(filename)
        
        self.stdout.write(f'Found {len(image_files)} image files')
        
        # Get all products
        products = Product.objects.all()
        self.stdout.write(f'Found {products.count()} products')
        
        # Assign images to products (circular assignment)
        for i, product in enumerate(products):
            if i < len(image_files):
                image_url = f'/static/images/crackers/{image_files[i]}'
                product.image_url = image_url
                product.save()
                self.stdout.write(f'✓ Assigned {image_files[i]} to {product.name}')
            else:
                # Reuse images if we run out
                image_url = f'/static/images/crackers/{image_files[i % len(image_files)]}'
                product.image_url = image_url
                product.save()
                self.stdout.write(f'✓ Reused {image_files[i % len(image_files)]} for {product.name}')
        
        self.stdout.write(self.style.SUCCESS('Image assignment completed!'))
