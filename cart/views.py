from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Cart, CartItem
from products.models import Product
from orders.models import Order, OrderItem
from users.models import User


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
    
    # Recalculate subtotal from items to ensure accuracy
    subtotal = sum(item.get_total_price() for item in cart_items)
    total = subtotal
    
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
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
        
        # Delete any existing cart items for this product first
        CartItem.objects.filter(cart=cart, product=product).delete()
        
        # Create new cart item
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity,
            unit_price=product.get_current_price()
        )
        
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
def clear_cart(request):
    """Clear all items from cart"""
    try:
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        
        # Ensure session is saved
        if not request.user.is_authenticated:
            request.session.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared'
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
    product_id = request.POST.get('product_id')

    cart = get_or_create_cart(request)

    if item_id:
        # Remove by item_id
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
    elif product_id:
        # Remove by product_id (for shop page)
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Item not found in cart'
            })
    else:
        return JsonResponse({
            'success': False,
            'message': 'No item_id or product_id provided'
        })

    return JsonResponse({
        'success': True,
        'message': 'Item removed from cart',
        'cart_count': cart.get_total_items(),
        'cart_total': str(cart.get_total_price())
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


@csrf_exempt
def create_whatsapp_order(request):
    """Create order from WhatsApp checkout and return WhatsApp message"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        name = data.get('name')
        mobile = data.get('mobile')
        address = data.get('address')
        pincode = data.get('pincode')
        
        # Get cart
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            return JsonResponse({'success': False, 'message': 'Cart is empty'})
        
        # Calculate totals
        subtotal = cart.get_total_price()
        
        # Removed minimum order validation - allow orders of any value
        # if subtotal < Decimal('2500.00'):
        #     return JsonResponse({'success': False, 'message': 'Minimum order value is ₹2500. Please add more products to your cart.'})
        
        shipping_charge = Decimal('0.00')
        gst = Decimal('0.00')
        total = subtotal
        
        # Create or get user
        user = None
        if request.user.is_authenticated:
            user = request.user
        else:
            # Create guest user
            try:
                user = User.objects.create_user(
                    email=f'guest_{mobile}@temp.com',
                    username=f'guest_{mobile}',
                    first_name=name,
                    phone=mobile
                )
            except:
                user = User.objects.filter(phone=mobile).first()
        
        # Create order
        order = Order.objects.create(
            user=user,
            shipping_name=name,
            shipping_phone=mobile,
            shipping_address_line1=address,
            shipping_address_line2='',
            shipping_city='',
            shipping_state='',
            shipping_postal_code=pincode,
            shipping_country='India',
            billing_name=name,
            billing_phone=mobile,
            billing_address_line1=address,
            billing_address_line2='',
            billing_city='',
            billing_state='',
            billing_postal_code=pincode,
            billing_country='India',
            subtotal=subtotal,
            shipping_charge=shipping_charge,
            gst_amount=gst,
            total_amount=total,
            payment_method='upi',
            payment_status='pending',
            payment_id='',
            order_status='pending'
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
        
        # Create notification for admin
        try:
            from siteadmin.models import Notification
            Notification.objects.create(
                title=f'New Order - {order.order_number}',
                message=f'New order from {name} for ₹{total}. Status: Pending',
                notification_type='order',
                link=f'/admin/orders/order/{order.id}/change/'
            )
        except:
            pass  # Skip notification if siteadmin app not ready
        
        # Generate WhatsApp message
        message = f"""*NEW ORDER - RED APPLE CRACKERS*

Order Number: {order.order_number}
Customer: {name}
Phone: {mobile}
Address: {address}, {pincode}

*Items:*
"""
        for item in order.items.all():
            message += f"- {item.product_name} x {item.quantity} = {item.total_price}\n"
        
        message += f"""
*Order Total: {order.total_amount}*
Payment: UPI Payment
Status: Pending

Thank you for your order!"""
        
        # WhatsApp admin number
        whatsapp_number = '9345980679'
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={message.replace(' ', '%20').replace('\n', '%0A')}"
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'order_id': order.id,
            'whatsapp_url': whatsapp_url,
            'message': message,
            'status': 'Order created successfully and pending confirmation',
            'redirect_url': f'/order-confirmation/{order.order_number}/'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def order_confirmation(request, order_number):
    """Order confirmation page"""
    try:
        order = Order.objects.get(order_number=order_number)
        return render(request, 'order_confirmation.html', {
            'order': order,
            'order_number': order.order_number,
            'total_amount': order.total_amount,
            'order_date': order.created_at.strftime('%Y-%m-%d %H:%M')
        })
    except Order.DoesNotExist:
        return render(request, 'order_confirmation.html', {
            'order': None,
            'order_number': 'Unknown',
            'total_amount': '0',
            'order_date': 'Unknown'
        })
