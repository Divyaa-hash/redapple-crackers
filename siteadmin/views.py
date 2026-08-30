from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Notification, SiteSettings
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from products.models import Product, Category
from cart.models import Cart
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


def is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(is_admin_user)
def admin_dashboard(request):
    """Custom admin dashboard overview"""
    # Statistics
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_users = User.objects.count()
    total_revenue = Order.objects.filter(payment_status='completed').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    # Recent notifications
    recent_notifications = Notification.objects.select_related('user').order_by('-created_at')[:10]
    
    # Low stock products
    low_stock_products = Product.objects.filter(stock__lt=10, is_active=True)[:10]
    
    # Today's stats
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today).count()
    today_revenue = Order.objects.filter(
        created_at__date=today,
        payment_status='completed'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Order status breakdown
    order_status_counts = Order.objects.values('order_status').annotate(
        count=Count('id')
    ).order_by('order_status')
    
    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'recent_notifications': recent_notifications,
        'low_stock_products': low_stock_products,
        'today_orders': today_orders,
        'today_revenue': today_revenue,
        'order_status_counts': order_status_counts,
    }
    
    return render(request, 'siteadmin/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin_user)
def admin_orders(request):
    """Admin order management page"""
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    orders = Order.objects.select_related('user').order_by('-created_at')
    
    if status_filter:
        orders = orders.filter(order_status=status_filter)
    
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(shipping_name__icontains=search_query) |
            Q(shipping_phone__icontains=search_query)
        )
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'siteadmin/admin_orders.html', context)


@login_required
@user_passes_test(is_admin_user)
def admin_products(request):
    """Admin product management page"""
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    products = Product.objects.select_related('category').order_by('-created_at')
    
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query)
        )
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'categories': categories,
        'category_filter': category_filter,
        'search_query': search_query,
    }
    
    return render(request, 'siteadmin/admin_products.html', context)


@login_required
def notification_list(request):
    """API endpoint to get user notifications"""
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    data = []
    for notification in notifications:
        data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'type': notification.notification_type,
            'link': notification.link,
            'is_read': notification.is_read,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({
        'notifications': data,
        'unread_count': unread_count
    })


@login_required
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            user=request.user
        )
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'})


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)
    return JsonResponse({'success': True})


@login_required
def notification_center(request):
    """Full notification center page"""
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    unread_count = notifications.filter(is_read=False).count()
    
    return render(request, 'siteadmin/notification_center.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })
