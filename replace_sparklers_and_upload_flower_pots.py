import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def replace_and_upload_images():
    """
    1. Remove existing images for 7 Cm and 10 Cm Sparklers
    2. Upload new images for 7 Cm and 10 Cm Sparklers
    3. Upload images for FLOWER POTS products
    """
    
    project_root = os.path.dirname(__file__)
    media_folder = os.path.join(project_root, 'media', 'products')
    
    # Create media folder if it doesn't exist
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)
        print(f"Created folder: {media_folder}")
    
    # Step 1: Remove existing images for 7 Cm and 10 Cm Sparklers
    print("=" * 50)
    print("STEP 1: Removing existing images for 7 Cm and 10 Cm Sparklers")
    print("=" * 50)
    
    sparklers_to_remove = [
        "7 Cm Electric Sparklers",
        "7 Cm Colour Sparklers",
        "7 Cm Green Sparklers",
        "7 Cm Red Sparklers",
        "10 Cm Electric Sparklers",
        "10 Cm Colour Sparklers",
        "10 Cm Green Sparklers",
        "10 Cm Red Sparklers"
    ]
    
    removed_count = 0
    for product_name in sparklers_to_remove:
        product = Product.objects.filter(name=product_name).first()
        if product and product.main_image:
            product.main_image = None
            product.save()
            print(f"✓ Removed image for: {product_name}")
            removed_count += 1
    
    print(f"Removed {removed_count} images")
    
    # Step 2: Upload new images for 7 Cm and 10 Cm Sparklers
    print("\n" + "=" * 50)
    print("STEP 2: Uploading new images for 7 Cm and 10 Cm Sparklers")
    print("=" * 50)
    
    sparkler_new_images = {
        "7 Cm Electric Sparklers.webp": "7 Cm Electric Sparklers",
        "7 Cm Colour Sparklers.webp": "7 Cm Colour Sparklers",
        "7 Cm Green Sparklers.webp": "7 Cm Green Sparklers",
        "7 Cm Red Sparklers.webp": "7 Cm Red Sparklers",
        "10 Cm Electric Sparklers.webp": "10 Cm Electric Sparklers",
        "10 Cm Colour Sparklers.webp": "10 Cm Colour Sparklers",
        "10 Cm Green Sparklers.webp": "10 Cm Green Sparklers",
        "10 Cm Red Sparklers.webp": "10 Cm Red Sparklers"
    }
    
    uploaded_sparklers = 0
    for image_file, product_name in sparkler_new_images.items():
        image_path = os.path.join(project_root, image_file)
        
        if not os.path.exists(image_path):
            print(f"✗ Image file not found: {image_file}")
            continue
        
        product = Product.objects.filter(name=product_name).first()
        if not product:
            print(f"✗ Product not found: {product_name}")
            continue
        
        file_ext = os.path.splitext(image_file)[1]
        new_filename = f"{product.slug}{file_ext}"
        destination_path = os.path.join(media_folder, new_filename)
        
        try:
            shutil.copy2(image_path, destination_path)
            product.main_image = f"products/{new_filename}"
            product.save()
            print(f"✓ Uploaded: {image_file} -> {product_name}")
            uploaded_sparklers += 1
        except Exception as e:
            print(f"✗ Error uploading {image_file}: {e}")
    
    print(f"Uploaded {uploaded_sparklers} Sparkler images")
    
    # Step 3: Upload images for FLOWER POTS
    print("\n" + "=" * 50)
    print("STEP 3: Uploading images for FLOWER POTS")
    print("=" * 50)
    
    flower_pot_images = {
        "Flower Pots Ashoka (10 Pcs).webp": "Flower Pots Ashoka (10 Pcs)",
        "Flower Pots Big (10 Pcs).webp": "Flower Pots Big (10 Pcs)",
        "Flower Pots Colour Koti (10 Pcs).webp": "Flower Pots Colour Koti (10 Pcs)",
        "Flower Pots Small ( 10 Pcs).webp": "Flower Pots Small (10 Pcs)",
        "Flower Pots Special (10 Pcs).webp": "Flower Pots Special (10 Pcs)",
        "Flower pots Colour Koti Deluxe(10 Pcs).webp": "Flower pots Colour Koti Deluxe (10 Pcs)",
        "Flower pots Multi Colour Giant (10 Pcs).webp": "Flower pots Multi Colour Giant (10 Pcs)",
        "Gypsy Colour Flower pots (5Pcs).webp": "Gypsy Colour Flower pots (5Pcs)"
    }
    
    uploaded_flower_pots = 0
    for image_file, product_name in flower_pot_images.items():
        image_path = os.path.join(project_root, image_file)
        
        if not os.path.exists(image_path):
            print(f"✗ Image file not found: {image_file}")
            continue
        
        product = Product.objects.filter(name=product_name).first()
        if not product:
            print(f"✗ Product not found: {product_name}")
            continue
        
        # Skip if already has image
        if product.main_image:
            print(f"- Product already has image: {product_name}")
            continue
        
        file_ext = os.path.splitext(image_file)[1]
        new_filename = f"{product.slug}{file_ext}"
        destination_path = os.path.join(media_folder, new_filename)
        
        try:
            shutil.copy2(image_path, destination_path)
            product.main_image = f"products/{new_filename}"
            product.save()
            print(f"✓ Uploaded: {image_file} -> {product_name}")
            uploaded_flower_pots += 1
        except Exception as e:
            print(f"✗ Error uploading {image_file}: {e}")
    
    print(f"Uploaded {uploaded_flower_pots} Flower Pot images")
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Removed: {removed_count} old Sparkler images")
    print(f"Uploaded: {uploaded_sparklers} new Sparkler images")
    print(f"Uploaded: {uploaded_flower_pots} Flower Pot images")
    print("\nDone!")

if __name__ == "__main__":
    replace_and_upload_images()
