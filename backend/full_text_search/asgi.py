"""ASGI config for full_text_search project."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'full_text_search.settings')

application = get_asgi_application()
