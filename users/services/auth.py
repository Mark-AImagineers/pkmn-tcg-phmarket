"""Authentication service helpers."""

from django.contrib.auth import authenticate, login
from django.http import HttpRequest


def login_user(request: HttpRequest, email: str, password: str) -> bool:
    """Authenticate and log in a user.

    Returns ``True`` if the credentials are valid, otherwise ``False``.
    """

    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return True
    return False
