"""WSGI config for full_text_search project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'full_text_search.settings')

application = get_wsgi_application()
