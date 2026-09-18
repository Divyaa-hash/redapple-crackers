import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def upload_remaining_flower_pots():
    """
    Upload remaining 4 Flower Pot images
    """
    
    # Image to product mapping for remaining images
    image_mapping = {
        "Jumbo Super Deluxe ( 10 pcs).webp": "Jumbo Super Deluxe (10 Pcs)",
        "Mega Tri Colour Fountain ( 5 pcs).webp": "Mega Tri Colour Fountain (5 Pcs)",
        "Motu Patlu Tri Colour (5 Pcs).webp": "Motu Patlu Tri Colour (5 Pcs)",
        "Special Colour Koti (10 Pcs).webp": "Special Colour Koti (10 Pcs)"
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
    
    print("-" * 50)
    print(f"Uploaded: {uploaded_count} images")
    print(f"Already had images: {already_has_image}")
    print(f"Not found/failed: {not_found_count} images")
    print("\nDone!")

if __name__ == "__main__":
    upload_remaining_flower_pots()
