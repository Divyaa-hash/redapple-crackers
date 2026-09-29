"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# For Vercel with in-memory SQLite, run migrations on startup
if os.environ.get('VERCEL'):
    import django
    django.setup()
    from django.core.management import call_command
    try:
        # Run migrations with --run-syncdb to create tables
        call_command('migrate', '--run-syncdb', verbosity=1)
        print("Migrations run successfully for Vercel in-memory database")
    except Exception as e:
        print(f"Migration error: {e}")
        # Try syncdb as fallback
        try:
            call_command('syncdb', verbosity=0, interactive=False)
            print("Syncdb completed as fallback")
        except Exception as e2:
            print(f"Syncdb error: {e2}")

application = get_wsgi_application()
