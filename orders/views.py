from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Order, OrderItem, ShippingAddress
from cart.views import get_or_create_cart
from products.models import Product
from siteadmin.models import Notification
from decimal import Decimal
import razorpay


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
    
    # Calculate totals
    subtotal = cart.get_total_price()
    shipping_charge = Decimal('99.00')
    gst = round(subtotal * Decimal('0.18'), 2)
    total = subtotal + shipping_charge + gst
    
    # Initialize Razorpay client if credentials are available
    razorpay_client = None
    razorpay_order = None
    if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
        try:
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            # Create Razorpay order
            razorpay_order_data = {
                'amount': int(total * 100),  # Amount in paise
                'currency': settings.RAZORPAY_CURRENCY,
                'receipt': f'receipt_{int(total)}',
                'payment_capture': '1'
            }
            razorpay_order = razorpay_client.order.create(data=razorpay_order_data)
        except Exception as e:
            print(f"Razorpay initialization error: {e}")
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'saved_addresses': saved_addresses,
        'subtotal': subtotal,
        'shipping_charge': shipping_charge,
        'gst': gst,
        'total': total,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order': razorpay_order,
    }
    
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
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    razorpay_signature = request.POST.get('razorpay_signature', '')
    
    # Calculate totals
    subtotal = cart.get_total_price()
    shipping_charge = Decimal('99.00')
    gst = round(subtotal * Decimal('0.18'), 2)
    total_amount = subtotal + shipping_charge + gst
    
    # Verify Razorpay payment if provided
    payment_status = 'pending'
    if payment_method != 'cod' and razorpay_payment_id and razorpay_order_id and razorpay_signature:
        if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
            try:
                razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                params = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                }
                razorpay_client.utility.verify_payment_signature(params)
                payment_status = 'completed'
            except Exception as e:
                print(f"Razorpay verification error: {e}")
                return JsonResponse({'success': False, 'message': 'Payment verification failed'})
        else:
            return JsonResponse({'success': False, 'message': 'Payment gateway not configured'})
    elif payment_method == 'cod':
        payment_status = 'pending'
    
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
        payment_status=payment_status,
        payment_id=razorpay_payment_id if payment_method != 'cod' else '',
        order_status='confirmed' if payment_status == 'completed' else 'pending'
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
            product_image=cart_item.product.get_display_image()
        )
    
    # Clear cart
    cart_items.delete()
    
    # Create notification for the user if authenticated
    if user:
        Notification.objects.create(
            user=user,
            title=f'Order #{order.order_number} Placed Successfully',
            message=f'Your order has been placed successfully. Total: ₹{total_amount:.2f}',
            notification_type='order',
            link=f'/orders/{order.order_number}/',
            is_read=False
        )
    
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
