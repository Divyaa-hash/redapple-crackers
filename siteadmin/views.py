from django.shortcuts import render, redirect
from django.db.models import Count, Sum, F
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.http import HttpResponse
from orders.models import Order, OrderItem
from products.models import Product
from users.models import User
from .utils import send_whatsapp_notification
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

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


def export_orders_pdf(request):
    """Export all orders to PDF"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/login/?next=/siteadmin/admin-orders/')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="redapple_orders.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.darkred,
        spaceAfter=30,
        alignment=1  # Center
    )

    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.darkred,
        spaceAfter=12
    )

    # Title
    elements.append(Paragraph("RedApple Crackers - Order Report", title_style))
    elements.append(Spacer(1, 0.2*inch))

    # Date
    elements.append(Paragraph(f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))

    # Orders table header
    data = [['Order ID', 'Customer', 'Email', 'Phone', 'Total', 'Status', 'Date']]

    # Orders data
    orders = Order.objects.all().order_by('-created_at')
    for order in orders:
        customer_name = order.user.username if order.user else 'Guest'
        customer_email = order.user.email if order.user else 'N/A'
        customer_phone = order.phone if hasattr(order, 'phone') else 'N/A'
        total_amount = f"₹{order.total_amount:.2f}"
        status = order.order_status.title()
        date = order.created_at.strftime('%Y-%m-%d %H:%M')

        data.append([
            order.id,
            customer_name,
            customer_email,
            customer_phone,
            total_amount,
            status,
            date
        ])

    # Create table
    table = Table(data, colWidths=[0.8*inch, 1.2*inch, 1.5*inch, 1*inch, 0.8*inch, 1*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))

    # Summary
    total_orders_count = orders.count()
    total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0

    summary_data = [
        ['Total Orders', total_orders_count],
        ['Total Revenue', f"₹{total_revenue:.2f}"]
    ]

    summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(Paragraph("Summary", header_style))
    elements.append(summary_table)

    doc.build(elements)
    return response


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
