from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import User


class Command(BaseCommand):
    help = 'Ensure default superuser exists'

    def handle(self, *args, **options):
        email = 'saran450j@gmail.com'
        password = 'Admin@123'
        
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(
                email=email,
                username='saran_admin',
                first_name='Saran',
                last_name='Admin',
                phone='9345980679'
            )
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser created: {email}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser already exists: {email}'))
