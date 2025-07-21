from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegistrationSerializer, UserSerializer


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
