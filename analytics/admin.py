from django.contrib import admin
from .models import ProductView, CartAbandonment, SearchQuery, SalesReport, TopProduct, UserActivity


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'viewed_at', 'ip_address']
    list_filter = ['viewed_at', 'product']
    search_fields = ['product__name', 'user__email', 'session_key']
    readonly_fields = ['viewed_at']


@admin.register(CartAbandonment)
class CartAbandonmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_value', 'abandoned_at', 'recovered']
    list_filter = ['abandoned_at', 'recovered']
    search_fields = ['user__email', 'session_key']
    readonly_fields = ['abandoned_at']


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'results_count', 'searched_at']
    list_filter = ['searched_at']
    search_fields = ['query']
    readonly_fields = ['searched_at']


@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_orders', 'total_revenue', 'average_order_value']
    list_filter = ['date']
    readonly_fields = ['date', 'created_at', 'updated_at']


@admin.register(TopProduct)
class TopProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'period', 'rank', 'sales_count', 'revenue']
    list_filter = ['period', 'period_start', 'period_end']
    search_fields = ['product__name']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_type', 'user', 'product', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__email', 'session_key', 'product__name']
    readonly_fields = ['created_at']