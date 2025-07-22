from django.test import TestCase
from django.urls import reverse

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
