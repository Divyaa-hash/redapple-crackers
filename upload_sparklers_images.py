import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def upload_sparklers_images():
    """
    Upload images for SPARKLERS products
    """
    
    # Image to product mapping
    image_mapping = {
        "7 Cm Electric Sparklers.webp": "7 Cm Electric Sparklers",
        "7 Cm Colour Sparklers.webp": "7 Cm Colour Sparklers",
        "7 Cm Green Sparklers.webp": "7 Cm Green Sparklers",
        "7 Cm Red Sparklers.webp": "7 Cm Red Sparklers",
        "10 Cm Electric Sparklers.webp": "10 Cm Electric Sparklers",
        "10 Cm Colour Sparklers.webp": "10 Cm Colour Sparklers",
        "10 Cm Green Sparklers.webp": "10 Cm Green Sparklers",
        "10 Cm Red Sparklers.webp": "10 Cm Red Sparklers",
        "12 Cm Electric Sparklers.webp": "12 Cm Electric Sparklers",
        "12 Cm Colour Sparklers.webp": "12 Cm Colour Sparklers",
        "12 Cm Green Sparklers.webp": "12 Cm Green Sparklers",
        "12 Cm Red Sparklers.webp": "12 Cm Red Sparklers",
        "15 Cm Electric Sparklers.webp": "15 Cm Electric Sparklers",
        "15 Cm Colour Sparklers.webp": "15 Cm Colour Sparklers",
        "15 Cm Green Sparklers.webp": "15 Cm Green Sparklers",
        "15 Cm Red Sparklers.webp": "15 Cm Red Sparklers",
        "30 Cm Electric Sparklers.webp": "30 Cm Electric Sparklers",
        "30 Cm Colour Sparklers.webp": "30 Cm Colour Sparklers",
        "30 Cm Green Sparklers.webp": "30 Cm Green Sparklers",
        "30 Cm Red Sparklers.webp": "30 Cm Red Sparklers",
        "50 Cm Electric Sparklers.webp": "50 Cm Electric Sparklers",
        "50 Cm Colour Sparklers.webp": "50 Cm Colour Sparklers"
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
        product = Product.objects.filter(name=product_name).first()
        
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
    
    # Check for Rotating Sparklers (no image file available)
    rotating_product = Product.objects.filter(name="Rotating Sparklers").first()
    if rotating_product and not rotating_product.main_image:
        print(f"⚠ No image file available for: Rotating Sparklers")
    
    print("-" * 50)
    print(f"Uploaded: {uploaded_count} images")
    print(f"Already had images: {already_has_image}")
    print(f"Not found/failed: {not_found_count} images")
    print("\nDone!")

if __name__ == "__main__":
    upload_sparklers_images()
