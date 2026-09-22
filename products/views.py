from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from products.models import Product, Category
import json
from decimal import Decimal
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Brand, Product, ProductReview, Festival, Coupon
from .serializers import (
    CategorySerializer, BrandSerializer, ProductSerializer, ProductListSerializer,
    ProductReviewSerializer, FestivalSerializer, CouponSerializer
)


def catalog_view(request):
    """Catalog view showing all products in Baby Crackers format"""
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    catalog_data = []
    for category in categories:
        products = Product.objects.filter(
            category=category,
            is_active=True
        ).order_by('order', 'name')
        
        if products.exists():
            # Use actual sale_price from database, or calculate 90% discount if no sale_price
            products_with_discount = []
            for product in products:
                original_price = product.regular_price
                discounted_price = product.sale_price if product.sale_price else original_price * Decimal('0.1')
                products_with_discount.append({
                    'product': product,
                    'original_price': original_price,
                    'discounted_price': discounted_price
                })
            
            catalog_data.append({
                'category': category,
                'products': products_with_discount
            })
    
    return render(request, 'catalog.html', {'catalog_data': catalog_data})


def product_detail_view(request, product_id):
    """Product detail page view"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Get all related products from the same category (excluding current product)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).order_by('order', 'name')
    
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })


def festival_offers_view(request):
    """Festival offers page displaying gift boxes"""
    try:
        # Show the 4 specific gift boxes
        gift_box_skus = ['GB-LF-20', 'GB-TB-30', 'GB-FS-40', 'GB-SF-50']
        gift_boxes = Product.objects.filter(sku__in=gift_box_skus, is_active=True)
        
        # Add savings calculation to each product
        for gift_box in gift_boxes:
            if gift_box.regular_price and gift_box.sale_price:
                gift_box.savings = gift_box.regular_price - gift_box.sale_price
            else:
                gift_box.savings = 0
        return render(request, 'festival_offers.html', {'gift_boxes': gift_boxes})
    except Exception as e:
        print(f"Error in festival_offers_view: {e}")
        return render(request, 'festival_offers.html', {'gift_boxes': []})


def offers_view(request):
    """Offers page displaying gift boxes and promotional offers"""
    try:
        # Show the 4 specific gift boxes
        gift_box_skus = ['GB-LF-20', 'GB-TB-30', 'GB-FS-40', 'GB-SF-50']
        gift_boxes = Product.objects.filter(sku__in=gift_box_skus, is_active=True)
        
        # Add savings calculation to each product
        for gift_box in gift_boxes:
            if gift_box.regular_price and gift_box.sale_price:
                gift_box.savings = gift_box.regular_price - gift_box.sale_price
            else:
                gift_box.savings = 0
        return render(request, 'offers.html', {'gift_boxes': gift_boxes})
    except Exception as e:
        print(f"Error in offers_view: {e}")
        return render(request, 'offers.html', {'gift_boxes': []})


def shop_view(request):
    """Shop page view with Vasantham Crackers World format"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Define category order to match exact database names
        category_order = [
            'One sound crackers',
            'PENCIL and (Sattai) TWINGLING STARS',
            'SPARKLERS',
            'FLOWER POTS',
            'GROUND CHAKKARS',
            'SKY ROCKETS',
            'BIJILI/ BOMB ITEMS',
            'PAPER BOMB',
            'Wala',
            'SKY NIGHT FANCY CELEBRATIONS',
            'REPEATING MULTI COLOUR FANCY SHOTS',
            'NIGHT FOUNTAIN CELEBRATIONS',
            'NIGHT FANCY CELEBRATION',
            'LADDU FOUNTAIN',
            'SNAKE and CARTOON',
            'CHILDRENS ROLL CAP/GUN',
            'COLOUR MATCHES',
            'NEW ARRIVALS',
            'GIFT BOXES',
            'COMBO PACKS',
            'SPECIAL SERIES FANCY SKY SHOTS'
        ]
        
        # Get categories in specific order
        ordered_categories = []
        for cat_name in category_order:
            try:
                category = Category.objects.get(name__iexact=cat_name, is_active=True)
                ordered_categories.append(category)
            except Category.DoesNotExist:
                continue
        
        # Get search query
        search_query = request.GET.get('q', '')
        
        # Get all active products
        products = Product.objects.filter(is_active=True)
        
        # Filter by search query if provided
        if search_query:
            products = products.filter(
                name__icontains=search_query
            )
        
        # Organize by category in Vasantham order
        catalog_data = []
        for category in ordered_categories:
            category_products = products.filter(category=category)
            
            if category_products.exists():
                # Use actual sale_price from database, or calculate 90% discount if no sale_price
                products_with_discount = []
                for product in category_products:
                    original_price = product.regular_price
                    discounted_price = product.sale_price if product.sale_price else original_price * Decimal('0.1')
                    products_with_discount.append({
                        'product': product,
                        'original_price': original_price,
                        'discounted_price': discounted_price
                    })
                
                catalog_data.append({
                    'category': category,
                    'products': products_with_discount
                })
        
        logger.info(f"Shop view returning {len(catalog_data)} categories with products")
        
        return render(request, 'shop.html', {
            'catalog_data': catalog_data,
            'categories': ordered_categories,
            'total_count': products.count(),
            'search_query': search_query
        })
    except Exception as e:
        logger.error(f"Error in shop_view: {e}")
        print(f"Error in shop_view: {e}")
        import traceback
        traceback.print_exc()
        return render(request, 'shop.html', {
            'catalog_data': [],
            'categories': [],
            'total_count': 0,
            'error': str(e)
        })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'sku', 'short_description', 'description']
    ordering_fields = ['name', 'regular_price', 'sale_price', 'created_at', 'stock']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        brand = self.request.query_params.get('brand')
        product_type = self.request.query_params.get('product_type')
        safety_level = self.request.query_params.get('safety_level')
        is_featured = self.request.query_params.get('is_featured')
        is_new = self.request.query_params.get('is_new')
        is_bestseller = self.request.query_params.get('is_bestseller')
        
        if category:
            queryset = queryset.filter(category__slug=category)
        if brand:
            queryset = queryset.filter(brand__slug=brand)
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        if safety_level:
            queryset = queryset.filter(safety_level=safety_level)
        if is_featured:
            queryset = queryset.filter(is_featured=True)
        if is_new:
            queryset = queryset.filter(is_new=True)
        if is_bestseller:
            queryset = queryset.filter(is_bestseller=True)
            
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def new_arrivals(self, request):
        new = self.queryset.filter(is_new=True)
        serializer = self.get_serializer(new, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        bestsellers = self.queryset.filter(is_bestseller=True)
        serializer = self.get_serializer(bestsellers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_slug = request.query_params.get('category')
        if category_slug:
            products = self.queryset.filter(category__slug=category_slug)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def by_brand(self, request):
        brand_slug = request.query_params.get('brand')
        if brand_slug:
            products = self.queryset.filter(brand__slug=brand_slug)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({'error': 'Brand parameter required'}, status=400)


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'comment']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ProductReview.objects.all()
        return ProductReview.objects.filter(is_approved=True)


class FestivalViewSet(viewsets.ModelViewSet):
    queryset = Festival.objects.filter(is_active=True)
    serializer_class = FestivalSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.filter(is_active=True)
    serializer_class = CouponSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'description']
    
    @action(detail=False, methods=['post'])
    def validate(self, request):
        code = request.data.get('code')
        order_value = request.data.get('order_value', 0)
        
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            if coupon.is_valid():
                if order_value >= coupon.minimum_order_value:
                    return Response({
                        'valid': True,
                        'discount_type': coupon.discount_type,
                        'discount_value': coupon.discount_value,
                        'maximum_discount': coupon.maximum_discount
                    })
                return Response({
                    'valid': False,
                    'message': f'Minimum order value of ₹{coupon.minimum_order_value} required'
                }, status=400)
            return Response({'valid': False, 'message': 'Coupon is expired or usage limit reached'}, status=400)
        except Coupon.DoesNotExist:
            return Response({'valid': False, 'message': 'Invalid coupon code'}, status=404)


@staff_member_required
@csrf_exempt
def reload_vasantham_products(request):
    """Admin-only URL to reload Vasantham products"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        # Count before deletion
        products_before = Product.objects.count()
        categories_before = Category.objects.count()
        
        # Delete all products
        Product.objects.all().delete()
        
        # Delete all categories
        Category.objects.all().delete()
        
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
