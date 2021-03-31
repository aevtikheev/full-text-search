from django.urls import path

from catalog.views import WinesView

urlpatterns = [
    path('wines/', WinesView.as_view()),
]
