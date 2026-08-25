from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, ProductReview, Festival, Coupon


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent', 'is_active', 'order']
        read_only_fields = ['id']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'description', 'website', 'is_featured', 'is_active']
        read_only_fields = ['id']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    current_price = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'sku', 'category', 'category_name', 'brand', 'brand_name',
            'product_type', 'safety_level', 'short_description', 'description', 'safety_instructions',
            'regular_price', 'sale_price', 'wholesale_price', 'current_price', 'discount_percentage',
            'stock', 'low_stock_threshold', 'main_image', 'additional_images', 'video_url',
            'weight', 'dimensions', 'pieces', 'duration',
            'is_featured', 'is_new', 'is_bestseller', 'is_digital',
            'meta_title', 'meta_description', 'meta_keywords',
            'is_active', 'average_rating', 'images', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_current_price(self, obj):
        return obj.get_current_price()
    
    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()
    
    def get_average_rating(self, obj):
        return obj.get_average_rating()


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    current_price = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'sku', 'category_name', 'short_description',
            'regular_price', 'sale_price', 'current_price', 'discount_percentage',
            'main_image', 'stock', 'is_featured', 'is_new', 'is_bestseller',
            'average_rating', 'created_at'
        ]
    
    def get_current_price(self, obj):
        return obj.get_current_price()
    
    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()
    
    def get_average_rating(self, obj):
        return obj.get_average_rating()


class ProductReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'product', 'product_name', 'user', 'user_email', 'rating',
            'title', 'comment', 'is_approved', 'is_verified_purchase', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'is_verified_purchase', 'created_at']


class FestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival
        fields = ['id', 'name', 'slug', 'description', 'image', 'start_date', 'end_date', 'is_active']
        read_only_fields = ['id']


class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'description', 'discount_type', 'discount_value',
            'minimum_order_value', 'maximum_discount', 'usage_limit', 'used_count',
            'valid_from', 'valid_until', 'is_active', 'is_valid'
        ]
        read_only_fields = ['id', 'used_count']
    
    def get_is_valid(self, obj):
        return obj.is_valid()
