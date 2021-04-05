from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver

from catalog.models import Wine, calculate_wine_search_vector


@receiver(post_save, sender=Wine, dispatch_uid='on_wine_save')
def on_wine_save(sender, instance, *args, **kwargs):
    """Add search vector for wine."""
    sender.objects.filter(pk=instance.id).update(search_vector=calculate_wine_search_vector())

    with connection.cursor() as cursor:
        cursor.execute(
            """
                INSERT INTO catalog_winesearchword (word)
                SELECT word FROM ts_stat('
                  SELECT to_tsvector(''simple'', winery) ||
                         to_tsvector(''simple'', coalesce(description, ''''))
                  FROM catalog_wine
                  WHERE id = '%s'
                ')
                ON CONFLICT (word) DO NOTHING;
            """,
            [str(instance.id)],
        )
