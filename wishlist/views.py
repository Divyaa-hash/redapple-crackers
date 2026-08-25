from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Wishlist, WishlistItem
from products.models import Product


def get_or_create_wishlist(request):
    """Get existing wishlist or create new one for user"""
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        return wishlist
    else:
        # For anonymous users, use session-based wishlist
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        wishlist, created = Wishlist.objects.get_or_create(session_key=session_key)
        return wishlist


def wishlist_view(request):
    """Render wishlist page"""
    wishlist = get_or_create_wishlist(request)
    wishlist_items = wishlist.items.all()
    return render(request, 'wishlist.html', {'wishlist': wishlist, 'wishlist_items': wishlist_items})


def wishlist_summary(request):
    """Get wishlist summary for AJAX requests"""
    wishlist = get_or_create_wishlist(request)
    return JsonResponse({
        'total_items': wishlist.items.count(),
        'wishlist_count': wishlist.items.count()
    })


@csrf_exempt
@require_POST
def add_to_wishlist(request):
    """Add product to wishlist"""
    product_id = request.POST.get('product_id')
    
    product = get_object_or_404(Product, id=product_id, is_active=True)
    wishlist = get_or_create_wishlist(request)
    
    wishlist_item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )
    
    if created:
        return JsonResponse({
            'success': True,
            'message': 'Product added to wishlist',
            'total_items': wishlist.items.count()
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Product already in wishlist'
        })


@csrf_exempt
@require_POST
def remove_from_wishlist(request):
    """Remove item from wishlist"""
    item_id = request.POST.get('item_id')
    wishlist_item = get_object_or_404(WishlistItem, id=item_id)
    wishlist_item.delete()
    
    return JsonResponse({
        'success': True,
        'message': 'Item removed from wishlist'
    })


@csrf_exempt
@require_POST
def move_to_cart(request):
    """Move item from wishlist to cart"""
    item_id = request.POST.get('item_id')
    wishlist_item = get_object_or_404(WishlistItem, id=item_id)
    
    # Add to cart (import cart function)
    from cart.views import get_or_create_cart
    cart = get_or_create_cart(request)
    
    from cart.models import CartItem
    CartItem.objects.get_or_create(
        cart=cart,
        product=wishlist_item.product,
        defaults={'quantity': 1, 'unit_price': wishlist_item.product.get_current_price()}
    )
    
    # Remove from wishlist
    wishlist_item.delete()
    
    return JsonResponse({
        'success': True,
        'message': 'Item moved to cart'
    })
