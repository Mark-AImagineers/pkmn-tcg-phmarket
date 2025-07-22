"""Services to handle password reset flow."""

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from users.models import User


def send_password_reset_email(user: User, base_url: str) -> None:
    """Send a password reset email with a signed token."""

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"{base_url}/password-reset/{uid}/{token}/"
    send_mail(
        "Password Reset",
        f"Reset your password: {reset_link}",
        None,
        [user.email],
        fail_silently=False,
    )
