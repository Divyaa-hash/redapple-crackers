from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem, ShippingAddress
from cart.views import get_or_create_cart
from products.models import Product
from decimal import Decimal


def checkout_view(request):
    """Multi-step checkout process"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty')
        return redirect('home')
    
    # Get user's saved addresses if logged in
    saved_addresses = []
    if request.user.is_authenticated:
        saved_addresses = ShippingAddress.objects.filter(user=request.user)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'saved_addresses': saved_addresses,
        'subtotal': cart.get_total_price(),
        'shipping_charge': Decimal('99.00'),
        'gst': round(cart.get_total_price() * Decimal('0.18'), 2),
    }
    
    context['total'] = context['subtotal'] + context['shipping_charge'] + context['gst']
    
    return render(request, 'checkout.html', context)


@csrf_exempt
@require_POST
def process_checkout(request):
    """Process checkout and create order"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        return JsonResponse({'success': False, 'message': 'Cart is empty'})
    
    # Get form data
    shipping_name = request.POST.get('shipping_name')
    shipping_phone = request.POST.get('shipping_phone')
    shipping_address_line1 = request.POST.get('shipping_address_line1')
    shipping_address_line2 = request.POST.get('shipping_address_line2', '')
    shipping_city = request.POST.get('shipping_city')
    shipping_state = request.POST.get('shipping_state')
    shipping_postal_code = request.POST.get('shipping_postal_code')
    shipping_country = request.POST.get('shipping_country', 'India')
    
    payment_method = request.POST.get('payment_method', 'cod')
    
    # Calculate totals
    subtotal = cart.get_total_price()
    shipping_charge = Decimal('99.00')
    gst = round(subtotal * Decimal('0.18'), 2)
    total_amount = subtotal + shipping_charge + gst
    
    # Create order (with or without user)
    user = request.user if request.user.is_authenticated else None
    
    order = Order.objects.create(
        user=user,
        shipping_name=shipping_name,
        shipping_phone=shipping_phone,
        shipping_address_line1=shipping_address_line1,
        shipping_address_line2=shipping_address_line2,
        shipping_city=shipping_city,
        shipping_state=shipping_state,
        shipping_postal_code=shipping_postal_code,
        shipping_country=shipping_country,
        billing_name=shipping_name,
        billing_phone=shipping_phone,
        billing_address_line1=shipping_address_line1,
        billing_address_line2=shipping_address_line2,
        billing_city=shipping_city,
        billing_state=shipping_state,
        billing_postal_code=shipping_postal_code,
        billing_country=shipping_country,
        subtotal=subtotal,
        shipping_charge=shipping_charge,
        gst_amount=gst,
        total_amount=total_amount,
        payment_method=payment_method,
        order_status='pending',
        payment_status='pending'
    )
    
    # Create order items
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            product_name=cart_item.product.name,
            product_sku=cart_item.product.sku,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            total_price=cart_item.get_total_price(),
            product_image=cart_item.product.main_image.url if cart_item.product.main_image else ''
        )
    
    # Clear cart
    cart_items.delete()
    
    return JsonResponse({
        'success': True,
        'order_number': order.order_number,
        'redirect_url': f'/orders/{order.order_number}/'
    })


def order_detail(request, order_number):
    """View order details"""
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    else:
        # For anonymous users, try to find by order number only
        order = get_object_or_404(Order, order_number=order_number, user__isnull=True)
    
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    
    return render(request, 'order_detail.html', context)


@login_required
def order_tracking(request, order_number):
    """Track order status"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    tracking_history = order.tracking.all()
    
    context = {
        'order': order,
        'tracking_history': tracking_history,
    }
    
    return render(request, 'order_tracking.html', context)


@login_required
def order_list(request):
    """List all user orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'order_list.html', context)
