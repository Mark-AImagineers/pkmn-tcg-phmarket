from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, Mock
from rest_framework.test import APIClient
import requests

from datetime import date

from cards.services.sync import _parse_date

from users.models import User


class ManageGlobalCardsViewTests(TestCase):
    """Tests for the manage global cards page."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@example.com", password="pass123"
        )
        self.superuser = User.objects.create_superuser(
            email="admin@example.com", password="pass123"
        )
        from cards.models import CardSet, Card
        from datetime import date, datetime

        self.card_set = CardSet.objects.create(
            set_id="x1",
            name="Example Set",
            series="Ex",
            printed_total=1,
            total=1,
            ptcgo_code="EX",
            release_date=date.today(),
            updated_at=datetime.utcnow(),
            symbol_image="http://example.com/symbol.png",
            logo_image="http://example.com/logo.png",
        )
        self.card = Card.objects.create(
            card_id="x1-1",
            name="Sample Card",
            supertype="Pokémon",
            number="1",
            set=self.card_set,
        )

    def test_success_for_anonymous_user(self):
        response = self.client.get(reverse("manage_global_cards"))
        self.assertEqual(response.status_code, 200)

    def test_access_for_non_superuser(self):
        self.client.login(email="user@example.com", password="pass123")
        response = self.client.get(reverse("manage_global_cards"))
        self.assertEqual(response.status_code, 200)

    def test_success_for_superuser(self):
        self.client.login(email="admin@example.com", password="pass123")
        response = self.client.get(reverse("manage_global_cards"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage Global Cards")

    def test_lists_cards_in_context(self):
        self.client.login(email="admin@example.com", password="pass123")
        response = self.client.get(reverse("manage_global_cards"))
        self.assertContains(response, "Sample Card")


class SyncCardsAPITests(TestCase):
    """Tests for the sync cards endpoint."""

    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser(
            email="admin2@example.com", password="pass123"
        )
        self.user = User.objects.create_user(
            email="user2@example.com", password="pass123"
        )
        self.client = APIClient()

    def test_requires_authentication(self):
        response = self.client.post(reverse("api_sync_cards"))
        self.assertEqual(response.status_code, 401)

    def test_forbidden_for_non_superuser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("api_sync_cards"))
        self.assertEqual(response.status_code, 403)

    @patch("cards.api_views.get_missing_cards_ids")
    @patch("cards.api_views.fetch_and_sync_cards")
    def test_sync_for_superuser(self, mock_fetch, mock_get_ids):
        mock_fetch.return_value = 5
        mock_get_ids.return_value = ["x"]
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(reverse("api_sync_cards"))
        self.assertEqual(response.status_code, 200)
        mock_get_ids.assert_called_once()
        mock_fetch.assert_called_once_with(["x"])


class ParseDateTests(TestCase):
    """Tests for the `_parse_date` utility."""

    def test_handles_slash_format(self):
        self.assertEqual(_parse_date("2010/11/03"), date(2010, 11, 3))

    def test_handles_dash_format(self):
        self.assertEqual(_parse_date("2010-11-03"), date(2010, 11, 3))

    def test_invalid_returns_none(self):
        self.assertIsNone(_parse_date("invalid"))
