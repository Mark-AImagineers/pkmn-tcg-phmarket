from django.test import TestCase
from django.urls import reverse

from users.models import User


class HomeViewTests(TestCase):
    """Tests for access to the home page."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@example.com", password="pass123"
        )

    def test_redirect_if_not_authenticated(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.headers.get("Location", ""))

    def test_success_for_authenticated_user(self):
        self.client.login(email="test@example.com", password="pass123")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
