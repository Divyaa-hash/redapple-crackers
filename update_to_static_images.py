import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

# Get all products that don't use static images
products = Product.objects.filter(is_active=True).exclude(main_image__startswith='images/crackers/')

# Map products to static images based on their current image filename
static_folder = 'static/images/crackers'

for product in products:
    if product.main_image:
        # Convert ImageFieldFile to string
        image_path = str(product.main_image)
        
        # Extract filename from current path (e.g., products/20251010060432_OcVGhe9.jpg -> 20251010060432_OcVGhe9.jpg)
        filename = image_path.split('/')[-1]
        
        # Check if this file exists in static folder
        static_path = f'images/crackers/{filename}'
        full_static_path = os.path.join(static_folder, filename)
        
        if os.path.exists(full_static_path):
            product.main_image = static_path
            product.save()
            print(f'Updated {product.name[:30]}: {product.main_image}')
        else:
            # Try without the random suffix
            base_filename = filename.split('_')[0] + '.jpg' if '_' in filename else filename
            static_path_base = f'images/crackers/{base_filename}'
            full_static_path_base = os.path.join(static_folder, base_filename)
            
            if os.path.exists(full_static_path_base):
                product.main_image = static_path_base
                product.save()
                print(f'Updated {product.name[:30]}: {product.main_image}')
            else:
                print(f'Not found: {filename} for {product.name[:30]}')

print('Update complete')
