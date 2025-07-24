"""API endpoints for the cards app."""

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .services.sync import get_missing_cards_ids, fetch_and_sync_cards
from .services.discovery import discover_all_cards_ids, get_cardref_count

User = get_user_model()


class SyncCardsAPIView(APIView):
    """Synchronize card data from the PokéTCG API."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user: User = request.user
        if not user.is_superuser:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        ids = get_missing_cards_ids()
        created = fetch_and_sync_cards(ids)
        return Response({"detail": f"Synced {created} cards"})


class SyncAllCardsAPIView(APIView):
    """Fetch and sync all missing cards from PokéTCG."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user: User = request.user
        if not user.is_superuser:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        ids = get_missing_cards_ids()
        created = fetch_and_sync_cards(ids)
        return Response({"detail": f"Synced {created} cards"})


class SyncCardsByVolumeAPIView(APIView):
    """Fetch and sync a limited number of missing cards."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user: User = request.user
        if not user.is_superuser:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        limit = int(request.data.get("limit", 0))
        ids = get_missing_cards_ids()
        ids = ids[:limit] if limit > 0 else ids
        created = fetch_and_sync_cards(ids)
        return Response({"detail": f"Synced {created} cards"})


class DiscoverCardsAPIView(APIView):
    """Discover all card IDs from PokéTCG."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user: User = request.user
        if not user.is_superuser:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        discover_all_cards_ids()
        count = get_cardref_count()
        return Response({"detail": f"Discovery complete. {count} IDs stored"})
