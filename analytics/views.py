from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg, F
from django.utils import timezone
from datetime import timedelta
from .models import ProductView, SearchQuery, SalesReport, UserActivity
from products.models import Product


def analytics_dashboard(request):
    """
    Main analytics dashboard view.
    """
    # Get today's stats
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    
    # Product views today
    views_today = ProductView.objects.filter(viewed_at__date=today).count()
    views_yesterday = ProductView.objects.filter(viewed_at__date=yesterday).count()
    views_growth = ((views_today - views_yesterday) / views_yesterday * 100) if views_yesterday > 0 else 0
    
    # Search queries today
    searches_today = SearchQuery.objects.filter(searched_at__date=today).count()
    
    # Top products today
    top_products_today = ProductView.objects.filter(
        viewed_at__date=today
    ).values('product__name', 'product__slug').annotate(
        views=Count('id')
    ).order_by('-views')[:10]
    
    # Recent searches
    recent_searches = SearchQuery.objects.order_by('-searched_at')[:20]
    
    # User activity breakdown
    activity_breakdown = UserActivity.objects.filter(
        created_at__date=today
    ).values('activity_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'views_today': views_today,
        'views_growth': views_growth,
        'searches_today': searches_today,
        'top_products_today': top_products_today,
        'recent_searches': recent_searches,
        'activity_breakdown': activity_breakdown,
    }
    
    return render(request, 'analytics/dashboard.html', context)


def product_analytics(request, product_id):
    """
    Detailed analytics for a specific product.
    """
    product = Product.objects.get(id=product_id)
    
    # Views over time (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    views_over_time = ProductView.objects.filter(
        product=product,
        viewed_at__gte=thirty_days_ago
    ).extra(
        select={'day': 'date(viewed_at)'}
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    # Search terms leading to this product
    search_terms = SearchQuery.objects.filter(
        clicked_product=product
    ).values('query').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    context = {
        'product': product,
        'views_over_time': views_over_time,
        'search_terms': search_terms,
    }
    
    return render(request, 'analytics/product_analytics.html', context)


def realtime_stats(request):
    """
    Real-time statistics API endpoint.
    """
    now = timezone.now()
    hour_ago = now - timedelta(hours=1)
    
    stats = {
        'views_last_hour': ProductView.objects.filter(viewed_at__gte=hour_ago).count(),
        'searches_last_hour': SearchQuery.objects.filter(searched_at__gte=hour_ago).count(),
        'active_users': UserActivity.objects.filter(
            created_at__gte=hour_ago
        ).values('user').distinct().count(),
    }
    
    return JsonResponse(stats)