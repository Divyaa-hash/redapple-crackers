from django.urls import path
from . import views

app_name = 'siteadmin'

urlpatterns = [
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notification-center/', views.notification_center, name='notification_center'),
]
