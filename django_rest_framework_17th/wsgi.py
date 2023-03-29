"""
WSGI config for django_rest_framework_17th project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from django_rest_framework_17th.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_framework_17th.settings')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

application = get_wsgi_application()
