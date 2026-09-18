import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def upload_8_images():
    """
    Upload 8 specific product images for One Sound Crackers category
    """
    
    # Image to product mapping
    image_mapping = {
        "4' lakshmi.webp": "4' Lakshmi",
        "3 Lakshmi.webp": "3 1/2 Lakshmi",
        "4 ' Lakshmi Deluxe.webp": "4' Lakshmi Deluxe",
        "Golden Lakshmi Deluxe.webp": "Golden Lakshmi Deluxe",
        "5' Kumki Deluxe": "5' Kumki Deluxe",
        "Deluxe Jallikattu": "Deluxe Jallikattu",
        "Two Sound Colour": "Two Sound Colour",
        "2  ' Kuruvi": "2 3/4' Kuruvi"
    }
    
    project_root = os.path.dirname(__file__)
    media_folder = os.path.join(project_root, 'media', 'products')
    
    # Create media folder if it doesn't exist
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)
        print(f"Created folder: {media_folder}")
    
    uploaded_count = 0
    not_found_count = 0
    
    for image_file, product_name in image_mapping.items():
        image_path = os.path.join(project_root, image_file)
        
        # Check if image file exists
        if not os.path.exists(image_path):
            print(f"✗ Image file not found: {image_file}")
            not_found_count += 1
            continue
        
        # Find product
        product = Product.objects.filter(name=product_name).first()
        
        if not product:
            print(f"✗ Product not found: {product_name}")
            not_found_count += 1
            continue
        
        # Get file extension
        file_ext = os.path.splitext(image_file)[1]
        if not file_ext:
            file_ext = '.webp'  # Default to webp
        
        # Generate unique filename using product slug
        new_filename = f"{product.slug}{file_ext}"
        destination_path = os.path.join(media_folder, new_filename)
        
        # Copy file
        try:
            shutil.copy2(image_path, destination_path)
            
            # Update product
            product.main_image = f"products/{new_filename}"
            product.save()
            
            print(f"✓ Uploaded: {image_file} -> {product.name}")
            uploaded_count += 1
        except Exception as e:
            print(f"✗ Error uploading {image_file}: {e}")
            not_found_count += 1
    
    print("-" * 50)
    print(f"Uploaded: {uploaded_count} images")
    print(f"Not found/failed: {not_found_count} images")
    print("\nDone!")

if __name__ == "__main__":
    upload_8_images()
