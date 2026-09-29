from django import template
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
import os

register = template.Library()

def safe_static(path):
    """
    Safely get static URL with fallback to logo if file doesn't exist.
    This prevents ValueError with ManifestStaticFilesStorage.
    """
    try:
        # Try to get the static URL
        url = static(path)
        # Check if the file actually exists in staticfiles
        if staticfiles_storage.exists(path):
            return url
        # File doesn't exist, use logo fallback
        return static('images/crackers/logo.jpg')
    except (ValueError, Exception):
        # If static() fails (manifest error), use logo fallback
        return static('images/crackers/logo.jpg')

@register.simple_tag
def product_image_url(product):
    """
    Get the correct image URL for a product with proper static file handling.

    Usage: {% product_image_url product %}

    Logic:
    1. If product.main_image contains a full Cloudinary URL starting with https://res.cloudinary.com/, use it directly.
    2. If product.main_image is a local path such as images/crackers/Kids Pack.jpeg, render it using Django static.
    3. If main_image is empty, fallback to product.image_url using the same static-path logic.
    4. If static file doesn't exist, fallback to logo.jpg
    """
    # Try main_image first
    if product.main_image:
        image_path = str(product.main_image)

        # If it's a Cloudinary URL or external URL, use it directly
        if image_path.startswith('http'):
            return image_path

        # If it's a local static path, use Django's static tag with safety check
        if image_path.startswith('images/'):
            return safe_static(image_path)

        # If it's a media path, convert to static path
        if 'media/products/' in image_path:
            filename = image_path.replace('media/products/', '')
            return safe_static(f'images/crackers/{filename}')

        # If it's just products/filename.jpg
        if image_path.startswith('products/'):
            filename = image_path.replace('products/', '')
            return safe_static(f'images/crackers/{filename}')

        # If main_image has .url attribute (ImageField)
        if hasattr(product.main_image, 'url'):
            url = product.main_image.url
            if 'media/products/' in url:
                filename = url.replace('media/products/', '')
                return safe_static(f'images/crackers/{filename}')
            return url

        # Otherwise use the string value as-is
        return image_path

    # Fall back to image_url
    if product.image_url:
        image_path = str(product.image_url)

        # If it's a Cloudinary URL or external URL, use it directly
        if image_path.startswith('http'):
            return image_path

        # If it's a local static path, use Django's static tag with safety check
        if image_path.startswith('images/'):
            return safe_static(image_path)

        # Otherwise use as-is
        return image_path

    # Final fallback - use slug-based image with safety check
    return safe_static(f'images/crackers/{product.slug}.jpg')


@register.simple_tag
def product_image_url_debug(product):
    """
    Debug version that returns the actual values for inspection.
    """
    debug_info = {
        'main_image': str(product.main_image) if product.main_image else None,
        'image_url': str(product.image_url) if product.image_url else None,
        'slug': product.slug,
    }
    return f"DEBUG: {debug_info}"
