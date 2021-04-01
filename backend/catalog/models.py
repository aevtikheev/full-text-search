from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models


class Wine(models.Model):
    country = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    points = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    variety = models.CharField(max_length=255)
    winery = models.CharField(max_length=255)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [
            GinIndex(name='search_vector_gin_idx', fields=['search_vector']),
        ]

    def __str__(self):
        return f'{self.id}'


def calculate_wine_search_vector():
    """Weighted search vector for Wines. Variety and winery are more important than description."""
    return (
        SearchVector('variety', weight='A')
        + SearchVector('winery', weight='A')
        + SearchVector('description', weight='B')
    )
