from django import template
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def product_image_url(product):
    """
    Get the correct image URL for a product with proper static file handling.
    
    Usage: {% product_image_url product %}
    
    Logic:
    1. If product.main_image contains a full Cloudinary URL starting with https://res.cloudinary.com/, use it directly.
    2. If product.main_image is a local path such as images/crackers/Kids Pack.jpeg, render it using Django static.
    3. If main_image is empty, fallback to product.image_url using the same static-path logic.
    """
    # Try main_image first
    if product.main_image:
        image_path = str(product.main_image)
        
        # If it's a Cloudinary URL or external URL, use it directly
        if image_path.startswith('http'):
            return image_path
        
        # If it's a local static path, use Django's static tag
        if image_path.startswith('images/'):
            return static(image_path)
        
        # If it's a media path, convert to static path
        if 'media/products/' in image_path:
            filename = image_path.replace('media/products/', '')
            return static(f'images/crackers/{filename}')
        
        # If it's just products/filename.jpg
        if image_path.startswith('products/'):
            filename = image_path.replace('products/', '')
            return static(f'images/crackers/{filename}')
        
        # If main_image has .url attribute (ImageField)
        if hasattr(product.main_image, 'url'):
            url = product.main_image.url
            if 'media/products/' in url:
                filename = url.replace('media/products/', '')
                return static(f'images/crackers/{filename}')
            return url
        
        # Otherwise use the string value as-is
        return image_path
    
    # Fall back to image_url
    if product.image_url:
        image_path = str(product.image_url)
        
        # If it's a Cloudinary URL or external URL, use it directly
        if image_path.startswith('http'):
            return image_path
        
        # If it's a local static path, use Django's static tag
        if image_path.startswith('images/'):
            return static(image_path)
        
        # Otherwise use as-is
        return image_path
    
    # Final fallback - use slug-based image
    return static(f'images/crackers/{product.slug}.jpg')
