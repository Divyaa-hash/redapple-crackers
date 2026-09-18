import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def upload_bijili_bomb_images():
    """
    Upload images for BIJILI/ BOMB ITEMS products
    """
    
    # Image to product mapping
    image_mapping = {
        "555 Bomb ( 10 Pcs).webp": "555 Bomb (10 Pcs)",
        "Atom Bomb (10 Pcs).webp": "Atom Bomb (10 Pcs)",
        "Bullet Bomb (10 Pcs).webp": "Bullet Bomb (10 Pcs)",
        "Digital Deluxe Bomb ( 10 Pcs).webp": "Digital Deluxe Bomb (10 Pcs)",
        "Dinoser Bomb (10 Pcs).webp": "Dinoser Bomb (10 Pcs)",
        "Hydro Bomb ( 10 Pcs).webp": "Hydro Bomb (10 Pcs)",
        "King of King Bomb (10 Pcs).webp": "King of King Bomb (10 Pcs)",
        "Red Bijili ( 100 pcs).webp": "Red Bijili (100 pcs)",
        "Red Bijili ( 50 pcs).webp": "Red Bijili (50 pcs)"
    }
    
    project_root = os.path.dirname(__file__)
    media_folder = os.path.join(project_root, 'media', 'products')
    
    # Create media folder if it doesn't exist
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)
        print(f"Created folder: {media_folder}")
    
    uploaded_count = 0
    not_found_count = 0
    already_has_image = 0
    
    for image_file, product_name in image_mapping.items():
        image_path = os.path.join(project_root, image_file)
        
        # Check if image file exists
        if not os.path.exists(image_path):
            print(f"✗ Image file not found: {image_file}")
            not_found_count += 1
            continue
        
        # Find product
        product = Product.objects.filter(name__icontains=product_name).first()
        
        if not product:
            print(f"✗ Product not found: {product_name}")
            not_found_count += 1
            continue
        
        # Skip if already has image
        if product.main_image:
            print(f"- Product already has image: {product.name}")
            already_has_image += 1
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
    
    # Check for Stripped (vari) Bijili (100 Pcs) - no image file found
    stripped_product = Product.objects.filter(name__icontains="Stripped").first()
    if stripped_product and not stripped_product.main_image:
        print(f"⚠ No image file available for: Stripped (vari) Bijili (100 Pcs)")
    
    print("-" * 50)
    print(f"Uploaded: {uploaded_count} images")
    print(f"Already had images: {already_has_image}")
    print(f"Not found/failed: {not_found_count} images")
    print("\nDone!")

if __name__ == "__main__":
    upload_bijili_bomb_images()
