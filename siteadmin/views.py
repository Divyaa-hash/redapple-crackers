from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, F
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from orders.models import Order, OrderItem
from products.models import Product
from users.models import User

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return render(request, 'error.html', {'message': 'Access denied'})
    
    # Get current date and time
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Order statistics
    total_orders = Order.objects.count()
    today_orders = Order.objects.filter(created_at__date=today).count()
    week_orders = Order.objects.filter(created_at__date__gte=week_ago).count()
    month_orders = Order.objects.filter(created_at__date__gte=month_ago).count()
    
    # Revenue statistics
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    today_revenue = Order.objects.filter(created_at__date=today).aggregate(total=Sum('total_amount'))['total'] or 0
    week_revenue = Order.objects.filter(created_at__date__gte=week_ago).aggregate(total=Sum('total_amount'))['total'] or 0
    month_revenue = Order.objects.filter(created_at__date__gte=month_ago).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Order status breakdown
    pending_orders = Order.objects.filter(order_status='pending').count()
    confirmed_orders = Order.objects.filter(order_status='confirmed').count()
    processing_orders = Order.objects.filter(order_status='processing').count()
    shipped_orders = Order.objects.filter(order_status='shipped').count()
    delivered_orders = Order.objects.filter(order_status='delivered').count()
    cancelled_orders = Order.objects.filter(order_status='cancelled').count()
    
    # Recent orders
    recent_orders = Order.objects.order_by('-created_at')[:10]
    
    # Top selling products
    top_products = OrderItem.objects.values('product__name').annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('unit_price'))
    ).order_by('-total_sold')[:10]
    
    # Customer statistics
    total_customers = User.objects.count()
    new_customers = User.objects.filter(created_at__date__gte=month_ago).count()
    
    # Product statistics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    out_of_stock = Product.objects.filter(stock=0).count()
    low_stock = Product.objects.filter(stock__lte=F('low_stock_threshold')).count()
    
    context = {
        'total_orders': total_orders,
        'today_orders': today_orders,
        'week_orders': week_orders,
        'month_orders': month_orders,
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'week_revenue': week_revenue,
        'month_revenue': month_revenue,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'total_customers': total_customers,
        'new_customers': new_customers,
        'total_products': total_products,
        'active_products': active_products,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
    }
    
    return render(request, 'siteadmin/admin_dashboard.html', context)


def admin_orders(request):
    """Admin orders view"""
    if not request.user.is_staff:
        return render(request, 'error.html', {'message': 'Access denied'})
    
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'siteadmin/admin_orders.html', {'orders': orders})


def admin_products(request):
    """Admin products view"""
    if not request.user.is_staff:
        return render(request, 'error.html', {'message': 'Access denied'})
    
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'siteadmin/admin_products.html', {'products': products})


def notification_list(request):
    """Notification list view"""
    if not request.user.is_staff:
        return render(request, 'error.html', {'message': 'Access denied'})
    
    # Placeholder for notification system
    return render(request, 'siteadmin/notification_list.html', {'notifications': []})


def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    if not request.user.is_staff:
        return render(request, 'error.html', {'message': 'Access denied'})
    
    # Placeholder for notification marking
    return redirect('siteadmin:notification_list')


def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    if not request.user.is_staff:
        return render(request, 'error.html', {'message': 'Access denied'})
    
    # Placeholder for marking all notifications
    return redirect('siteadmin:notification_list')


def notification_center(request):
    """Notification center view"""
    if not request.user.is_staff:
        return render(request, 'error.html', {'message': 'Access denied'})
    
    # Placeholder for notification center
    return render(request, 'siteadmin/notification_center.html', {'notifications': []})


def send_whatsapp_notification(order):
    """Send WhatsApp notification for new order"""
    try:
        # Get WhatsApp admin number from settings
        whatsapp_number = getattr(settings, 'WHATSAPP_ADMIN_NUMBER', '9345980679')
        
        # Prepare message
        message = f"""
🎉 *NEW ORDER RECEIVED* 🎉

Order Number: {order.order_number}
Customer: {order.shipping_name}
Phone: {order.shipping_phone}
Amount: ₹{order.total_amount}
Status: {order.get_order_status_display().upper()}

Shipping Address:
{order.shipping_address_line1}
{order.shipping_address_line2}
{order.shipping_city}, {order.shipping_state}
{order.shipping_postal_code}

Items:
"""
        for item in order.items.all():
            message += f"- {item.product.name} x {item.quantity} = ₹{item.total_price}\n"
        
        message += f"\nTotal: ₹{order.total_amount}"
        
        # Use WhatsApp API (you'll need to integrate with a service like Twilio, WhatsApp Business API, etc.)
        # This is a placeholder - you'll need to set up actual WhatsApp API integration
        print(f"WhatsApp notification sent to {whatsapp_number}: {message}")
        
        return True
    except Exception as e:
        print(f"Error sending WhatsApp notification: {e}")
        return False
