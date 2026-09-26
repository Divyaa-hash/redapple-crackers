from django.db.models.signals import post_migrate
from django.dispatch import receiver
from users.models import User


@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    """Create default superuser if it does not exist"""
    if sender.name == 'users':
        email = 'saran450j@gmail.com'
        password = 'Admin@123'
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': 'saran_admin',
                'first_name': 'Saran',
                'last_name': 'Admin',
                'phone': '9345980679'
            }
        )
        
        # Always set the password to ensure it's correct
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        if created:
            print(f"Superuser created: {email}")
        else:
            print(f"Superuser password updated: {email}")
