from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from rest_framework.test import APIClient

from datetime import date

from cards.services.poketcg import _parse_date

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

    @patch("cards.api_views.sync_cards")
    def test_sync_for_superuser(self, mock_sync):
        mock_sync.return_value = 5
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(reverse("api_sync_cards"))
        self.assertEqual(response.status_code, 200)
        mock_sync.assert_called_once()


class ParseDateTests(TestCase):
    """Tests for the `_parse_date` utility."""

    def test_handles_slash_format(self):
        self.assertEqual(_parse_date("2010/11/03"), date(2010, 11, 3))

    def test_handles_dash_format(self):
        self.assertEqual(_parse_date("2010-11-03"), date(2010, 11, 3))

    def test_invalid_returns_none(self):
        self.assertIsNone(_parse_date("invalid"))
