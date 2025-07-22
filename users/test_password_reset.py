from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from users.models import User


class PasswordResetAPITests(TestCase):
    """Tests for the password reset API flow."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="reset@example.com", password="pass123"
        )

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_sends_email(self):
        response = self.client.post(
            reverse("api_password_reset"), {"email": "reset@example.com"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("reset@example.com", mail.outbox[0].to)

    def test_password_reset_confirm_updates_password(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.post(
            reverse("api_password_reset_confirm"),
            {"uid": uid, "token": token, "password": "newpass456"},
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass456"))
