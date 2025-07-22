"""API endpoints for the cards app."""

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .services.poketcg import sync_cards

User = get_user_model()


class SyncCardsAPIView(APIView):
    """Synchronize card data from the PokéTCG API."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user: User = request.user
        if not user.is_superuser:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        created = sync_cards()
        return Response({"detail": f"Synced {created} cards"})
