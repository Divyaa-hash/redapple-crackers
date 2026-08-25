from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('process/', views.process_checkout, name='process_checkout'),
    path('<str:order_number>/', views.order_detail, name='order_detail'),
    path('<str:order_number>/track/', views.order_tracking, name='order_tracking'),
    path('list/', views.order_list, name='order_list'),
]
