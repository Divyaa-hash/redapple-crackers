from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Banner(models.Model):
    """
    Banner management for homepage and other pages.
    """
    BANNER_TYPES = [
        ('hero', _('Hero Banner')),
        ('promo', _('Promotional Banner')),
        ('category', _('Category Banner')),
        ('announcement', _('Announcement')),
    ]
    
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPES, default='hero')
    image = models.ImageField(upload_to='banners/')
    mobile_image = models.ImageField(upload_to='banners/mobile/', blank=True, null=True)
    link = models.URLField(blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title


class Notification(models.Model):
    """
    Notification system for users.
    """
    NOTIFICATION_TYPES = [
        ('order', _('Order Update')),
        ('promo', _('Promotional')),
        ('system', _('System')),
        ('review', _('Review')),
    ]
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    link = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """
    Global site settings.
    """
    site_name = models.CharField(max_length=255, default='Premium Fireworks')
    site_tagline = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True)
    
    # Contact info
    contact_email = models.EmailField(default='info@premiumfireworks.com')
    contact_phone = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    
    # Social media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # SEO
    default_meta_title = models.CharField(max_length=255, blank=True)
    default_meta_description = models.TextField(blank=True)
    
    # Currency
    currency_symbol = models.CharField(max_length=5, default='₹')
    currency_code = models.CharField(max_length=3, default='INR')
    
    # Shipping
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    default_shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Tax
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18)
    
    # Maintenance mode
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')
    
    def __str__(self):
        return self.site_name


class CMSPage(models.Model):
    """
    Custom CMS pages for static content.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    show_in_menu = models.BooleanField(default=False)
    menu_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('CMS Page')
        verbose_name_plural = _('CMS Pages')
        ordering = ['menu_order', 'title']
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """
    Customer testimonials.
    """
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    testimonial = models.TextField()
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating} stars"