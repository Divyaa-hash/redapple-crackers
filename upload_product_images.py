import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def upload_product_images():
    """
    Upload product images from a folder to products.
    
    Instructions:
    1. Create a folder named 'product_images' in the project root
    2. Place your images in that folder
    3. Name images to match product names (e.g., '4 Lakshmi.jpg' for '4' Lakshmi')
    4. Run this script: python upload_product_images.py
    """
    
    # Path to images folder
    images_folder = os.path.join(os.path.dirname(__file__), 'product_images')
    
    # Create folder if it doesn't exist
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
        print(f"Created folder: {images_folder}")
        print("Please place your product images in this folder and run the script again.")
        return
    
    # Get all image files
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
    
    if not image_files:
        print(f"No images found in {images_folder}")
        print("Please place your product images in this folder and run the script again.")
        return
    
    print(f"Found {len(image_files)} image files")
    print("-" * 50)
    
    uploaded_count = 0
    not_found_count = 0
    
    for image_file in image_files:
        # Remove file extension to get product name
        image_name = os.path.splitext(image_file)[0]
        
        # Try to find matching product
        # Try exact match first
        product = Product.objects.filter(name__icontains=image_name).first()
        
        if not product:
            # Try fuzzy match (remove special characters)
            clean_name = image_name.replace('_', ' ').replace('-', ' ')
            product = Product.objects.filter(name__icontains=clean_name).first()
        
        if product:
            # Copy image to media folder
            image_path = os.path.join(images_folder, image_file)
            
            # Create media folder if it doesn't exist
            media_folder = os.path.join('media', 'products')
            if not os.path.exists(media_folder):
                os.makedirs(media_folder)
            
            # Generate unique filename
            file_ext = os.path.splitext(image_file)[1]
            new_filename = f"{product.slug}{file_ext}"
            destination_path = os.path.join(media_folder, new_filename)
            
            # Copy file
            shutil.copy2(image_path, destination_path)
            
            # Update product
            if not product.main_image:
                product.main_image = f"products/{new_filename}"
                product.save()
                print(f"✓ Uploaded main image for: {product.name}")
                uploaded_count += 1
            else:
                print(f"- Product already has main image: {product.name}")
        else:
            print(f"✗ Product not found for image: {image_file}")
            not_found_count += 1
    
    print("-" * 50)
    print(f"Uploaded: {uploaded_count} images")
    print(f"Not found: {not_found_count} images")
    print("\nDone!")

if __name__ == "__main__":
    upload_product_images()
