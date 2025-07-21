from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase

from .models import User


class JWTAuthCookieTests(TestCase):
    """Tests for JWT authentication flow using cookies."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@example.com",
            password="pass123",
        )
        self.client = APIClient()

    def test_login_sets_refresh_cookie(self):
        response = self.client.post(
            reverse("api_login"),
            {"email": "test@example.com", "password": "pass123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
        self.assertNotIn("refresh", response.json())
        self.assertIn("refresh_token", response.cookies)
        cookie = response.cookies["refresh_token"]
        self.assertTrue(cookie["httponly"])  # type: ignore[index]

    def test_refresh_uses_cookie(self):
        login = self.client.post(
            reverse("api_login"),
            {"email": "test@example.com", "password": "pass123"},
            format="json",
        )
        self.assertEqual(login.status_code, 200)
        self.client.cookies = login.cookies
        refresh = self.client.post(reverse("api_token_refeesh"))
        self.assertEqual(refresh.status_code, 200)
        self.assertIn("access", refresh.json())
