from django.urls import path

from .api_views import SyncCardsAPIView

urlpatterns = [
    path("cards/sync/", SyncCardsAPIView.as_view(), name="api_sync_cards"),
]
