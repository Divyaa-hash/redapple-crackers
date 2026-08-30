from django.contrib import admin
from .models import Banner, Notification, SiteSettings, CMSPage, Testimonial


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_type', 'order', 'is_active', 'start_date', 'end_date']
    list_filter = ['banner_type', 'is_active', 'start_date', 'end_date']
    search_fields = ['title', 'subtitle']
    prepopulated_fields = {}


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'user', 'is_read', 'created_at', 'view_link', 'order_details']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__email']
    readonly_fields = ['created_at']
    
    def view_link(self, obj):
        if obj.link:
            return f'<a href="{obj.link}" target="_blank">View</a>'
        return '-'
    view_link.short_description = 'Link'
    view_link.allow_tags = True
    
    def order_details(self, obj):
        if obj.notification_type == 'order' and obj.link:
            # Extract order number from link (e.g., /orders/ORD123/)
            import re
            order_match = re.search(r'/orders/([^/]+)/', obj.link)
            if order_match:
                order_number = order_match.group(1)
                return f'<a href="/admin/orders/order/?q={order_number}" target="_blank">{order_number}</a>'
        return '-'
    order_details.short_description = 'Order'
    order_details.allow_tags = True


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'maintenance_mode']
    fieldsets = (
        ('Basic Info', {
            'fields': ('site_name', 'site_tagline', 'logo', 'favicon')
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone', 'whatsapp_number')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url')
        }),
        ('SEO', {
            'fields': ('default_meta_title', 'default_meta_description')
        }),
        ('Currency & Tax', {
            'fields': ('currency_symbol', 'currency_code', 'gst_rate')
        }),
        ('Shipping', {
            'fields': ('free_shipping_threshold', 'default_shipping_cost')
        }),
        ('Maintenance', {
            'fields': ('maintenance_mode', 'maintenance_message')
        }),
    )


@admin.register(CMSPage)
class CMSPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'show_in_menu', 'menu_order']
    list_filter = ['is_published', 'show_in_menu']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'product', 'is_featured', 'is_approved']
    list_filter = ['rating', 'is_featured', 'is_approved']
    search_fields = ['customer_name', 'testimonial']