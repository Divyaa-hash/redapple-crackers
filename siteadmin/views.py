from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


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
