from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
import json
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Brand, Product, ProductReview, Festival, Coupon
from .serializers import (
    CategorySerializer, BrandSerializer, ProductSerializer, ProductListSerializer,
    ProductReviewSerializer, FestivalSerializer, CouponSerializer
)


def product_detail_view(request, product_id):
    """Product detail page view"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Get related products from the same category (excluding current product)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).order_by('order', 'name')[:8]
    
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
    """Shop page view displaying all products with filters"""
    try:
        products = Product.objects.filter(is_active=True).select_related('category', 'brand')
        categories = Category.objects.filter(is_active=True)
        
        # Get filter parameters
        category_id = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        in_stock = request.GET.get('in_stock')
        on_sale = request.GET.get('on_sale')
        sort_by = request.GET.get('sort_by', '-created_at')
        search_query = request.GET.get('q')
        page = request.GET.get('page', 1)
        
        # Apply search filter
        if search_query:
            products = products.filter(name__icontains=search_query)
        
        # Apply filters
        if category_id:
            products = products.filter(category_id=category_id)
        # Special handling for Gift Box category filter
        elif category_id and Category.objects.filter(id=category_id, name__icontains='Gift Box').exists():
            products = products.filter(category_id=category_id)
        if min_price:
            products = products.filter(regular_price__gte=min_price)
        if max_price:
            products = products.filter(regular_price__lte=max_price)
        if in_stock:
            products = products.filter(stock__gt=0)
        if on_sale:
            products = products.filter(sale_price__isnull=False)
        
        # Apply sorting - use current price (sale_price if available, else regular_price)
        if sort_by == 'price_low':
            # Sort by current price (sale_price takes precedence)
            products = products.order_by('sale_price', 'regular_price')
        elif sort_by == 'price_high':
            products = products.order_by('-sale_price', '-regular_price')
        elif sort_by == 'newest':
            products = products.order_by('-created_at')
        elif sort_by == 'name':
            products = products.order_by('name')
        else:
            # Default: sort by order field (Baby Crackers website order), then by name
            products = products.order_by('order', 'name')
        
        # Pagination - show all products on one page
        paginator = Paginator(products, 200)
        
        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)
        
        # Serialize categories for JavaScript
        categories_data = [{'id': cat.id, 'name': cat.name} for cat in categories]
        
        return render(request, 'shop.html', {
            'products': products_page,
            'categories': categories,
            'categories_json': json.dumps(categories_data, cls=DjangoJSONEncoder),
            'paginator': paginator,
            'current_page': products_page,
            'total_count': paginator.count
        })
    except Exception as e:
        # Log the error and return a simple error page
        import traceback
        print(f"Error in shop_view: {e}")
        print(traceback.format_exc())
        return render(request, 'shop.html', {
            'products': [],
            'categories': [],
            'paginator': None,
            'current_page': None,
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
