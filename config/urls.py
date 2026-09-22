"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from products.models import Product, Category
from products.views import shop_view, festival_offers_view, offers_view
from users.views import login_view, signup_view, logout_view
import os
import json
import openpyxl

def home_view(request):
    active = Product.objects.filter(is_active=True)
    trending_products = list(active.filter(is_trending=True)[:8])
    featured_products = list(active.filter(is_featured=True)[:4])
    new_products = list(active.filter(is_new=True)[:4])
    if not trending_products:
        trending_products = list(active[:8])
    if not featured_products:
        featured_products = list(active[:4])
    if not new_products:
        new_products = list(active[4:8])
    # If still no products, use all active products
    if not trending_products:
        trending_products = list(active[:8])
    if not featured_products:
        featured_products = list(active[:4])
    if not new_products:
        new_products = list(active[4:8])
    return render(request, 'home.html', {
        'trending_products': trending_products,
        'featured_products': featured_products,
        'new_products': new_products
    })

@csrf_exempt
def update_prices_view(request):
    """Update product names and prices from Excel file with 10% markup"""
    try:
        excel_file = 'Vamsi_Crackers 2026 diwali.xlsx'
        
        if not os.path.exists(excel_file):
            return JsonResponse({'success': False, 'message': f'Excel file not found: {excel_file}'})
        
        # Read Excel file using openpyxl
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active
        
        updated_count = 0
        created_count = 0
        
        # Skip header row, start from row 2
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row or len(row) < 3:
                continue
                
            product_name = str(row[0]).strip() if row[0] else ''
            category_name = str(row[1]).strip() if row[1] else ''
            original_price = float(row[2]) if row[2] else 0
            
            if not product_name or not category_name or original_price == 0:
                continue
            
            # Apply 10% markup
            new_price = original_price * 1.1
            
            # Try to find existing product by name (case-insensitive)
            product = Product.objects.filter(name__icontains=product_name).first()
            
            if product:
                # Update existing product
                product.name = product_name
                product.regular_price = new_price
                product.save()
                updated_count += 1
            else:
                # Try to find or create category
                category = Category.objects.filter(name__icontains=category_name).first()
                if not category:
                    category = Category.objects.create(
                        name=category_name,
                        slug=category_name.lower().replace(' ', '-'),
                        is_active=True
                    )
                
                # Create new product
                slug = product_name.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace('"', '')
                sku = slug[:50]
                
                product = Product.objects.create(
                    name=product_name,
                    slug=slug,
                    sku=sku,
                    category=category,
                    regular_price=new_price,
                    short_description=f'{product_name} - Premium quality crackers',
                    description=f'{product_name} from {category_name}. Premium quality fireworks for your celebrations.',
                    stock=100,
                    is_active=True,
                    is_new=True
                )
                created_count += 1
        
        return JsonResponse({
            'success': True,
            'message': 'Price update completed successfully',
            'updated': updated_count,
            'created': created_count,
            'total': updated_count + created_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
def reload_vasantham_view(request):
    """Reload Vasantham products from JSON export - public for Render deployment"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        from django.db import connection
        
        # Count before deletion
        products_before = Product.objects.count()
        categories_before = Category.objects.count()
        
        # Use raw SQL to delete all related data bypassing Django ORM constraints
        with connection.cursor() as cursor:
            # Delete cart items first (they reference products)
            cursor.execute("DELETE FROM cart_cartitem")
            # Delete wishlist items
            cursor.execute("DELETE FROM wishlist_wishlistitem")
            # Delete products
            cursor.execute("DELETE FROM products_product")
            # Delete categories
            cursor.execute("DELETE FROM products_category")
        
        # Load Vasantham products from export file
        with open('products_export.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create categories
        categories_data = data.get('categories', [])
        for cat_data in categories_data:
            Category.objects.create(
                name=cat_data['name'],
                slug=cat_data['slug'],
                description=cat_data.get('description', ''),
                is_active=True,
                order=cat_data.get('order', 0)
            )
        
        # Create products
        products_data = data.get('products', [])
        for prod_data in products_data:
            category = Category.objects.get(slug=prod_data['category'])
            Product.objects.create(
                name=prod_data['name'],
                slug=prod_data['slug'],
                sku=prod_data.get('sku', ''),
                category=category,
                regular_price=prod_data['regular_price'],
                sale_price=prod_data.get('sale_price'),
                stock=prod_data.get('stock', 0),
                low_stock_threshold=prod_data.get('low_stock_threshold', 5),
                short_description=prod_data.get('short_description', ''),
                description=prod_data.get('description', ''),
                safety_instructions=prod_data.get('safety_instructions', ''),
                is_active=prod_data.get('is_active', True),
                order=prod_data.get('order', 0)
            )
        
        return JsonResponse({
            'success': True,
            'message': 'Vasantham products loaded successfully',
            'products_before': products_before,
            'categories_before': categories_before,
            'products_after': Product.objects.count(),
            'categories_after': Category.objects.count()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('home/', home_view, name='home_redirect'),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('orders/', include('orders.urls')),
    path('checkout/', include('orders.urls')),
    path('shop/', shop_view, name='shop'),
    path('categories/', TemplateView.as_view(template_name='categories.html')),
    path('wholesale/', TemplateView.as_view(template_name='wholesale.html')),
    path('offers/', offers_view, name='offers'),
    path('festival-offers/', festival_offers_view, name='festival_offers'),
    path('about/', TemplateView.as_view(template_name='about.html')),
    path('contact/', TemplateView.as_view(template_name='contact.html')),
    path('safety/', TemplateView.as_view(template_name='safety_guidelines.html')),
    path('order-confirmation/', TemplateView.as_view(template_name='order_confirmation.html'), name='order_confirmation'),
    path('order-tracking/', TemplateView.as_view(template_name='order_tracking.html'), name='order_tracking'),
    path('update-prices/', update_prices_view, name='update_prices'),
    path('reload-vasantham/', reload_vasantham_view, name='reload_vasantham'),
    path('siteadmin/', include('siteadmin.urls')),
    # Auth URLs
    path('login/', login_view, name='login'),
    path('register/', signup_view, name='register'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]

# Serve media files in both development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
