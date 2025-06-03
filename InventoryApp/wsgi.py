"""
WSGI config for InventoryApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from decouple import config

from django.core.wsgi import get_wsgi_application

# Set the default settings module based on environment
environment = config('DJANGO_ENVIRONMENT', default='development')
if environment == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventoryApp.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InventoryApp.settings.development')

application = get_wsgi_application()
