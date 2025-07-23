from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, Mock
from rest_framework.test import APIClient
import requests

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


class GetAllCardIDsTests(TestCase):
    """Tests for `get_all_card_ids`."""

    @patch("cards.services.poketcg.requests.get")
    def test_stops_on_empty_data(self, mock_get):
        mock_get.side_effect = [
            Mock(
                status_code=200,
                json=lambda: {"data": [{"id": "x"}], "totalCount": 999},
                raise_for_status=lambda: None,
            ),
            Mock(
                status_code=200,
                json=lambda: {"data": []},
                raise_for_status=lambda: None,
            ),
        ]

        from cards.services.poketcg import get_all_card_ids

        ids = get_all_card_ids()

        self.assertEqual(ids, ["x"])
        self.assertEqual(mock_get.call_count, 2)

    @patch("cards.services.poketcg.requests.get")
    def test_stops_on_404(self, mock_get):
        first = Mock(
            status_code=200,
            json=lambda: {"data": [{"id": "x"}], "totalCount": 999},
            raise_for_status=lambda: None,
        )
        second = Mock(status_code=404)
        second.raise_for_status.side_effect = requests.HTTPError(response=second)
        mock_get.side_effect = [first, second]

        from cards.services.poketcg import get_all_card_ids

        ids = get_all_card_ids()

        self.assertEqual(ids, ["x"])
        self.assertEqual(mock_get.call_count, 2)


class FetchCardDetailsTests(TestCase):
    """Tests for `fetch_card_details`."""

    @patch("cards.services.poketcg.requests.get")
    def test_returns_empty_on_404(self, mock_get):
        mock_res = Mock(status_code=404)
        mock_res.raise_for_status.side_effect = requests.HTTPError(response=mock_res)
        mock_get.return_value = mock_res

        from cards.services.poketcg import fetch_card_details

        data = fetch_card_details("abc")

        self.assertEqual(data, {})
        mock_get.assert_called_once()

    @patch("cards.services.poketcg.requests.get")
    def test_strips_whitespace(self, mock_get):
        mock_res = Mock(status_code=200, json=lambda: {"data": {"id": "x"}})
        mock_res.raise_for_status = lambda: None
        mock_get.return_value = mock_res

        from cards.services.poketcg import fetch_card_details

        data = fetch_card_details(" x \n")

        self.assertEqual(data["id"], "x")
        mock_get.assert_called_once_with(
            "https://api.pokemontcg.io/v2/cards/x",
            headers={},
            timeout=30,
        )
