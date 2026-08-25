"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import render
from products.models import Product, Category
from products.views import shop_view

def home_view(request):
    active = Product.objects.filter(is_active=True)
    trending_products = list(active.filter(is_trending=True)[:8])
    featured_products = list(active.filter(is_featured=True)[:4])
    new_products = list(active.filter(is_new=True)[:4])
    if not trending_products:
        trending_products = list(active[:8])
    if not featured_products:
        featured_products = list(active[:4])
    if not new_products:
        new_products = list(active[4:8])
    return render(request, 'home.html', {
        'trending_products': trending_products,
        'featured_products': featured_products,
        'new_products': new_products
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('home/', home_view, name='home_redirect'),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('orders/', include('orders.urls')),
    path('checkout/', include('orders.urls')),
    path('shop/', shop_view, name='shop'),
    path('categories/', TemplateView.as_view(template_name='categories.html')),
    path('wholesale/', TemplateView.as_view(template_name='wholesale.html')),
    path('offers/', TemplateView.as_view(template_name='festival_offers.html')),
    path('festival-offers/', TemplateView.as_view(template_name='festival_offers.html')),
    path('about/', TemplateView.as_view(template_name='about.html')),
    path('contact/', TemplateView.as_view(template_name='contact.html')),
    path('safety/', TemplateView.as_view(template_name='safety_guidelines.html')),
    path('order-confirmation/', TemplateView.as_view(template_name='order_confirmation.html'), name='order_confirmation'),
    path('order-tracking/', TemplateView.as_view(template_name='order_tracking.html'), name='order_tracking'),
    # Auth URLs
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('logout/', TemplateView.as_view(template_name='logout.html'), name='logout'),
    path('account/', TemplateView.as_view(template_name='account.html'), name='account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
