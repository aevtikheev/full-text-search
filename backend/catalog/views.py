from rest_framework.generics import ListAPIView

from catalog.models import Wine
from catalog.serializers import WineSerializer
from catalog.filters import WineFilterSet


class WinesView(ListAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    filterset_class = WineFilterSet
