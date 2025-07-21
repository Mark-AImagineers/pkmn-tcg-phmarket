from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import User


class MeEndpointTests(SimpleTestCase):
    """Tests for the /api/me/ endpoint."""

    def setUp(self) -> None:
        self.user = User(email="test@example.com")
        self.user.set_password("pass123")
        self.client = APIClient()

    def test_requires_authentication(self):
        response = self.client.get(reverse("api_me"))
        self.assertEqual(response.status_code, 401)

    def test_returns_user_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("api_me"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("email"), self.user.email)
