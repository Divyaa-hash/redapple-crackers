import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def upload_pencil_images():
    """
    Upload images for PENCIL and (Sattai) TWINGLING STARS products
    """
    
    # Image to product mapping
    image_mapping = {
        "10 ' Pencil ( 10 Pcs).webp": "10' Pencil (10 Pcs)",
        "7 ' Pencil ( 10 Pcs).webp": "7' Pencil (10 Pcs)",
        "Popcorn Pencil (5 Pcs).webp": "Popcorn Pencil (5 Pcs)",
        "Rainbow flash Pencil (5 Pcs).webp": "Rainbow flash Pencil (5 Pcs)",
        "Sivakasi special Candle Pencil (2 Pcs).webp": "Sivakasi special Candle Pencil (2 Pcs)",
        "Ultra Torch pencil (3 Pcs).webp": "Ultra Torch pencil (3 Pcs)",
        "1 ' (Sattai) Twingling Star (10 Pcs).webp": "1 1/2' (Sattai) Twingling Star (10 Pcs)",
        "4' (Sattai) Twingling Star (10 Pcs).webp": "4' (Sattai) Twingling Star (10 Pcs)"
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
    upload_pencil_images()
