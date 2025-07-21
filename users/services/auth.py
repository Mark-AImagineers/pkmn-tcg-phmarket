"""Services related to user authentication and registration."""

from users.models import User


def register_user(email: str, password: str) -> User:
    """Create and return a new user."""

    return User.objects.create_user(email=email, password=password)
