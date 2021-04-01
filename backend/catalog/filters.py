from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F, Q
from django_filters.rest_framework import CharFilter, FilterSet

from catalog.models import Wine


class WineFilterSet(FilterSet):
    query = CharFilter(method='filter_query')

    def filter_query(self, queryset, name, value):
        search_query = Q(
            Q(search_vector=SearchQuery(value)),
        )
        return queryset.annotate(
            search_rank=SearchRank(F('search_vector'), SearchQuery(value)),
        ).filter(search_query).order_by('-search_rank', 'id')

    class Meta:
        model = Wine
        fields = ('query', 'country', 'points')
