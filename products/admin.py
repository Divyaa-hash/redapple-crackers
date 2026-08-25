from django.contrib import admin
from .models import (
    Category, Brand, Product, ProductImage, ProductReview, Festival, Coupon,
    GiftCard, LoyaltyReward, RecentlyViewed, ProductComparison, FlashSale, PincodeAvailability
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_featured', 'is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'brand', 'regular_price', 'sale_price', 'stock', 'is_active', 'is_featured', 'is_new', 'is_trending', 'created_at']
    list_filter = ['is_active', 'is_featured', 'is_new', 'is_bestseller', 'is_trending', 'is_limited_edition', 'category', 'brand', 'product_type', 'safety_level', 'festival']
    search_fields = ['name', 'sku', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    ordering = ['-created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'brand', 'festival')
        }),
        ('Product Details', {
            'fields': ('product_type', 'safety_level', 'short_description', 'description', 'safety_instructions')
        }),
        ('Pricing', {
            'fields': ('regular_price', 'sale_price', 'wholesale_price')
        }),
        ('Inventory', {
            'fields': ('stock', 'low_stock_threshold')
        }),
        ('Images', {
            'fields': ('main_image', 'additional_images', 'video_url', 'image_360')
        }),
        ('Specifications', {
            'fields': ('weight', 'dimensions', 'pieces', 'duration', 'sound_level', 'height')
        }),
        ('Features', {
            'fields': ('is_featured', 'is_new', 'is_bestseller', 'is_digital', 'is_trending', 'is_limited_edition')
        }),
        ('Premium Features', {
            'fields': ('has_free_shipping', 'has_gift_wrap', 'reward_points')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'is_approved', 'is_verified_purchase', 'created_at']
    list_filter = ['is_approved', 'is_verified_purchase', 'rating']
    search_fields = ['title', 'comment', 'user__email', 'product__name']
    ordering = ['-created_at']


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'start_date', 'end_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'minimum_order_value', 'usage_limit', 'used_count', 'is_active', 'valid_from', 'valid_until']
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'description']
    ordering = ['-created_at']


@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount', 'balance', 'sender_name', 'recipient_name', 'is_active', 'expiry_date']
    list_filter = ['is_active', 'expiry_date']
    search_fields = ['code', 'sender_name', 'recipient_email']


@admin.register(LoyaltyReward)
class LoyaltyRewardAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'tier', 'total_spent']
    list_filter = ['tier']
    search_fields = ['user__email']


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['product__name', 'user__email']


@admin.register(ProductComparison)
class ProductComparisonAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__email']


@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_percentage', 'start_time', 'end_time', 'is_active']
    list_filter = ['is_active', 'start_time', 'end_time']
    search_fields = ['name']
    filter_horizontal = ['products']


@admin.register(PincodeAvailability)
class PincodeAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['pincode', 'city', 'state', 'is_available', 'delivery_days']
    list_filter = ['is_available', 'state']
    search_fields = ['pincode', 'city', 'state']
