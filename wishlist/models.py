from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from products.models import Product


class Wishlist(models.Model):
    """
    Wishlist for users to save favorite products.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist', null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Wishlist')
        verbose_name_plural = _('Wishlists')
    
    def __str__(self):
        if self.user:
            return f"Wishlist - {self.user.email}"
        return f"Wishlist - Session {self.session_key}"
    
    def get_total_items(self):
        return self.items.count()


class WishlistItem(models.Model):
    """
    Individual items in a wishlist.
    """
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Wishlist Item')
        verbose_name_plural = _('Wishlist Items')
        unique_together = ['wishlist', 'product']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.wishlist} - {self.product.name}"
