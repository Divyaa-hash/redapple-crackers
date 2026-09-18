import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def upload_single_sound_images():
    """
    Upload images for SINGLE SOUND CRACKERS products that don't have images
    """
    
    # Products without images in SINGLE SOUND CRACKERS category
    products_to_upload = [
        "4\" Lakshmi Mega Deluxe",
        "4\" Lakshmi"
    ]
    
    # Image mapping (you need to provide the actual image file names)
    # For now, I'll use the existing images we have
    image_mapping = {
        "4\" Lakshmi Mega Deluxe": "4 ' Lakshmi Deluxe.webp",  # Using similar image
        "4\" Lakshmi": "4' lakshmi.webp"  # Using similar image
    }
    
    project_root = os.path.dirname(__file__)
    media_folder = os.path.join(project_root, 'media', 'products')
    
    # Create media folder if it doesn't exist
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)
        print(f"Created folder: {media_folder}")
    
    uploaded_count = 0
    not_found_count = 0
    
    for product_name, image_file in image_mapping.items():
        image_path = os.path.join(project_root, image_file)
        
        # Check if image file exists
        if not os.path.exists(image_path):
            print(f"✗ Image file not found: {image_file}")
            not_found_count += 1
            continue
        
        # Find product (there might be multiple with same name)
        products = Product.objects.filter(name=product_name, category__name='SINGLE SOUND CRACKERS')
        
        if not products.exists():
            print(f"✗ Product not found: {product_name}")
            not_found_count += 1
            continue
        
        for product in products:
            # Skip if already has image
            if product.main_image:
                print(f"- Product already has image: {product.name}")
                continue
            
            # Get file extension
            file_ext = os.path.splitext(image_file)[1]
            
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
    upload_single_sound_images()
