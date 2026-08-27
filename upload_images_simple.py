"""
Simple script to upload product images to Cloudinary without database access.
Scans media/products folder and uploads all images to Cloudinary.
"""

import os
import cloudinary.uploader
from pathlib import Path

# Cloudinary configuration
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

def upload_images_from_folder():
    """Upload all images from media/products folder to Cloudinary"""
    
    media_folder = Path('media/products')
    
    if not media_folder.exists():
        print(f"❌ Media folder not found: {media_folder}")
        return
    
    # Get all image files
    image_files = list(media_folder.glob('*.jpg')) + list(media_folder.glob('*.jpeg')) + list(media_folder.glob('*.png'))
    
    if not image_files:
        print(f"❌ No images found in {media_folder}")
        return
    
    print(f"Found {len(image_files)} images to upload")
    print()
    
    # Create output file for mapping
    output_file = open('cloudinary_image_mapping.txt', 'w')
    output_file.write("Product Slug | Cloudinary URL\n")
    output_file.write("="*80 + "\n\n")
    
    success_count = 0
    error_count = 0
    
    for image_file in image_files:
        try:
            # Extract product slug from filename (remove extension)
            product_slug = image_file.stem
            
            print(f"Uploading: {image_file.name}")
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                str(image_file),
                folder='products',
                public_id=f"products/{product_slug}",
                resource_type='image',
                overwrite=True
            )
            
            cloudinary_url = upload_result['secure_url']
            
            print(f"✅ Uploaded: {image_file.name}")
            print(f"   URL: {cloudinary_url}")
            print()
            
            # Write to mapping file
            output_file.write(f"{product_slug} | {cloudinary_url}\n")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error uploading {image_file.name}: {str(e)}")
            print()
            error_count += 1
    
    output_file.close()
    
    print(f"{'='*50}")
    print(f"Upload complete!")
    print(f"✅ Successfully uploaded: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"{'='*50}")
    print(f"\nMapping file saved: cloudinary_image_mapping.txt")
    print(f"\nNext steps:")
    print(f"1. Check cloudinary_image_mapping.txt for the URL mappings")
    print(f"2. Update your Product records in Django admin with the Cloudinary URLs")
    print(f"3. Add Cloudinary environment variables to Render and deploy")

if __name__ == '__main__':
    print("Starting image upload to Cloudinary...")
    print(f"Cloud Name: {CLOUDINARY_CLOUD_NAME}")
    print(f"API Key: {CLOUDINARY_API_KEY}")
    print()
    
    confirm = input("Do you want to proceed? (yes/no): ")
    if confirm.lower() == 'yes':
        upload_images_from_folder()
    else:
        print("Upload cancelled.")
