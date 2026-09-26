from django.shortcuts import render, redirect
from django.db.models import Count, Sum, F
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from orders.models import Order, OrderItem
from products.models import Product
from users.models import User
from .utils import send_whatsapp_notification

def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/?next=/siteadmin/dashboard/')
    
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
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/?next=/siteadmin/admin-orders/')
    
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'siteadmin/admin_orders.html', {'orders': orders})


def admin_products(request):
    """Admin products view"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/?next=/siteadmin/admin-products/')
    
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'siteadmin/admin_products.html', {'products': products})


def notification_list(request):
    """Notification list view"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/?next=/siteadmin/notifications/')
    
    # Placeholder for notification system
    return render(request, 'siteadmin/notification_list.html', {'notifications': []})


def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/?next=/siteadmin/notifications/')
    
    # Placeholder for notification marking
    return redirect('siteadmin:notification_list')


def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/?next=/siteadmin/notifications/mark-all-read/')
    
    # Placeholder for marking all notifications
    return redirect('siteadmin:notification_list')


def notification_center(request):
    """Notification center view"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/?next=/siteadmin/notification-center/')
    
    # Placeholder for notification center
    return render(request, 'siteadmin/notification_center.html', {'notifications': []})
