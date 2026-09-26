from django.db.models.signals import post_migrate
from django.dispatch import receiver
from users.models import User


@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    """Create default superuser if it does not exist"""
    if sender.name == 'users':
        email = 'saran450j@gmail.com'
        password = 'Admin@123'
        
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                username='saran_admin',
                password=password,
                first_name='Saran',
                last_name='Admin',
                phone='9345980679'
            )
            print(f"Superuser created: {email}")
        else:
            print(f"Superuser already exists: {email}")
