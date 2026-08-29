from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Cart, CartItem
from products.models import Product


def get_or_create_cart(request):
    """Get existing cart or create new one for user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            request.session.save()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    # Ensure session is saved for non-authenticated users
    if not request.user.is_authenticated:
        request.session.save()
    
    return cart


def cart_view(request):
    """Render cart page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    subtotal = cart.get_total_price()
    shipping = Decimal('99')
    gst_amount = subtotal * Decimal('0.18')
    total = subtotal + shipping + gst_amount
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'gst_amount': gst_amount,
        'total': total
    })


@csrf_exempt
@require_POST
def add_to_cart(request):
    """Add product to cart"""
    try:
        # Handle both JSON and POST data
        if request.content_type == 'application/json':
            import json
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
        else:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
        
        if not product_id:
            return JsonResponse({'success': False, 'message': 'No product ID provided'})
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
        
        if not product.is_in_stock():
            return JsonResponse({'success': False, 'message': 'Product is out of stock'})
        
        cart = get_or_create_cart(request)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity, 'unit_price': product.get_current_price()}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.unit_price = product.get_current_price()
            cart_item.save()
        
        # Ensure session is saved
        if not request.user.is_authenticated:
            request.session.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_count': cart.get_total_items(),
            'cart_total': str(cart.get_total_price())
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@require_POST
def update_cart_item(request):
    """Update cart item quantity"""
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    cart = cart_item.cart
    return JsonResponse({
        'success': True,
        'cart_total': cart.get_total_price(),
        'item_total': cart_item.get_total_price()
    })


@csrf_exempt
@require_POST
def remove_from_cart(request):
    """Remove item from cart"""
    item_id = request.POST.get('item_id')
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    cart_item.delete()
    
    return JsonResponse({
        'success': True,
        'message': 'Item removed from cart',
        'cart_count': cart.get_total_items(),
        'cart_total': cart.get_total_price()
    })


def cart_summary(request):
    """Get cart summary for AJAX requests"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    items_data = []
    for item in cart_items:
        items_data.append({
            'id': item.id,
            'product_id': item.product.id,
            'product_name': item.product.name,
            'product_image': item.product.get_display_image(),
            'quantity': item.quantity,
            'unit_price': str(item.unit_price),
            'total_price': str(item.get_total_price())
        })
    
    return JsonResponse({
        'total_items': cart.get_total_items(),
        'cart_count': cart.get_total_items(),
        'cart_total': str(cart.get_total_price()),
        'items': items_data
    })
