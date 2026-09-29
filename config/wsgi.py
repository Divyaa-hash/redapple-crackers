"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

# Disable Django logging for Vercel completely
if os.environ.get('VERCEL'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    import logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # Prevent Django from configuring file logging
    os.environ['DJANGO_LOG_LEVEL'] = 'INFO'

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Run migrations on startup for Vercel
if os.environ.get('VERCEL'):
    import django
    django.setup()
    from django.core.management import call_command
    try:
        call_command('migrate', verbosity=0, interactive=False)
        print("Migrations completed successfully")
    except Exception as e:
        print(f"Migration error: {e}")

application = get_wsgi_application()
