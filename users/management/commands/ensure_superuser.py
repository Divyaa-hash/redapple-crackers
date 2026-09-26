from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import User


class Command(BaseCommand):
    help = 'Ensure default superuser exists with correct password'

    def handle(self, *args, **options):
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
            self.stdout.write(self.style.SUCCESS(f'Superuser created: {email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser password updated: {email}'))
