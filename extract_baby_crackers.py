import re
import requests
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def extract_product_data_from_html():
    """Extract product names and image URLs from the provided HTML"""
    
    # HTML content - paste the full HTML here
    html_content = """
    PASTE HTML HERE
    """
    
    products = []
    
    # Pattern to extract product data from HTML
    # Looking for: <img class="itmImage" alt="product name" src="image url">
    # and: <td class="itemDesc">product name</td>
    
    # Find all img tags with class itmImage
    img_pattern = r'<img[^>]*class="itmImage"[^>]*alt="([^"]*)"[^>]*src="([^"]*)"[^>]*>'
    img_matches = re.findall(img_pattern, html_content)
    
    # Find all itemDesc td tags
    desc_pattern = r'<td[^>]*class="itemDesc"[^>]*>([^<]*)</td>'
    desc_matches = re.findall(desc_pattern, html_content)
    
    # Combine the data
    for i, (alt_text, image_url) in enumerate(img_matches):
        if i < len(desc_matches):
            product_name = desc_matches[i].strip()
            if image_url and product_name:
                products.append({
                    'name': product_name,
                    'image_url': image_url
                })
    
    return products

def download_image(url, save_path):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {save_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def update_products_with_images():
    """Update existing products with new images"""
    
    print("Extracting product data...")
    products = extract_product_data_from_html()
    print(f"Found {len(products)} products")
    
    # Download images
    media_path = 'media/products'
    downloaded_images = []
    
    for product in products:
        # Generate filename from product name
        safe_name = re.sub(r'[^\w\s-]', '', product['name'])
        safe_name = re.sub(r'[-\s]+', '-', safe_name)
        filename = f"{safe_name}.jpg"
        save_path = os.path.join(media_path, filename)
        
        # Download image
        if download_image(product['image_url'], save_path):
            downloaded_images.append({
                'name': product['name'],
                'image_path': f'products/{filename}'
            })
    
    print(f"\nSuccessfully downloaded {len(downloaded_images)} images")
    
    # Update database
    updated_count = 0
    for downloaded in downloaded_images:
        try:
            # Try to find product by name (fuzzy match)
            product = Product.objects.filter(name__icontains=downloaded['name']).first()
            if product:
                product.main_image = downloaded['image_path']
                product.save()
                updated_count += 1
                print(f"Updated: {product.name}")
            else:
                print(f"Not found in database: {downloaded['name']}")
        except Exception as e:
            print(f"Error updating {downloaded['name']}: {e}")
    
    print(f"\nUpdated {updated_count} products in database")

if __name__ == '__main__':
    update_products_with_images()
