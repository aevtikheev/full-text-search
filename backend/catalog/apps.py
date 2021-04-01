from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Config for Catalog app."""

    name = 'catalog'

    def ready(self):
        from . import signals  # noqa: F401
