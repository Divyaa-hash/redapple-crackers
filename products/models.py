from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from users.models import User


class Category(models.Model):
    """
    Category model for organizing fireworks products.
    Supports hierarchical structure with parent-child relationships.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    # SEO fields
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'slug': self.slug})
    
    def get_children(self):
        return self.children.filter(is_active=True)


class Brand(models.Model):
    """
    Brand model for fireworks manufacturers.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Main Product model for fireworks items.
    """
    PRODUCT_TYPE_CHOICES = [
        ('single', _('Single Item')),
        ('box', _('Box')),
        ('combo', _('Combo Pack')),
        ('gift_box', _('Gift Box')),
    ]
    
    SAFETY_LEVEL_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
    ]
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    
    # Category and Brand
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    # Product Type and Safety
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='single')
    safety_level = models.CharField(max_length=20, choices=SAFETY_LEVEL_CHOICES, default='medium')
    
    # Description
    short_description = models.CharField(max_length=500)
    description = models.TextField()
    safety_instructions = models.TextField(blank=True)
    
    # Pricing
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Inventory
    stock = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    
    # Images
    main_image = models.ImageField(upload_to='products/')
    additional_images = models.JSONField(default=list, blank=True)
    video_url = models.URLField(blank=True)
    image_360 = models.ImageField(upload_to='products/360/', blank=True, null=True)
    
    # Specifications
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Weight in grams')
    dimensions = models.CharField(max_length=100, blank=True, help_text='L x W x H in cm')
    pieces = models.IntegerField(default=1, help_text='Number of pieces in pack')
    duration = models.CharField(max_length=50, blank=True, help_text='Duration of firework')
    sound_level = models.CharField(max_length=50, blank=True, help_text='Sound level in decibels')
    height = models.CharField(max_length=50, blank=True, help_text='Maximum height')
    
    # Features
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_limited_edition = models.BooleanField(default=False)
    
    # Premium Features
    has_free_shipping = models.BooleanField(default=False)
    has_gift_wrap = models.BooleanField(default=False)
    reward_points = models.IntegerField(default=0)
    
    # Festival Related
    festival = models.ForeignKey('Festival', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    viewed_count = models.IntegerField(default=0)
    purchased_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_featured']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    def get_catalog_image(self):
        """Local static path for catalogue images (no external URLs)."""
        if isinstance(self.additional_images, list) and self.additional_images:
            first = self.additional_images[0]
            if isinstance(first, str) and first.startswith('images/crackers/'):
                return first
        return f'images/crackers/{self.slug}.jpg'
    
    def get_current_price(self):
        return self.sale_price if self.sale_price else self.regular_price
    
    def get_discount_percentage(self):
        if self.sale_price:
            return int(((self.regular_price - self.sale_price) / self.regular_price) * 100)
        return 0
    
    def is_in_stock(self):
        return self.stock > 0
    
    def is_low_stock(self):
        return self.stock <= self.low_stock_threshold
    
    def get_average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0


class ProductImage(models.Model):
    """
    Additional product images.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


class ProductReview(models.Model):
    """
    Product reviews by customers.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=255)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_verified_purchase = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')
        ordering = ['-created_at']
        unique_together = ['product', 'user']
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name}"


class Festival(models.Model):
    """
    Festival model for seasonal offers and themes.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='festivals/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Festival')
        verbose_name_plural = _('Festivals')
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name


class Coupon(models.Model):
    """
    Coupon/Discount code model.
    """
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', _('Percentage')),
        ('fixed', _('Fixed Amount')),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usage_limit = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.code
    
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_until:
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        return True


class GiftCard(models.Model):
    """
    Gift Card model for gifting fireworks.
    """
    code = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    sender_name = models.CharField(max_length=255)
    sender_email = models.EmailField()
    recipient_name = models.CharField(max_length=255)
    recipient_email = models.EmailField()
    message = models.TextField(blank=True)
    template = models.CharField(max_length=50, default='default')
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Gift Card')
        verbose_name_plural = _('Gift Cards')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.amount}"


class LoyaltyReward(models.Model):
    """
    Loyalty rewards program for customers.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loyalty_rewards')
    points = models.IntegerField(default=0)
    tier = models.CharField(max_length=50, default='bronze')
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Loyalty Reward')
        verbose_name_plural = _('Loyalty Rewards')
    
    def __str__(self):
        return f"{self.user.email} - {self.points} points"


class RecentlyViewed(models.Model):
    """
    Track recently viewed products for users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='recently_viewed')
    session_key = models.CharField(max_length=255, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Recently Viewed')
        verbose_name_plural = _('Recently Viewed')
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.product.name} - {self.viewed_at}"


class ProductComparison(models.Model):
    """
    Product comparison feature.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comparisons', null=True, blank=True)
    session_key = models.CharField(max_length=255, blank=True)
    products = models.ManyToManyField(Product, related_name='comparisons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Product Comparison')
        verbose_name_plural = _('Product Comparisons')
    
    def __str__(self):
        return f"Comparison - {self.user.email if self.user else self.session_key}"


class FlashSale(models.Model):
    """
    Flash sale model for limited time offers.
    """
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product, related_name='flash_sales')
    discount_percentage = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Flash Sale')
        verbose_name_plural = _('Flash Sales')
        ordering = ['-start_time']
    
    def __str__(self):
        return self.name
    
    def is_active_now(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time


class PincodeAvailability(models.Model):
    """
    Check product availability by pincode.
    """
    pincode = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    delivery_days = models.IntegerField(default=3)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Pincode Availability')
        verbose_name_plural = _('Pincode Availabilities')
    
    def __str__(self):
        return f"{self.pincode} - {self.city}"
