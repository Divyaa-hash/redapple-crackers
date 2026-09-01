from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, BrandViewSet, ProductViewSet, ProductReviewViewSet,
    FestivalViewSet, CouponViewSet, catalog_view, product_detail_view
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'products', ProductViewSet)
router.register(r'reviews', ProductReviewViewSet)
router.register(r'festivals', FestivalViewSet)
router.register(r'coupons', CouponViewSet)

urlpatterns = [
    path('catalog/', catalog_view, name='catalog'),
    path('api/', include(router.urls)),
    path('<int:product_id>/', product_detail_view, name='product_detail'),
]
