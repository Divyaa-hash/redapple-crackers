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
    list_display = ['title', 'notification_type', 'user', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__email']


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