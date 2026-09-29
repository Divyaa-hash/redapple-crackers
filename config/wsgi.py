"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# For Vercel with in-memory SQLite, run migrations on EVERY request
if os.environ.get('VERCEL'):
    import django
    django.setup()
    from django.core.management import call_command
    try:
        # Run migrations every time for in-memory database
        call_command('migrate', '--run-syncdb', verbosity=0, interactive=False)
        print("Migrations run for Vercel in-memory database")
    except Exception as e:
        print(f"Migration error: {e}")

application = get_wsgi_application()
