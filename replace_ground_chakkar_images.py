import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def replace_ground_chakkar_images():
    """
    1. Remove existing images for GROUND CHAKKAR products
    2. Upload new images for GROUND CHAKKAR products
    """
    
    project_root = os.path.dirname(__file__)
    media_folder = os.path.join(project_root, 'media', 'products')
    
    # Create media folder if it doesn't exist
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)
        print(f"Created folder: {media_folder}")
    
    # Step 1: Remove existing images for GROUND CHAKKAR products
    print("=" * 50)
    print("STEP 1: Removing existing images for GROUND CHAKKAR products")
    print("=" * 50)
    
    ground_chakkar_products = [
        "Ground Chakkar Ashoka (10 Pcs)",
        "Ground Chakkar Big (10 Pcs)",
        "Ground Chakkar Big (25 Pcs)",
        "Ground Chakkar Small (10 Pcs)",
        "Ground Chakkar Asoka (10 Pcs)",
        "Ground Chakkar Special (10 Pcs)",
        "Ground Chakkar Deluxe (10 Pcs)"
    ]
    
    removed_count = 0
    for product_name in ground_chakkar_products:
        product = Product.objects.filter(name=product_name).first()
        if product and product.main_image:
            product.main_image = None
            product.save()
            print(f"✓ Removed image for: {product_name}")
            removed_count += 1
        else:
            print(f"- No image to remove for: {product_name}")
    
    print(f"Removed {removed_count} images")
    
    # Step 2: Upload new images for GROUND CHAKKAR products
    print("\n" + "=" * 50)
    print("STEP 2: Uploading new images for GROUND CHAKKAR products")
    print("=" * 50)
    
    # Image to product mapping
    image_mapping = {
        "Ground Chakkar Ashoka (10 Pcs).webp": "Ground Chakkar Ashoka (10 Pcs)",
        "Ground Chakkar Big ( 25 Pcs).webp": "Ground Chakkar Big (25 Pcs)",
        "Ground Chakkar Small(10 Pcs).webp": "Ground Chakkar Small (10 Pcs)",
        "Ground Chakkar Special (10 Pcs).webp": "Ground Chakkar Special (10 Pcs)",
        "Chakkar Spinner Deluxe (10Pcs).webp": "Ground Chakkar Deluxe (10 Pcs)",
        "Disco Wheel ( 5 Pcs).webp": "Ground Chakkar Big (10 Pcs)",
        "Whizzling Wheel ( 5 Pcs).webp": "Ground Chakkar Asoka (10 Pcs)"
    }
    
    uploaded_count = 0
    not_found_count = 0
    
    for image_file, product_name in image_mapping.items():
        image_path = os.path.join(project_root, image_file)
        
        if not os.path.exists(image_path):
            print(f"✗ Image file not found: {image_file}")
            not_found_count += 1
            continue
        
        product = Product.objects.filter(name=product_name).first()
        if not product:
            print(f"✗ Product not found: {product_name}")
            not_found_count += 1
            continue
        
        file_ext = os.path.splitext(image_file)[1]
        new_filename = f"{product.slug}{file_ext}"
        destination_path = os.path.join(media_folder, new_filename)
        
        try:
            shutil.copy2(image_path, destination_path)
            product.main_image = f"products/{new_filename}"
            product.save()
            print(f"✓ Uploaded: {image_file} -> {product_name}")
            uploaded_count += 1
        except Exception as e:
            print(f"✗ Error uploading {image_file}: {e}")
            not_found_count += 1
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Removed: {removed_count} old images")
    print(f"Uploaded: {uploaded_count} new images")
    print(f"Not found/failed: {not_found_count} images")
    print("\nDone!")

if __name__ == "__main__":
    replace_ground_chakkar_images()
