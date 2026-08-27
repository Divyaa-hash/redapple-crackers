"""
Script to upload existing product images to Cloudinary and update database.
Run this locally where your media files exist.
"""

import os
import django
import cloudinary.uploader
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product
from django.conf import settings

# Cloudinary configuration (update these with your credentials)
CLOUDINARY_CLOUD_NAME = 'agkeucqd'
CLOUDINARY_API_KEY = '647136372246985'
CLOUDINARY_API_SECRET = 'ixaCuXNAQ7-TFJgmXEY2SzwE9bE'

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

def upload_product_images():
    """Upload all product images to Cloudinary and update database"""
    
    products = Product.objects.filter(main_image__isnull=False).exclude(main_image='')
    
    print(f"Found {products.count()} products with images to upload")
    
    success_count = 0
    error_count = 0
    
    for product in products:
        try:
            # Get local image path
            if product.main_image and hasattr(product.main_image, 'path'):
                local_path = product.main_image.path
                
                # Check if file exists locally
                if not os.path.exists(local_path):
                    print(f"⚠️  File not found: {local_path}")
                    error_count += 1
                    continue
                
                print(f"Uploading: {product.name} from {local_path}")
                
                # Upload to Cloudinary
                upload_result = cloudinary.uploader.upload(
                    local_path,
                    folder='products',
                    public_id=f"products/{product.slug}",
                    resource_type='image',
                    overwrite=True
                )
                
                # Update product with Cloudinary URL
                cloudinary_url = upload_result['secure_url']
                product.main_image = cloudinary_url
                product.save(
                    update_fields=['main_image']
                )
                
                print(f"✅ Uploaded: {product.name} -> {cloudinary_url}")
                success_count += 1
                
            else:
                print(f"⚠️  No valid image path for: {product.name}")
                error_count += 1
                
        except Exception as e:
            print(f"❌ Error uploading {product.name}: {str(e)}")
            error_count += 1
    
    print(f"\n{'='*50}")
    print(f"Upload complete!")
    print(f"✅ Successfully uploaded: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Starting product image upload to Cloudinary...")
    print(f"Cloud Name: {CLOUDINARY_CLOUD_NAME}")
    print(f"API Key: {CLOUDINARY_API_KEY}")
    print()
    
    confirm = input("Do you want to proceed? (yes/no): ")
    if confirm.lower() == 'yes':
        upload_product_images()
    else:
        print("Upload cancelled.")
