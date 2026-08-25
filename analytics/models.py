from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product, User


class ProductView(models.Model):
    """
    Track product views for analytics.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='analytics_views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_views')
    session_key = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Product View')
        verbose_name_plural = _('Product Views')
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['viewed_at']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        return f"{self.product.name} - {self.viewed_at}"


class CartAbandonment(models.Model):
    """
    Track abandoned carts for recovery.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='abandoned_carts')
    session_key = models.CharField(max_length=255, blank=True)
    products = models.JSONField(default=list)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    abandoned_at = models.DateTimeField(auto_now_add=True)
    recovered = models.BooleanField(default=False)
    recovered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Cart Abandonment')
        verbose_name_plural = _('Cart Abandonments')
        ordering = ['-abandoned_at']
    
    def __str__(self):
        return f"Abandoned Cart - {self.user.email if self.user else self.session_key}"


class SearchQuery(models.Model):
    """
    Track search queries for analytics and improvement.
    """
    query = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='search_queries')
    session_key = models.CharField(max_length=255, blank=True)
    results_count = models.IntegerField(default=0)
    clicked_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='search_clicks')
    searched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Search Query')
        verbose_name_plural = _('Search Queries')
        ordering = ['-searched_at']
        indexes = [
            models.Index(fields=['query']),
            models.Index(fields=['searched_at']),
        ]
    
    def __str__(self):
        return self.query


class SalesReport(models.Model):
    """
    Daily sales reports and analytics.
    """
    date = models.DateField(unique=True)
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_products_sold = models.IntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unique_customers = models.IntegerField(default=0)
    returning_customers = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Sales Report')
        verbose_name_plural = _('Sales Reports')
        ordering = ['-date']
    
    def __str__(self):
        return f"Sales Report - {self.date}"


class TopProduct(models.Model):
    """
    Track top performing products.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='top_performances')
    period = models.CharField(max_length=50)  # daily, weekly, monthly
    views_count = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rank = models.IntegerField(default=0)
    period_start = models.DateField()
    period_end = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Top Product')
        verbose_name_plural = _('Top Products')
        ordering = ['period', 'rank']
    
    def __str__(self):
        return f"{self.product.name} - #{self.rank} ({self.period})"


class UserActivity(models.Model):
    """
    Track user activities for behavior analysis.
    """
    ACTIVITY_TYPES = [
        ('view', _('Product View')),
        ('search', _('Search')),
        ('add_to_cart', _('Add to Cart')),
        ('remove_from_cart', _('Remove from Cart')),
        ('wishlist', _('Add to Wishlist')),
        ('checkout', _('Checkout')),
        ('purchase', _('Purchase')),
        ('review', _('Review')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    session_key = models.CharField(max_length=255, blank=True)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_activities')
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('User Activity')
        verbose_name_plural = _('User Activities')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['activity_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.activity_type} - {self.user.email if self.user else self.session_key}"