from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVectorField, SearchVector, TrigramSimilarity,
)
from django.db import models
from django.db.models import F, Q


TRIGRAM_SIMILARITY_THRESHOLD = 0.3


class WineQuerySet(models.query.QuerySet):
    def search(self, query):
        search_query = Q(search_vector=SearchQuery(query))

        return self.annotate(
            variety_headline=SearchHeadline(F('variety'), SearchQuery(query)),
            winery_headline=SearchHeadline(F('winery'), SearchQuery(query)),
            description_headline=SearchHeadline(F('description'), SearchQuery(query)),
            search_rank=SearchRank(F('search_vector'), SearchQuery(query)),
        ).filter(search_query).order_by('-search_rank', 'id')


class Wine(models.Model):
    country = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    points = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    variety = models.CharField(max_length=255)
    winery = models.CharField(max_length=255)
    search_vector = SearchVectorField(null=True, blank=True)

    objects = WineQuerySet.as_manager()

    class Meta:
        indexes = [
            GinIndex(name='search_vector_gin_idx', fields=['search_vector']),
        ]

    def __str__(self):
        return f'{self.id}'


class WineSearchWordQuerySet(models.query.QuerySet):
    def search(self, query):
        return self.annotate(
            similarity=TrigramSimilarity('word', query),
        ).filter(similarity__gte=TRIGRAM_SIMILARITY_THRESHOLD).order_by('-similarity')


class WineSearchWord(models.Model):
    """Unique words that appear in Wine records. Used for similarity search."""
    word = models.CharField(max_length=255, unique=True)

    objects = WineSearchWordQuerySet.as_manager()

    def __str__(self):
        return self.word


class SearchHeadline(models.Func):
    """Highlights the search result with a <mark> tag."""
    function = 'ts_headline'
    output_field = models.TextField()
    template = (
        '%(function)s(%(expressions)s, \'StartSel = <mark>, StopSel = </mark>, HighlightAll=TRUE\')'
    )


def calculate_wine_search_vector():
    """Weighted search vector for Wines. Variety and winery are more important than description."""
    return (
        SearchVector('variety', weight='A')
        + SearchVector('winery', weight='A')
        + SearchVector('description', weight='B')
    )
