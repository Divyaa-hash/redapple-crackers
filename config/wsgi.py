"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import logging
import sys

# Monkey-patch Django's configure_logging to prevent file handler errors
original_configure_logging = None

def safe_configure_logging(config, settings_dict):
    """Safe logging configuration that prevents file handlers"""
    try:
        # Remove any file handlers from config
        if 'handlers' in config:
            config['handlers'] = {
                k: v for k, v in config['handlers'].items()
                if v.get('class', '') != 'logging.FileHandler'
            }
    except:
        pass

# Import Django and patch before setup
import django.utils.log as django_log
django_log.configure_logging = safe_configure_logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application

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
