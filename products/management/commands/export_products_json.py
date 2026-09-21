from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
import json
from products.models import Product, Category

class Command(BaseCommand):
    help = 'Export products and categories to JSON for safe sync to production'

    def handle(self, *args, **options):
        self.stdout.write('Exporting products and categories to JSON...')
        
        # Export categories
        categories = Category.objects.all()
        categories_data = []
        for cat in categories:
            categories_data.append({
                'name': cat.name,
                'slug': cat.slug,
                'description': cat.description,
                'is_active': cat.is_active,
                'order': cat.order,
                'meta_title': cat.meta_title,
                'meta_description': cat.meta_description,
                'meta_keywords': cat.meta_keywords,
            })
        
        # Export products
        products = Product.objects.all()
        products_data = []
        for product in products:
            products_data.append({
                'name': product.name,
                'slug': product.slug,
                'sku': product.sku,
                'category_name': product.category.name if product.category else None,
                'category_slug': product.category.slug if product.category else None,
                'product_type': product.product_type,
                'safety_level': product.safety_level,
                'short_description': product.short_description,
                'description': product.description,
                'safety_instructions': product.safety_instructions,
                'regular_price': str(product.regular_price),
                'sale_price': str(product.sale_price) if product.sale_price else None,
                'wholesale_price': str(product.wholesale_price) if product.wholesale_price else None,
                'stock': product.stock,
                'low_stock_threshold': product.low_stock_threshold,
                'image_url': product.image_url,
                'additional_images': product.additional_images,
                'video_url': product.video_url,
                'weight': str(product.weight) if product.weight else None,
                'dimensions': product.dimensions,
                'pieces': product.pieces,
                'duration': product.duration,
                'sound_level': product.sound_level,
                'height': product.height,
                'is_featured': product.is_featured,
                'is_new': product.is_new,
                'is_bestseller': product.is_bestseller,
                'is_digital': product.is_digital,
                'is_trending': product.is_trending,
                'is_limited_edition': product.is_limited_edition,
                'has_free_shipping': product.has_free_shipping,
                'has_gift_wrap': product.has_gift_wrap,
                'reward_points': product.reward_points,
                'festival_name': product.festival.name if product.festival else None,
                'meta_title': product.meta_title,
                'meta_description': product.meta_description,
                'meta_keywords': product.meta_keywords,
                'is_active': product.is_active,
                'order': product.order,
            })
        
        # Save to JSON file
        export_data = {
            'categories': categories_data,
            'products': products_data,
        }
        
        with open('products_export.json', 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder)
        
        self.stdout.write(self.style.SUCCESS(f'Exported {len(categories_data)} categories and {len(products_data)} products to products_export.json'))
