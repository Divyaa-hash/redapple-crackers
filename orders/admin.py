from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress, OrderTracking


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'unit_price', 'total_price']


class OrderTrackingInline(admin.TabularInline):
    model = OrderTracking
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'order_status', 'payment_status', 'payment_method', 'total_amount', 'created_at']
    list_filter = ['order_status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'shipping_name', 'shipping_phone', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'shipped_at', 'delivered_at']
    inlines = [OrderItemInline, OrderTrackingInline]
    ordering = ['-created_at']
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'order_status', 'payment_status', 'payment_method', 'payment_id')
        }),
        ('Shipping Address', {
            'fields': ('shipping_name', 'shipping_phone', 'shipping_address_line1', 'shipping_address_line2', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country')
        }),
        ('Billing Address', {
            'fields': ('billing_name', 'billing_phone', 'billing_address_line1', 'billing_address_line2', 'billing_city', 'billing_state', 'billing_postal_code', 'billing_country')
        }),
        ('Order Details', {
            'fields': ('subtotal', 'discount_amount', 'coupon_code', 'shipping_charge', 'gst_amount', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('notes', 'customer_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at')
        }),
    )


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'city', 'state', 'postal_code', 'is_default', 'created_at']
    list_filter = ['is_default', 'state', 'city']
    search_fields = ['name', 'user__email', 'city', 'state']


@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'location', 'tracking_number', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['status', 'tracking_number', 'order__order_number']
    ordering = ['-created_at']
