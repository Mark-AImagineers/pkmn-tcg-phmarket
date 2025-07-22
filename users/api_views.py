from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegistrationSerializer,
    UserSerializer,
)
from .services.password_reset import send_password_reset_email

User = get_user_model()


class RegistrationAPIView(APIView):
    """API endpoint for user registration."""

    permission_classes: list = []

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeAPIView(APIView):
    """Return details for the authenticated user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CookieTokenObtainPairView(TokenObtainPairView):
    """Return access token and set refresh token in a secure cookie."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get("refresh")
        if refresh:
            response.set_cookie(
                "refresh_token",
                refresh,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Strict",
                path="/api/token/refresh/",
            )
            del response.data["refresh"]
        return response


class CookieTokenRefreshView(TokenRefreshView):
    """Refresh access token using the HTTP-only cookie."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:  # type: ignore[attr-defined]
            raise InvalidToken(exc.args[0]) from exc

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        new_refresh = serializer.validated_data.get("refresh")
        if new_refresh:
            response.set_cookie(
                "refresh_token",
                new_refresh,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Strict",
                path="/api/token/refresh/",
            )
            del response.data["refresh"]
        return response


class LogoutAPIView(APIView):
    """Remove refresh token cookie to log the user out."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("refresh_token", path="/api/token/refresh/")
        return response


class PasswordResetRequestAPIView(APIView):
    """Send password reset link to the given email address."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            register_url = reverse("register")
            return Response(
                {
                    "detail": "No account found with this email.",
                    "register_url": register_url,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        base_url = f"{request.scheme}://{request.get_host()}"
        send_password_reset_email(user, base_url)
        return Response(status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    """Verify reset token and update the password."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        try:
            uid_int = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_int)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_200_OK)
