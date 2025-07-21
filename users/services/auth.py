from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from users.models import User


def login_user(request: HttpRequest, email: str, password: str) -> bool:
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return True
    return False


def register_user(email: str, password: str) -> User:
    """Create and return a new user."""

    return User.objects.create_user(email=email, password=password)
