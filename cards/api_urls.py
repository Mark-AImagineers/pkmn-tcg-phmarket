from django.urls import path

from .api_views import (
    SyncCardsAPIView,
    SyncAllCardsAPIView,
    SyncCardsByVolumeAPIView,
    DiscoverCardsAPIView,
)

urlpatterns = [
    path("cards/sync/", SyncCardsAPIView.as_view(), name="api_sync_cards"),
    path("cards/sync-all/", SyncAllCardsAPIView.as_view(), name="api_sync_all_cards"),
    path(
        "cards/sync-volume/",
        SyncCardsByVolumeAPIView.as_view(),
        name="api_sync_cards_by_volume",
    ),
    path("cards/discover/", DiscoverCardsAPIView.as_view(), name="api_discover_cards"),
]
