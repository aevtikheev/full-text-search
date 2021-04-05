from rest_framework import serializers

from catalog.models import Wine, WineSearchWord


class WineSerializer(serializers.ModelSerializer):

    variety = serializers.SerializerMethodField()
    winery = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_variety(self, obj):
        return obj.variety_headline if hasattr(obj, 'variety_headline') else obj.variety

    def get_winery(self, obj):
        return obj.winery_headline if hasattr(obj, 'winery_headline') else obj.winery

    def get_description(self, obj):
        return obj.description_headline if hasattr(obj, 'description_headline') else obj.description

    class Meta:
        model = Wine
        fields = ('id', 'country', 'description', 'points', 'price', 'variety', 'winery')


class WineSearchWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineSearchWord
        fields = ('word',)
