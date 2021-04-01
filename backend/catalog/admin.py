from django.contrib import admin

from catalog.models import Wine


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    fields = (
        'id', 'country', 'description', 'points', 'price', 'variety', 'winery', 'search_vector',
    )
    list_display = ('id', 'country', 'points', 'price', 'variety', 'winery')
    list_filter = ('country', 'variety', 'winery')
    ordering = ('variety',)
    readonly_fields = ('id',)
