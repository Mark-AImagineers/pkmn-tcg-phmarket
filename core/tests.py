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


class SettingsViewTests(TestCase):
    """Tests for the settings page."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user@example.com", password="pass123"
        )
        self.superuser = User.objects.create_superuser(
            email="admin@example.com", password="pass123"
        )

    def test_redirect_if_not_authenticated(self):
        response = self.client.get(reverse("settings"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.headers.get("Location", ""))

    def test_success_for_authenticated_user(self):
        self.client.login(email="user@example.com", password="pass123")
        response = self.client.get(reverse("settings"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Settings")

    def test_admin_panel_link_for_superuser(self):
        self.client.login(email="admin@example.com", password="pass123")
        response = self.client.get(reverse("settings"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Panel")


class AdminPanelViewTests(TestCase):
    """Tests for the admin panel page."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="user2@example.com", password="pass123"
        )
        self.superuser = User.objects.create_superuser(
            email="super@example.com", password="pass123"
        )

    def test_redirect_if_not_authenticated(self):
        response = self.client.get(reverse("admin_panel"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.headers.get("Location", ""))

    def test_forbidden_for_non_superuser(self):
        self.client.login(email="user2@example.com", password="pass123")
        response = self.client.get(reverse("admin_panel"))
        self.assertEqual(response.status_code, 403)

    def test_success_for_superuser(self):
        self.client.login(email="super@example.com", password="pass123")
        response = self.client.get(reverse("admin_panel"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Panel")
