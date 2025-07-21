from django.test import TestCase
from django.urls import reverse

from users.models import User


class ProfileViewTests(TestCase):
    """Tests for the profile page."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@example.com", password="pass123"
        )

    def test_success_for_anonymous_user(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_success_for_authenticated_user(self):
        self.client.login(email="test@example.com", password="pass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile")
